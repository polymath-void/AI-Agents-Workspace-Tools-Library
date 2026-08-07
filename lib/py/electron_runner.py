import os
import re
import json
import zipfile
from pathlib import Path
from typing import Dict, Any, List, Optional

class ElectronStudioRunner:
    """Headless Electron IPC bridge mock validator, preload context test harness and extension studio simulator."""

    @classmethod
    def audit_security(cls, main_js: Path) -> Dict[str, Any]:
        """Audits Electron BrowserWindow constructor flags for security vulnerabilities."""
        if not main_js.exists():
            return {"status": "ERROR", "message": f"main.js not found: {main_js}"}

        content = main_js.read_text(encoding="utf-8", errors="replace")
        
        has_node_integration = bool(re.search(r"nodeIntegration\s*:\s*true", content))
        has_context_isolation = bool(re.search(r"contextIsolation\s*:\s*true", content))
        has_sandbox = bool(re.search(r"sandbox\s*:\s*true", content))

        issues = []
        if has_node_integration:
            issues.append("VULNERABILITY: 'nodeIntegration: true' exposes Node.js primitives to renderer process.")
        if not has_context_isolation and "contextIsolation" in content:
            issues.append("VULNERABILITY: 'contextIsolation' should be explicitly set to true.")

        return {
            "status": "PASS" if not issues else "WARN",
            "file": str(main_js),
            "node_integration_disabled": not has_node_integration,
            "context_isolation_enabled": has_context_isolation or not has_node_integration,
            "sandbox_enabled": has_sandbox,
            "security_issues": issues
        }

    @classmethod
    def audit_ipc_channels(cls, main_js: Path, preload_js: Optional[Path] = None) -> Dict[str, Any]:
        """Extracts and cross-references IPC handlers in main process against invocations in preload bridge."""
        if not main_js.exists():
            return {"status": "ERROR", "message": f"File not found: {main_js}"}

        main_content = main_js.read_text(encoding="utf-8", errors="replace")
        main_handles = re.findall(r"ipcMain\.(?:handle|on)\s*\(\s*['\"]([^'\"]+)['\"]", main_content)

        preload_invokes = []
        if preload_js and preload_js.exists():
            preload_content = preload_js.read_text(encoding="utf-8", errors="replace")
            preload_invokes = re.findall(r"ipcRenderer\.(?:invoke|send)\s*\(\s*['\"]([^'\"]+)['\"]", preload_content)

        unhandled = [ch for ch in preload_invokes if ch not in main_handles]

        return {
            "status": "SUCCESS",
            "main_ipc_handlers": sorted(list(set(main_handles))),
            "preload_ipc_invocations": sorted(list(set(preload_invokes))),
            "unhandled_invocations": unhandled,
            "contract_matched": len(unhandled) == 0
        }

    @classmethod
    def simulate_bundle_import(cls, piuu_bundle: Path) -> Dict[str, Any]:
        """Simulates importing and validating a .piuu extension bundle in the desktop studio."""
        if not piuu_bundle.exists():
            return {"status": "ERROR", "message": f"Bundle file not found: {piuu_bundle}"}

        try:
            with zipfile.ZipFile(piuu_bundle, "r") as z:
                names = z.namelist()
                has_plugin_json = "plugin.json" in names
                has_theme_json = "theme.json" in names or "theme/theme.json" in names
                has_preview = any(n.startswith("preview.") or n == "preview.png" for n in names)

                manifest_data = {}
                if has_plugin_json:
                    manifest_data = json.loads(z.read("plugin.json").decode("utf-8"))

                return {
                    "status": "SUCCESS",
                    "bundle": str(piuu_bundle),
                    "file_count": len(names),
                    "has_plugin_json": has_plugin_json,
                    "has_theme_json": has_theme_json,
                    "has_preview_image": has_preview,
                    "plugin_id": manifest_data.get("id", manifest_data.get("name", "unknown")),
                    "version": manifest_data.get("version", "1.0.0"),
                    "is_valid_piuu": has_plugin_json and (has_theme_json or has_preview)
                }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}
