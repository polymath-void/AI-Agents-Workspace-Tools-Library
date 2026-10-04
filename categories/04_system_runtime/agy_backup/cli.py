import argparse
import os
import shutil
import sys
import time
from pathlib import Path

from .auth import (
    load_credentials,
    perform_device_flow_auth,
    get_valid_access_token,
    load_tokens
)
from .config import (
    HOME,
    KNOWN_CLIENTS,
    MAX_BACKUPS,
    TEMP_DIR,
    load_user_config,
    save_user_config,
    get_active_targets
)
from .gdrive import (
    get_or_create_backup_folder,
    upload_or_update_file,
    list_backups,
    download_file,
    delete_file
)
from .archive import (
    has_target_changed,
    create_target_archive,
    update_manifest_entry,
    verify_checksum,
    create_pre_restore_snapshot,
    restore_target_archive,
    rollback_snapshot
)

def cmd_auth(args):
    creds = load_credentials()
    client_id = args.client_id or creds.get("client_id")
    client_secret = args.client_secret or creds.get("client_secret")

    if not client_id:
        print("\033[1;33mGoogle Drive Client Credentials Needed:\033[0m")
        client_id = input("Enter Google OAuth Client ID: ").strip()
        client_secret = input("Enter Google OAuth Client Secret: ").strip()

    if not client_id:
        print("Error: Client ID is required for authentication.", file=sys.stderr)
        sys.exit(1)

    success = perform_device_flow_auth(client_id, client_secret)
    if not success:
        sys.exit(1)

def cmd_config(args):
    cfg = load_user_config()
    print("\n=======================================================")
    print("  \033[1mUNIVERSAL BACKUP CONFIGURATION MANAGER\033[0m")
    print("=======================================================")

    print("\n[1] Configure Active CLI Agent Clients & System Targets:")
    current_enabled = cfg.get("enabled_targets", ["agy", "gemini", "termux"])
    
    for key, client_info in KNOWN_CLIENTS.items():
        is_active = key in current_enabled
        status_str = "\033[1;32m[ENABLED]\033[0m" if is_active else "[DISABLED]"
        print(f"  - {key:<8} ({client_info['name']:<25}) -> {status_str}")

    print("\nOptions:")
    print("  1. Enable / Disable a Client Target (e.g. type 'toggle agy' or 'toggle hermes')")
    print("  2. Add Custom Storage Directory (type 'add <dir_path>')")
    print("  3. Remove Custom Storage Directory (type 'remove <dir_path>')")
    print("  4. View All Configured Targets (type 'list')")
    print("  5. Exit Configuration (press Enter)")

    choice = input("\nEnter configuration command (or press Enter to exit): ").strip()
    if not choice:
        return

    parts = choice.split(maxsplit=1)
    action = parts[0].lower()
    val = parts[1].strip() if len(parts) > 1 else ""

    if action == "toggle" and val:
        if val in KNOWN_CLIENTS:
            if val in current_enabled:
                current_enabled.remove(val)
                print(f"Disabled {KNOWN_CLIENTS[val]['name']}.")
            else:
                current_enabled.append(val)
                print(f"Enabled {KNOWN_CLIENTS[val]['name']}.")
            cfg["enabled_targets"] = current_enabled
            save_user_config(cfg)
        else:
            print(f"Unknown client target '{val}'. Known targets: {list(KNOWN_CLIENTS.keys())}")

    elif action == "add" and val:
        p = Path(val).expanduser().resolve()
        if not p.exists():
            print(f"Error: Path '{p}' does not exist.", file=sys.stderr)
        else:
            custom_dirs = cfg.get("custom_directories", [])
            p_str = str(p)
            if p_str not in custom_dirs:
                custom_dirs.append(p_str)
                cfg["custom_directories"] = custom_dirs
                save_user_config(cfg)
                print(f"\033[1;32m✓ Added custom directory:\033[0m {p_str}")
            else:
                print(f"Directory '{p_str}' is already in custom directories.")

    elif action == "remove" and val:
        custom_dirs = cfg.get("custom_directories", [])
        to_remove = [d for d in custom_dirs if val in d]
        if to_remove:
            for d in to_remove:
                custom_dirs.remove(d)
                print(f"Removed custom directory '{d}'.")
            cfg["custom_directories"] = custom_dirs
            save_user_config(cfg)
        else:
            print(f"No custom directory matching '{val}' found.")

    elif action == "list":
        cmd_list_dirs(args)

