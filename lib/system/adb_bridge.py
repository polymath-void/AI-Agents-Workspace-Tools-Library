import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

class ADBBridge:
    """Termux & Linux wireless ADB connection manager, port discovery, remote shell and screencap tool."""

    @staticmethod
    def get_adb_binary() -> str:
        """Finds active adb binary in PATH or Termux PREFIX."""
        which_adb = shutil.which("adb")
        if which_adb:
            return which_adb
        termux_adb = Path("/data/data/com.termux/files/usr/bin/adb")
        if termux_adb.exists():
            return str(termux_adb)
        return "adb"

    @classmethod
    def run_adb_command(cls, args: List[str], timeout: int = 15) -> Dict[str, Any]:
        """Executes raw adb binary command with timeout and return status."""
        adb_bin = cls.get_adb_binary()
        cmd = [adb_bin] + args
        try:
            p = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "success": p.returncode == 0,
                "returncode": p.returncode,
                "stdout": p.stdout.strip(),
                "stderr": p.stderr.strip(),
                "command": " ".join(cmd)
            }
        except FileNotFoundError:
            return {
                "success": False,
                "returncode": 127,
                "stdout": "",
                "stderr": f"ADB binary '{adb_bin}' not found in environment PATH.",
                "command": " ".join(cmd)
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": 124,
                "stdout": "",
                "stderr": f"ADB command timed out after {timeout}s",
                "command": " ".join(cmd)
            }

    @classmethod
    def list_devices(cls) -> Dict[str, Any]:
        """Lists connected USB and Wireless ADB devices."""
        res = cls.run_adb_command(["devices", "-l"])
        if not res["success"] and "not found" in res["stderr"]:
            return {"status": "ERROR", "message": res["stderr"], "devices": []}

        devices = []
        for line in res["stdout"].splitlines()[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            serial = parts[0]
            state = parts[1] if len(parts) > 1 else "unknown"
            
            meta = {}
            for item in parts[2:]:
                if ":" in item:
                    k, v = item.split(":", 1)
                    meta[k] = v

            devices.append({
                "serial": serial,
                "state": state,
                "model": meta.get("model", "unknown"),
                "product": meta.get("product", "unknown"),
                "device": meta.get("device", "unknown")
            })

        return {
            "status": "SUCCESS",
            "device_count": len(devices),
            "devices": devices
        }

    @classmethod
    def pair_wireless(cls, host_port: str, pairing_code: str) -> Dict[str, Any]:
        """Pairs with an Android 11+ Wireless Debugging service."""
        return cls.run_adb_command(["pair", host_port, pairing_code], timeout=20)

    @classmethod
    def connect_wireless(cls, host_port: str) -> Dict[str, Any]:
        """Connects to a Wireless ADB target."""
        return cls.run_adb_command(["connect", host_port], timeout=15)

    @classmethod
    def run_shell(cls, command: str, serial: Optional[str] = None) -> Dict[str, Any]:
        """Executes a shell command on target device."""
        args = []
        if serial:
            args.extend(["-s", serial])
        args.extend(["shell", command])
        return cls.run_adb_command(args, timeout=30)

    @classmethod
    def capture_screenshot(cls, output_path: Path, serial: Optional[str] = None) -> Dict[str, Any]:
        """Captures device framebuffer screenshot directly to local file."""
        adb_bin = cls.get_adb_binary()
        args = [adb_bin]
        if serial:
            args.extend(["-s", serial])
        args.extend(["exec-out", "screencap", "-p"])

        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(output_path, "wb") as f:
                p = subprocess.run(args, stdout=f, stderr=subprocess.PIPE, timeout=20)
            
            if p.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0:
                return {
                    "status": "SUCCESS",
                    "file": str(output_path),
                    "size_bytes": output_path.stat().st_size
                }
            return {
                "status": "ERROR",
                "message": p.stderr.decode("utf-8", errors="replace").strip()
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    @classmethod
    def get_telemetry(cls, serial: Optional[str] = None) -> Dict[str, Any]:
        """Extracts battery, display resolution, OS version and CPU ABI telemetry."""
        dev_res = cls.list_devices()
        if dev_res["device_count"] == 0:
            return {"status": "NO_DEVICES", "message": "No ADB devices connected"}

        target_serial = serial or dev_res["devices"][0]["serial"]

        # Run properties check
        props_cmd = "getprop ro.build.version.release && getprop ro.product.cpu.abi && dumpsys battery | grep level"
        shell_res = cls.run_shell(props_cmd, target_serial)

        lines = shell_res.get("stdout", "").splitlines()
        os_version = lines[0] if len(lines) > 0 else "unknown"
        abi = lines[1] if len(lines) > 1 else "unknown"
        battery_line = lines[2] if len(lines) > 2 else ""
        battery_level = re.search(r"\d+", battery_line).group(0) if re.search(r"\d+", battery_line) else "unknown"

        return {
            "status": "SUCCESS",
            "serial": target_serial,
            "android_version": os_version,
            "cpu_abi": abi,
            "battery_level_percent": battery_level
        }
