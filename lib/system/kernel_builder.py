import os
import re
import sys
import shutil
import struct
import zipfile
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional

ARM64_IMAGE_MAGIC = 0x644d5241  # 'ARM\x64' at offset 0x38 in Little Endian

REQUIRED_BUILD_TOOLS = [
    "clang", "ld.lld", "llvm-ar", "llvm-nm",
    "bison", "flex", "bc", "rsync", "make"
]

RECOMMENDED_GKI_CONFIGS = [
    ("CONFIG_ARM64", "y"),
    ("CONFIG_KPROBES", "y"),
    ("CONFIG_HAVE_KPROBES", "y"),
    ("CONFIG_BPF_SYSCALL", "y"),
    ("CONFIG_MODULES", "y"),
    ("CONFIG_OVERLAY_FS", "y")
]

class KernelBuilder:
    """Android GKI Linux Kernel compilation auditor, defconfig doctor and AnyKernel3 packager."""

    @classmethod
    def check_environment(cls) -> Dict[str, Any]:
        """Audits host or Termux environment for kernel build requirements."""
        tools_status = {}
        missing_tools = []

        for t in REQUIRED_BUILD_TOOLS:
            p = shutil.which(t)
            tools_status[t] = bool(p)
            if not p:
                missing_tools.append(t)

        clang_ver = "unknown"
        if shutil.which("clang"):
            try:
                import subprocess
                out = subprocess.run(["clang", "--version"], capture_output=True, text=True, timeout=5).stdout
                m = re.search(r"clang version\s+([\d\.]+)", out)
                if m:
                    clang_ver = m.group(1)
            except Exception:
                pass

        return {
            "ready_for_compilation": len(missing_tools) == 0,
            "clang_version": clang_ver,
            "toolchain_audit": tools_status,
            "missing_tools": missing_tools,
            "recommended_flags": {
                "ARCH": "arm64",
                "LLVM": "1",
                "LLVM_IAS": "1",
                "CROSS_COMPILE": "aarch64-linux-gnu-"
            }
        }

    @classmethod
    def audit_defconfig(cls, defconfig_path: Path) -> Dict[str, Any]:
        """Audits a kernel defconfig or .config file for GKI compliance and required flags."""
        if not defconfig_path.exists():
            return {"status": "ERROR", "message": f"Config file not found: {defconfig_path}"}

        content = defconfig_path.read_text(encoding="utf-8", errors="replace")
        present_configs = {}
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                present_configs[k.strip()] = v.strip().strip("\"'")

        checks = []
        passed_count = 0

        for opt, expected in RECOMMENDED_GKI_CONFIGS:
            actual = present_configs.get(opt)
            passed = (actual == expected)
            if passed:
                passed_count += 1
            checks.append({
                "option": opt,
                "expected": expected,
                "actual": actual,
                "status": "PASS" if passed else "MISSING"
            })

        return {
            "status": "SUCCESS",
            "file": str(defconfig_path),
            "total_options": len(present_configs),
            "gki_compliance_score": f"{passed_count}/{len(RECOMMENDED_GKI_CONFIGS)}",
            "checks": checks
        }

    @classmethod
    def verify_kernel_image(cls, image_path: Path) -> Dict[str, Any]:
        """Verifies if a compiled kernel Image is a valid ARM64 GKI Linux kernel binary."""
        if not image_path.exists():
            return {"status": "ERROR", "message": f"Kernel Image not found: {image_path}"}

        size = image_path.stat().st_size
        if size < 64:
            return {"status": "ERROR", "message": "File too small to be an ARM64 kernel Image"}

        with open(image_path, "rb") as f:
            header = f.read(64)

        # ARM64 Image header format:
        # offset 0x38 (56) = 0x644d5241 ('ARM\x64')
        magic = struct.unpack("<I", header[56:60])[0]
        is_arm64 = (magic == ARM64_IMAGE_MAGIC)

        text_offset = struct.unpack("<Q", header[8:16])[0]
        image_size = struct.unpack("<Q", header[16:24])[0]

        h = hashlib.sha256()
        with open(image_path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)

        return {
            "status": "SUCCESS" if is_arm64 else "INVALID_MAGIC",
            "path": str(image_path),
            "is_valid_arm64": is_arm64,
            "image_size_bytes": size,
            "header_image_size": image_size,
            "text_offset": hex(text_offset),
            "sha256": h.hexdigest()
        }

    @classmethod
    def pack_anykernel3(cls, kernel_image: Path, output_zip: Path, device_name: str = "Android Device") -> Dict[str, Any]:
        """Creates an AnyKernel3 flashable recovery zip package."""
        if not kernel_image.exists():
            return {"status": "ERROR", "message": f"Kernel image not found: {kernel_image}"}

        verify = cls.verify_kernel_image(kernel_image)
        if not verify.get("is_valid_arm64"):
            return {"status": "ERROR", "message": "Refusing to pack invalid ARM64 kernel binary"}

        output_zip.parent.mkdir(parents=True, exist_ok=True)

        anykernel_sh = f"""#!/sbin/sh
# AnyKernel3 Deployment Script
# Automatically packed by wc-kernel-builder

properties() {{
kernel.string=Custom Linux GKI Kernel for {device_name}
do.devicecheck=0
do.modules=0
do.cleanup=1
do.cleanuponabort=0
}}

# Boot block setup
block=boot;
is_active_slot=`getprop ro.boot.slot_suffix`;
slot=$is_active_slot;

# Flash boot image
ui_print " "; ui_print "Flashing custom kernel Image...";
write_boot;
"""

        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(kernel_image, arcname="Image")
            z.writestr("anykernel.sh", anykernel_sh)
            z.writestr("banner", f"--- Custom GKI Kernel for {device_name} ---\nPacked with wc-kernel-builder\n")

        return {
            "status": "SUCCESS",
            "package": str(output_zip),
            "size_bytes": output_zip.stat().st_size,
            "kernel_image": str(kernel_image)
        }