def cmd_add_dir(args):
    cfg = load_user_config()
    p = Path(args.path).expanduser().resolve()
    if not p.exists():
        print(f"Error: Directory path '{p}' does not exist.", file=sys.stderr)
        sys.exit(1)

    custom_dirs = cfg.get("custom_directories", [])
    p_str = str(p)
    if p_str not in custom_dirs:
        custom_dirs.append(p_str)
        cfg["custom_directories"] = custom_dirs
        save_user_config(cfg)
        print(f"\033[1;32m✓ Successfully added custom storage directory:\033[0m {p_str}")
    else:
        print(f"Directory '{p_str}' is already configured for backup.")

def cmd_remove_dir(args):
    cfg = load_user_config()
    custom_dirs = cfg.get("custom_directories", [])
    val = args.path.strip()
    to_remove = [d for d in custom_dirs if val in d]
    if to_remove:
        for d in to_remove:
            custom_dirs.remove(d)
            print(f"\033[1;32m✓ Removed custom directory:\033[0m {d}")
        cfg["custom_directories"] = custom_dirs
        save_user_config(cfg)
    else:
        print(f"No custom directory matching '{val}' found.")

def cmd_list_dirs(args):
    active_targets = get_active_targets()
    cfg = load_user_config()

    print("\n\033[1mConfigured Backup Targets & Storage Directories:\033[0m")
    print("=" * 70)
    print(f"{'Target ID':<15} {'Name / Description':<30} {'Directory Path'}")
    print("-" * 70)

    for target_id, info in active_targets.items():
        print(f"{target_id:<15} {info['name']:<30} {info['path']}")

    print("=" * 70 + "\n")

def cmd_backup(args):
    active_targets = get_active_targets()

    if args.target == "all":
        targets_to_run = active_targets
    elif args.target in active_targets:
        targets_to_run = {args.target: active_targets[args.target]}
    else:
        print(f"Target '{args.target}' not enabled. Available active targets: {list(active_targets.keys())}", file=sys.stderr)
        sys.exit(1)

    token = get_valid_access_token() if not args.local_only else None

    if not args.local_only and not token:
        print("Authentication required for Google Drive. Run 'agy-backup auth' first (or use --local-only).", file=sys.stderr)
        sys.exit(1)

    folder_id = get_or_create_backup_folder() if token else None

    for target_id, target_info in targets_to_run.items():
        print(f"\n=======================================================")
        print(f" Processing Backup Target: \033[1;34m{target_info['name'].upper()}\033[0m")
        print(f"=======================================================")

        changed, current_hashes = has_target_changed(target_id, target_info)

        if not changed and not args.force:
            print(f"\033[1;32m✓ No changes detected in {target_info['name']} since last backup.\033[0m Backup instance is up to date.")
            continue

        if args.force:
            print(f"Force flag set. Re-building {target_info['name']} backup...")

        archive_path, sha256_path, sha256_hex = create_target_archive(target_id, target_info, TEMP_DIR)

        res_file_id = ""
        if token and folder_id:
            print(f"Syncing {target_info['name']} backup instance to Google Drive...")
            res_archive = upload_or_update_file(archive_path, folder_id, description=f"{target_info['name']} User Data Backup (SHA256: {sha256_hex})")
            upload_or_update_file(sha256_path, folder_id, description=f"SHA256 checksum for {archive_path.name}")
            action = res_archive.get("_action", "Synced")
            res_file_id = res_archive.get("id", "")
            print(f"\033[1;32m✓ {action} {target_info['name']} backup instance on Google Drive!\033[0m (File ID: {res_file_id})")

        if args.local_dir:
            local_dest = Path(args.local_dir).expanduser()
            local_dest.mkdir(parents=True, exist_ok=True)
            dest_archive = local_dest / archive_path.name
            dest_sha256 = local_dest / sha256_path.name
            shutil.copy2(archive_path, dest_archive)
            shutil.copy2(sha256_path, dest_sha256)
            print(f"\033[1;32m✓ Saved local backup copy to:\033[0m {dest_archive}")

        update_manifest_entry(target_id, current_hashes, sha256_hex, res_file_id)

    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print("\n\033[1;32m★ Universal backup sync sequence completed!\033[0m")

