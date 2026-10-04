import datetime
import hashlib
import fnmatch
import json
import os
import shutil
import sys
import tarfile
from pathlib import Path
from .config import (
    HOME,
    EXCLUDED_PATTERNS,
    MANIFEST_FILE,
    TEMP_DIR,
    get_active_targets
)

AGY_USER_DATA_DIR = HOME / ".gemini" / "antigravity-cli"
PRE_RESTORE_BAK_DIR = HOME / ".gemini" / "antigravity-cli.pre-restore.bak"

def compute_file_sha256(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""

def is_excluded(rel_path):
    path_str = str(rel_path)
    for pattern in EXCLUDED_PATTERNS:
        if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(os.path.basename(path_str), pattern):
            return True
    return False

def load_manifest():
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_manifest(manifest):
    MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

def scan_target_files(target_name, target_info):
    base_dir = target_info.get("path")
    inclusions = target_info.get("inclusions", [])
    
    if not base_dir or not base_dir.exists():
        return {}

    file_hashes = {}

    for item in inclusions:
        if item == ".":
            src_path = base_dir
        else:
            src_path = base_dir / item

        if not src_path.exists():
            continue

        if src_path.is_file():
            rel_path = item
            if not is_excluded(rel_path):
                file_hashes[rel_path] = compute_file_sha256(src_path)
        else:
            for root, dirs, files in os.walk(src_path):
                try:
                    rel_root = Path(root).relative_to(base_dir)
                except ValueError:
                    continue

                if is_excluded(rel_root):
                    dirs.clear()
                    continue

                for f in files:
                    file_rel = str(rel_root / f)
                    if not is_excluded(file_rel):
                        full_file_path = base_dir / file_rel
                        file_hashes[file_rel] = compute_file_sha256(full_file_path)

    return file_hashes

def has_target_changed(target_name, target_info):
    manifest = load_manifest()
    last_target_hashes = manifest.get(target_name, {}).get("hashes", {})
    current_hashes = scan_target_files(target_name, target_info)

    if not current_hashes:
        return False, current_hashes

    if current_hashes == last_target_hashes:
        return False, current_hashes
    
    return True, current_hashes

def create_target_archive(target_name, target_info, output_dir=TEMP_DIR):
    base_dir = target_info.get("path")
    inclusions = target_info.get("inclusions", [])
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    archive_name = f"{target_name}_backup_latest.tar.gz"
    archive_path = output_dir / archive_name
    sha256_path = output_dir / f"{archive_name}.sha256"

    print(f"Archiving \033[1m{target_info['name']}\033[0m from \033[1m{base_dir}\033[0m ...")

    with tarfile.open(archive_path, "w:gz") as tar:
        for item in inclusions:
            if item == ".":
                src_path = base_dir
            else:
                src_path = base_dir / item

            if not src_path.exists():
                continue

            if src_path.is_file():
                tar.add(src_path, arcname=item)
            else:
                for root, dirs, files in os.walk(src_path):
                    try:
                        rel_root = Path(root).relative_to(base_dir)
                    except ValueError:
                        continue

                    if is_excluded(rel_root):
                        dirs.clear()
                        continue

                    for f in files:
                        file_rel = rel_root / f
                        if not is_excluded(file_rel):
                            full_file_path = base_dir / file_rel
                            arc_name = item if item != "." else str(file_rel)
                            tar.add(full_file_path, arcname=str(file_rel))

    sha256_hex = compute_file_sha256(archive_path)
    with open(sha256_path, "w") as f:
        f.write(f"{sha256_hex}  {archive_name}\n")

    size_mb = archive_path.stat().st_size / (1024 * 1024)
    print(f"\033[1;32m✓ Created {target_name.upper()} Archive:\033[0m {archive_name} ({size_mb:.2f} MB)")
    print(f"\033[1;34m  SHA256:\033[0m {sha256_hex}")

    return archive_path, sha256_path, sha256_hex

def update_manifest_entry(target_name, hashes, sha256_hex, file_id=""):
    manifest = load_manifest()
    manifest[target_name] = {
        "last_backup": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "archive_sha256": sha256_hex,
        "gdrive_file_id": file_id,
        "hashes": hashes
    }
    save_manifest(manifest)

def verify_checksum(archive_path, sha256_path):
    if not sha256_path.exists():
        return True

    with open(sha256_path, "r") as f:
        line = f.read().strip()
        expected_hash = line.split()[0]

    computed_hash = compute_file_sha256(archive_path)
    if computed_hash.lower() == expected_hash.lower():
        print(f"\033[1;32m✓ Checksum verification passed.\033[0m ({computed_hash})")
        return True
    else:
        print(f"\033[1;31m✗ Checksum mismatch!\033[0m Expected {expected_hash}, got {computed_hash}", file=sys.stderr)
        return False

def create_pre_restore_snapshot():
    target_dir = AGY_USER_DATA_DIR
    if target_dir.exists():
        print(f"Creating pre-restore safety snapshot at \033[1m{PRE_RESTORE_BAK_DIR}\033[0m...")
        if PRE_RESTORE_BAK_DIR.exists():
            shutil.rmtree(PRE_RESTORE_BAK_DIR)
        shutil.copytree(target_dir, PRE_RESTORE_BAK_DIR, symlinks=True)
        print("\033[1;32m✓ Pre-restore safety snapshot saved.\033[0m")
    return PRE_RESTORE_BAK_DIR

def restore_target_archive(target_name, target_info, archive_path):
    target_dir = target_info.get("path", AGY_USER_DATA_DIR)
    archive_path = Path(archive_path)
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive file not found: {archive_path}")

    print(f"Restoring \033[1m{target_name.upper()}\033[0m data into \033[1m{target_dir}\033[0m...")
    
    with tarfile.open(archive_path, "r:gz") as tar:
        tar.extractall(path=target_dir)

    try:
        os.system(f"termux-fix-shebang {target_dir}/skills/*/*.sh >/dev/null 2>&1")
    except Exception:
        pass

    print(f"\033[1;32m✓ {target_name.upper()} Restoration completed successfully!\033[0m")

def rollback_snapshot():
    target_dir = AGY_USER_DATA_DIR
    if not PRE_RESTORE_BAK_DIR.exists():
        print(f"Error: No pre-restore snapshot found at {PRE_RESTORE_BAK_DIR}", file=sys.stderr)
        return False

    print(f"Rolling back to pre-restore snapshot from \033[1m{PRE_RESTORE_BAK_DIR}\033[0m...")
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(PRE_RESTORE_BAK_DIR, target_dir, symlinks=True)
    print("\033[1;32m✓ Rollback successful! Restored previous state.\033[0m")
    return True
