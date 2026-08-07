# `wc-electron-runner`

## Overview
`wc-electron-runner` is a headless Electron desktop application and plugin runner harness. It audits `BrowserWindow` security configurations (checking `contextIsolation`, `nodeIntegration`, and `sandbox`), verifies IPC channel contracts between `main.js` and `preload.js`, and simulates `.piuu` extension bundle loading.

## Category & Classification
- **Category**: `03_code_refactoring` (Code Quality & Complexity)
- **Runtime**: Pure Python 3 & AST Pattern Matcher
- **Dependencies**: None (Standard Library)

## CLI Usage
```bash
wc-electron-runner <audit-security|audit-ipc|simulate-bundle> [target]
```

### Subcommands
- `audit-security <main.js>`: Scans Electron constructor settings for common security flaws.
- `audit-ipc <main.js> [-p preload.js]`: Matches IPC channels across process boundaries to detect unhandled invokes.
- `simulate-bundle <bundle.piuu>`: Validates `.piuu` extension bundle manifests and UI preview resources.

## Associated Skills
- `piuu-electron-desktop-studio`
- `piuu-compose-launcher-ui`

## Example Agent Invocation
```bash
wc-electron-runner audit-security ~/repo/piuu-studio-desktop/src/main.js
```
