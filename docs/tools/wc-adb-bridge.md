# `wc-adb-bridge`

## Overview
`wc-adb-bridge` is a wireless ADB connection manager, device discovery agent, remote execution harness, and framebuffer screenshot capture utility for Android Termux and host systems.

## Category & Classification
- **Category**: `04_system_runtime` (Android & Termux System)
- **Runtime**: Pure Python 3 & Subprocess Bridge
- **Dependencies**: `adb` binary

## CLI Usage
```bash
wc-adb-bridge <devices|pair|connect|shell|screencap|telemetry> [args]
```

### Subcommands
- `devices`: Lists all connected USB and wireless ADB devices with product and model metadata.
- `pair <host:port> <code>`: Pairs with Android 11+ Wireless Debugging service.
- `connect <host:port>`: Connects to a paired wireless ADB endpoint.
- `shell "<command>" [-s serial]`: Executes shell command on remote target.
- `screencap <output.png> [-s serial]`: Takes instant framebuffer capture directly to local PNG file.
- `telemetry [-s serial]`: Extracts battery level, screen density, OS version, and CPU ABI.

## Associated Skills
- `phone-ssh-connect`
- `termux-environment`
- `piuu-compose-launcher-ui`

## Example Agent Invocation
```bash
wc-adb-bridge screencap launcher_preview.png
```
