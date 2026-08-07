# AI Agents Workspace Tools Library ⚡

[![Build & Test Status](https://img.shields.io/badge/tests-41%2F41%20passing-brightgreen.svg)](#-test-suite--verification)
[![Tools Count](https://img.shields.io/badge/tools-49%20tools-blue.svg)](#-complete-49-tool-catalog)
[![Profile Views](https://komarev.com/ghpvc/?username=polymath-void&color=blueviolet&style=flat-square&label=PROFILE+VIEWS)](https://github.com/polymath-void)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows%20(WSL)%20%7C%20Android%20(Termux)-orange.svg)](#-cross-platform--zero-resource-architecture)
[![Zero Overhead](https://img.shields.io/badge/overhead-zero--resource-purple.svg)](#-cross-platform--zero-resource-architecture)

> **The definitive zero-resource, self-healing, cross-platform autonomous task execution, JSON data transformation, and workspace context library for AI agents, multi-agent swarms, host computers, and mobile-native workflows.**

---

## 🌐 Cross-Platform & Zero-Resource Architecture

* **100% Pure Python 3 Standard Library**: Zero external pip dependencies. Every tool is built exclusively on Python's robust standard library (`ast`, `json`, `sqlite3`, `pathlib`, `re`, `subprocess`, `argparse`, `sys`, `os`).
* **Universal Portability**: Configured with universal `#!/usr/bin/env python3` shebangs. Runs seamlessly across:
  * 🖥️ **Host Workstations & Cloud** (Linux, macOS, Windows via WSL / Git Bash)
  * 📱 **Mobile Workspaces** (Android Termux)
* **Zero Native Binaries**: No compiled C/C++ ELF binaries or architecture-locked machine code—enabling instant execution without cross-compilation or root privileges.
* **Sub-100ms Latency**: Designed for autonomous AI loops and subagent orchestration with minimal RAM/CPU footprint.

---

## 🚀 Quick Start & Integration

### Option 1: Direct PATH Export (Recommended for Agents & CLI)
Clone the repository and add `bin/` to your environment's `PATH`:
```bash
git clone https://github.com/polymath-void/AI-Agents-Workspace-Tools-Library.git
cd AI-Agents-Workspace-Tools-Library
export PATH="$PWD/bin:$PATH"
```

### Option 2: Editable Python Package
Install in editable mode for system or virtualenv CLI access:
```bash
pip install -e .
```

---

## 📂 Search-Friendly Category Layout

Tools are cleanly partitioned into 4 search-friendly category directories under `categories/` with direct execution symlinks in `bin/` and core logic in `lib/`:

```
AI-Agents-Workspace-Tools-Library/
├── bin/                                # 49 executable CLI tools (universal python3)
├── categories/
│   ├── 01_json_data/                   # 13 JSON & tabular transformation tools
│   ├── 02_workflow_swarm/              # 12 Swarm orchestration & DAG tools
│   ├── 03_code_refactoring/            # 7 AST analysis & scaffolding tools
│   └── 04_system_runtime/              # 17 System, build & diagnostic tools
└── lib/
    ├── json/                           # JSON suite, schema generators & prompt processors
    ├── workflow/                       # Swarm dispatcher, context managers & skill packager
    ├── py/                             # AST analyzers, scaffolders & electron simulator
    └── system/                         # Cloud backups, ELF alignment, ADB bridge & kernel builder
```

---

## 🛠️ Complete 49-Tool Categorized Catalog

### 📊 Category 01: JSON & Data Processing Suite (`categories/01_json_data/`)
* **`wc-json-prompt`**: Unformatted prompt JSON extractor & heuristic syntax auto-repairer.
* **`wc-json-query`**: Dot/bracket JSONPath query and token minifier.
* **`wc-json-patch`**: Atomic in-place key patcher and deep object merger.
* **`wc-json-validate`**: Schema & required field validator.
* **`wc-json-format`**: JSON prettifier, ANSI colorizer, key sorter & dense minifier.
* **`wc-json-schema`**: Auto-infers standard JSON Schema Draft 7 from sample payloads.
* **`wc-json-flatten`**: Converts deep hierarchical objects to dot-notation keys and un-flattens back.
* **`wc-json-ndjson`**: High-throughput NDJSON (JSON Lines) streaming converter and line filter.
* **`wc-json-csv`**: Bidirectional JSON $\leftrightarrow$ CSV/TSV converter with auto-typing.
* **`wc-json-stats`**: Structural profiler computing depth, key count, byte volume, and token metrics.
* **`wc-json-filter`**: Predicate engine for querying collections (`==`, `!=`, `>`, `<`, `contains`, `startswith`).
* **`wc-json-mask`**: Security redactor that automatically masks API keys, tokens, and passwords.
* **`wc-agy-session`**: Antigravity AGY session transcript analyzer, token density counter & timeline exporter.

### 🐝 Category 02: Multi-Tasking & Swarm Workflows (`categories/02_workflow_swarm/`)
* **`wc-swarm-dispatch`**: Subagent necessity evaluator, dispatch spec generator & outcome aggregator.
* **`wc-workflow-context`**: Context isolation namespace & frame handoff bus between subagents.
* **`wc-task-dag`**: Dependency-aware multi-task DAG executor with worker pools.
* **`wc-agent-mesh`**: Multi-agent swarm role coordinator (`Architect`, `Implementer`, `Verifier`).
* **`wc-agent-channel`**: Persistent inter-agent Pub/Sub messaging bus.
* **`wc-resource-lock`**: Distributed mutex lock guarding files and databases against race conditions.
* **`wc-context-pack`**: Token density compressor and ANSI trace deduplicator.
* **`wc-agent-loop`**: Self-healing execution loop with pre-flight probes and rollback snapshots.
* **`wc-agent-probe`**: Internal diagnostic probe auditing PATH, auth, RAM, and Python engines.
* **`wc-error-healer`**: Deterministic error doctor for Git 403s, missing shebangs, and database locks.
* **`wc-skill-pack`**: SKILL.md linter, YAML frontmatter validator, dependency checker & `.skill` bundle packager.
* **`wc-hermes-adapter`**: Protocol bridge translating between Hermes JSON sessions and Antigravity AGY logs.

### 💻 Category 03: Code Refactoring & AST Analysis (`categories/03_code_refactoring/`)
* **`wc-code-mod`**: Multi-file batch code modifier, regex replacer & import injector with rollback.
* **`wc-object-diff`**: Semantic object comparator, JSON schema differ & code symbol extractor.
* **`wc-search`**: Noise-free symbol and regex search ignoring build/cache directories.
* **`wc-contract-check`**: Cross-language contract verifier for Kotlin JNI $\leftrightarrow$ POSIX C exports.
* **`wc-scaffold`**: Component generator for Jetpack Compose UI and StateFlow repositories.
* **`wc-analyze`**: AST cyclomatic complexity, LOC, and function metrics profiler.
* **`wc-electron-runner`**: Headless Electron security auditor, IPC bridge validator & plugin simulator.

### ⚙️ Category 04: System, Diagnostics & Build (`categories/04_system_runtime/`)
* **`wc-build-doctor`**: Android Gradle configuration auditor and 16KB page alignment verifier.
* **`wc-crash-doctor`**: Android logcat, stacktrace, and SIGSEGV exception isolator.
* **`wc-bundle-packer`**: `.piuu` extension compiler with manifest generation and SHA256 hashing.
* **`wc-benchmark`**: Battery-friendly latency and execution benchmark runner.
* **`wc-termux-env`**: Android/Termux hardware telemetry and compiler toolchain verifier.
* **`wc-git-sync`**: Multi-branch synchronizer (`main` $\leftrightarrow$ `master` unified flow).
* **`wc-deps`**: Multi-ecosystem dependency manifest analyzer (Gradle, NPM, Pip, Cargo).
* **`wc-scan`**: Resilient directory tree scanner and file metric aggregator.
* **`wc-manage`**: Safe workspace cleaner with protected root boundaries and dry-run previews.
* **`wc-monitor`**: Continuous workspace health auditor detecting anomalies and size violations.
* **`wc-agent-memory`**: Persistent SQLite storage for architectural rules and directory snapshots.
* **`wc-task-exec`**: Autonomous multi-phase task pipeline runner with receipt generation.
* **`wc-tool-registry`**: Interactive master tool catalog supporting keyword and JSON queries.
* **`wc-cloud-backup`**: Autonomous incremental snapshot creator, SHA-256 integrity ledger & cloud backup manager.
* **`wc-elf-align`**: Android 15/16 (API 36) 16KB page-alignment ELF binary analyzer & segment validator.
* **`wc-adb-bridge`**: Termux wireless ADB connection manager, device discovery & screencap capture tool.
* **`wc-kernel-builder`**: Android GKI Linux Kernel compilation manager, defconfig auditor & AnyKernel3 packager.

---

## 🧪 Test Suite & Verification

Run the unified regression test suite across all test modules:
```bash
python3 -m unittest discover tests
```
**Result**:
```
Ran 41 tests in 5.14s
OK
```

---

## 📄 License
Apache-2.0 © 2026 Polymath-Void
