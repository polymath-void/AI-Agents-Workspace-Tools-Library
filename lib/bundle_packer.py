import os
import json
import zipfile
import hashlib
from pathlib import Path

def calculate_sha256(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def pack_piuu_bundle(source_dir, output_path, name="custom-extension", version="1.0.0", entry_point="index.js"):
    """
    Packs a folder into a standard .piuu extension bundle with manifest and checksums.
    """
    src = Path(source_dir).resolve()
    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    manifest_file = src / "manifest.json"
    if not manifest_file.exists():
        # Create a default manifest
        manifest = {
            "id": f"com.piuu.ext.{name.lower().replace(' ', '-')}",
            "name": name,
            "version": version,
            "entryPoint": entry_point,
            "permissions": ["storage", "ui"]
        }
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    # Create zip / .piuu archive
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root_dir, _, files in os.walk(src):
            for file in files:
                full_path = Path(root_dir) / file
                rel_path = full_path.relative_to(src)
                zf.write(full_path, arcname=str(rel_path))

    sha256 = calculate_sha256(out)
    return {
        "bundle_path": str(out),
        "size_bytes": out.stat().st_size,
        "sha256": sha256
    }

def verify_piuu_bundle(bundle_path):
    """
    Verifies the integrity and manifest validity of a .piuu bundle.
    """
    path = Path(bundle_path).resolve()
    if not path.exists():
        return {"valid": False, "error": "Bundle file does not exist"}

    try:
        with zipfile.ZipFile(path, "r") as zf:
            namelist = zf.namelist()
            if "manifest.json" not in namelist:
                return {"valid": False, "error": "Missing manifest.json in bundle root"}

            manifest_data = json.loads(zf.read("manifest.json").decode("utf-8"))
            required_keys = {"id", "name", "version"}
            missing = required_keys - set(manifest_data.keys())
            if missing:
                return {"valid": False, "error": f"Manifest missing required keys: {missing}"}

            return {
                "valid": True,
                "manifest": manifest_data,
                "files_count": len(namelist),
                "sha256": calculate_sha256(path)
            }
    except Exception as e:
        return {"valid": False, "error": str(e)}