def cmd_list(args):
    token = get_valid_access_token()
    if not token:
        print("Authentication required. Run 'agy-backup auth' first.", file=sys.stderr)
        sys.exit(1)

    folder_id = get_or_create_backup_folder()
    files = list_backups(folder_id)
    archives = [f for f in files if f["name"].endswith(".tar.gz")]

    if not archives:
        print("No backups found in Google Drive (/AGY_Backups).")
        return

    print("\n\033[1mAvailable Backups on Google Drive:\033[0m")
    print("=" * 75)
    print(f"{'#':<3} {'Backup Name':<35} {'Size (MB)':<10} {'Created Date':<20} {'File ID'}")
    print("-" * 75)

    for idx, f in enumerate(archives, 1):
        size_bytes = int(f.get("size", 0))
        size_mb = f"{size_bytes / (1024*1024):.2f}"
        created = f.get("createdTime", "")[:19].replace("T", " ")
        print(f"{idx:<3} {f['name']:<35} {size_mb:<10} {created:<20} {f['id']}")
    print("=" * 75 + "\n")

def cmd_restore(args):
    active_targets = get_active_targets()
    target_id = args.target if args.target in active_targets else "agy"
    target_info = active_targets.get(target_id, {"name": target_id.upper(), "path": HOME})

    if args.local_file:
        archive_path = Path(args.local_file).expanduser()
        if not archive_path.exists():
            print(f"Error: Local backup file not found: {archive_path}", file=sys.stderr)
            sys.exit(1)
        
        print(f"\033[1;33mPreparing to restore {target_info['name']} from local file:\033[0m {archive_path}")
        if not args.yes:
            confirm = input("Are you sure you want to proceed with restore? [y/N]: ").strip().lower()
            if confirm != "y":
                print("Restore operation cancelled.")
                return

        create_pre_restore_snapshot()
        restore_target_archive(target_id, target_info, archive_path)
        print(f"\n\033[1;32m★ Local restoration of {target_info['name']} complete!\033[0m")
        return

    token = get_valid_access_token()
    if not token:
        print("Authentication required. Run 'agy-backup auth' first.", file=sys.stderr)
        sys.exit(1)

    folder_id = get_or_create_backup_folder()
    files = list_backups(folder_id)
    archives = [f for f in files if f["name"].endswith(".tar.gz")]

    if not archives:
        print("Error: No backups found on Google Drive to restore.", file=sys.stderr)
        sys.exit(1)

    target_file = None

    if args.backup_id:
        if args.backup_id.isdigit():
            idx = int(args.backup_id) - 1
            if 0 <= idx < len(archives):
                target_file = archives[idx]
        else:
            for f in archives:
                if f["id"] == args.backup_id or f["name"] == args.backup_id:
                    target_file = f
                    break
    else:
        matching_archives = [f for f in archives if f["name"].startswith(f"{target_id}_backup")]
        target_file = matching_archives[0] if matching_archives else archives[0]

    if not target_file:
        print(f"Error: Specified backup '{args.backup_id}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"\033[1;33mPreparing to restore {target_info['name']} from Google Drive:\033[0m {target_file['name']} ({target_file['id']})")
    
    if not args.yes:
        confirm = input("Are you sure you want to proceed with restore? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Restore operation cancelled.")
            return

    create_pre_restore_snapshot()

    print("\nDownloading archive from Google Drive...")
    dl_dir = TEMP_DIR / "restore_dl"
    dl_dir.mkdir(parents=True, exist_ok=True)
    
    archive_path = dl_dir / target_file["name"]
    download_file(target_file["id"], archive_path)

    sha256_filename = f"{target_file['name']}.sha256"
    sha256_file_obj = next((f for f in files if f["name"] == sha256_filename), None)
    sha256_path = dl_dir / sha256_filename
    
    if sha256_file_obj:
        download_file(sha256_file_obj["id"], sha256_path)
        if not verify_checksum(archive_path, sha256_path):
            print("\033[1;31mChecksum verification failed! Aborting restore for safety.\033[0m", file=sys.stderr)
            sys.exit(1)

    restore_target_archive(target_id, target_info, archive_path)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print(f"\n\033[1;32m★ Restoration of {target_info['name']} complete!\033[0m")

def cmd_rollback(args):
    success = rollback_snapshot()
    if not success:
        sys.exit(1)

def cmd_status(args):
    tokens = load_tokens()
    creds = load_credentials()
    active_targets = get_active_targets()

    print("\n\033[1mAGY Universal Cloud Backup Status\033[0m")
    print("=" * 60)
    print(f"Active Backup Targets & Storage Directories:")
    for name, info in active_targets.items():
        print(f"  - {name:<12} ({info['name']}): {info['path']}")
    
    print(f"\nClient ID Configured: {'Yes' if creds.get('client_id') else 'No'}")
    
    if tokens:
        exp = tokens.get("expires_at", 0)
        valid = "Valid" if exp > time.time() else "Expired (Will refresh on next command)"
        print(f"Authentication Token: {valid}")
    else:
        print("Authentication Token: None (Not authenticated)")

    bak_snapshot = HOME / ".gemini" / "antigravity-cli.pre-restore.bak"
    print(f"Local Safety Snapshot: {'Present' if bak_snapshot.exists() else 'None'}")
    print("=" * 60 + "\n")

def main():
    parser = argparse.ArgumentParser(prog="agy-backup", description="Universal CLI Agent & Termux User Data Cloud Backup Tool")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Auth
    p_auth = subparsers.add_parser("auth", help="Authenticate with Google Drive OAuth2")
    p_auth.add_argument("--client-id", help="Google OAuth Client ID")
    p_auth.add_argument("--client-secret", help="Google OAuth Client Secret")

    # Config / Directory Manager
    p_config = subparsers.add_parser("config", help="Interactive backup configuration & CLI agent selector wizard")
    
    p_add_dir = subparsers.add_parser("add-dir", help="Add a custom storage directory for backup")
    p_add_dir.add_argument("path", help="Directory path to add to backup configuration")

    p_remove_dir = subparsers.add_parser("remove-dir", help="Remove a custom storage directory")
    p_remove_dir.add_argument("path", help="Directory path or substring to remove")

    p_list_dirs = subparsers.add_parser("list-dirs", help="List all active backup targets & directories")

    # Backup
    p_backup = subparsers.add_parser("backup", help="Incremental sync of user data to Google Drive or local directory")
    p_backup.add_argument("-t", "--target", default="all", help="Target component or custom directory to backup (Default: all)")
    p_backup.add_argument("-l", "--local-dir", help="Manual local destination directory for backup archives")
    p_backup.add_argument("--local-only", action="store_true", help="Perform local directory backup only without cloud upload")
    p_backup.add_argument("-f", "--force", action="store_true", help="Force re-backup even if no file changes were detected")

    # List
    p_list = subparsers.add_parser("list", help="List backups on Google Drive")

    # Restore
    p_restore = subparsers.add_parser("restore", help="Restore AGY / Gemini / Termux user data from Google Drive or local archive")
    p_restore.add_argument("-t", "--target", default="agy", help="Target component to restore (Default: agy)")
    p_restore.add_argument("backup_id", nargs="?", help="Backup file ID, filename, or list index # (Default: latest)")
    p_restore.add_argument("--local-file", help="Restore directly from a local archive file path")
    p_restore.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompt")

    # Rollback
    p_rollback = subparsers.add_parser("rollback", help="Emergency rollback to pre-restore local safety snapshot")

    # Status
    p_status = subparsers.add_parser("status", help="Show authentication & backup status")

    args = parser.parse_args()

    if args.command == "auth":
        cmd_auth(args)
    elif args.command == "config":
        cmd_config(args)
    elif args.command == "add-dir":
        cmd_add_dir(args)
    elif args.command == "remove-dir":
        cmd_remove_dir(args)
    elif args.command == "list-dirs":
        cmd_list_dirs(args)
    elif args.command == "backup":
        cmd_backup(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "restore":
        cmd_restore(args)
    elif args.command == "rollback":
        cmd_rollback(args)
    elif args.command == "status":
        cmd_status(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
