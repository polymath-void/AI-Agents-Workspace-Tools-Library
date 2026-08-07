# `wc-cloud-backup`

## Overview
`wc-cloud-backup` is an autonomous, battery-optimized disaster recovery and incremental backup engine designed for Android Termux, Antigravity CLI (AGY), and multi-agent development environments. It creates compressed tarballs, computes SHA-256 integrity digests, logs snapshots into SQLite, and generates manifests for Google Drive and cloud synchronizations.

## Category & Classification
- **Category**: `04_system_runtime` (Disaster Recovery & Backup)
- **Runtime**: Pure Python 3 & POSIX Tar
- **Dependencies**: None (Standard Library)

## CLI Usage
```bash
wc-cloud-backup <backup|list|status> [-t target] [-d dest] [--dry-run] [-f]
```

### Subcommands & Options
- `backup`: Scans target domain, compresses files into `.tar.gz`, records SHA-256 signature and outputs JSON manifest.
  - `-t, --target <agy|gemini|termux|all>`: Target directory scope (default: `agy`).
  - `-d, --dest <path>`: Custom destination directory for backup archives.
  - `--dry-run`: Performs file scanning and size computation without creating archives.
  - `-f, --force`: Forces archive creation even if no changes occurred since last snapshot.
- `list`: Lists all previous backup runs recorded in the local SQLite ledger.
- `status`: Displays database path and latest snapshot metadata.

## Associated Skills
- `termux-cloud-backup-assist`
- `agy-gdrive-backup`
- `termux-environment`

## Example Agent Invocation
```bash
wc-cloud-backup backup -t agy --dest ~/backups
```
