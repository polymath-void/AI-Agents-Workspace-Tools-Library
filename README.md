# AI Agents Workspace Tools Library ⚡

[![Build & Test Status](https://img.shields.io/badge/tests-18%2F18%20passing-brightgreen.svg)](#-test-suite--verification)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Android%20Termux-orange.svg)](#-system-compatibility)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/LICENSE)
[![Zero Overhead](https://img.shields.io/badge/overhead-zero--resource-purple.svg)](#-zero-resource-philosophy)

> **The definitive zero-resource, high-throughput autonomous task execution and workspace context library for AI agents, developers, and mobile-native workflows.**

---

## 📖 Table of Contents
1. [Overview](#-overview)
2. [SEO Keywords & Technology Domains](#-technology-domains--seo-indexing)
3. [Zero-Resource Philosophy](#-zero-resource-philosophy)
4. [Complete 18-Tool Catalog](#-complete-18-tool-catalog)
   - [Autonomous Task Completion Suite](#-autonomous-task-completion-suite)
   - [Workspace Context & Discovery Suite](#-workspace-context--discovery-suite)
5. [Quickstart & Installation](#-quickstart--installation)
6. [Benchmarking & Performance](#-benchmarking--performance)
7. [System Compatibility & Termux Integration](#-system-compatibility)
8. [Citation & Academic Reference](#-citation)
9. [License](#-license)

---

## 🌟 Overview

The **AI Agents Workspace Tools Library** is an end-to-end suite designed to eliminate manual analysis loops, minimize context token consumption, and enable autonomous agents to execute complex software tasks with complete zero-overhead efficiency.

Whether executing cross-language JNI contract validation, performing atomic multi-file refactoring, repairing Android Gradle build configurations, managing persistent memory state across sessions, or packaging signed extension bundles, this ecosystem provides immediate deterministic capabilities.

---

## 🔍 Technology Domains & SEO Indexing

`ai-agents` • `autonomous-workflows` • `workspace-context` • `agentic-coding` • `termux-android` • `jetpack-compose-scaffolding` • `jni-contract-validation` • `self-healing-builds` • `zero-token-overhead` • `multi-agent-choreography` • `code-refactoring` • `benchmark-latency`

---

## 💡 Zero-Resource Philosophy

1. **Sub-100ms Invocations**: Lightweight Python/C wrappers designed to run within strict mobile CPU/battery constraints.
2. **Selective Noise-Free Parsing**: Bypasses heavy build artifacts (`.git`, `node_modules`, `build`, `.gradle`) automatically.
3. **Deterministic Receipts**: Outputs formatted execution receipts and JSON payloads, zeroing token waste for LLM agents.

---

## 📦 Complete 18-Tool Catalog

### 🚀 Autonomous Task Completion Suite

| Tool | Category | Operational Scope | Quick Command Example |
| :--- | :--- | :--- | :--- |
| **`wc-task-exec`** | Task Pipeline | End-to-end multi-phase validation pipeline & task receipt generation. | `wc-task-exec "Verify Launcher" .` |
| **`wc-code-mod`** | Refactoring | Atomic multi-file pattern replacement, import injection & rollback backups. | `wc-code-mod replace 'old' 'new' . -e kt` |
| **`wc-build-doctor`**| Self-Healing | Diagnoses Android targetSdk, Compose compiler, and 16KB native page alignments. | `wc-build-doctor . --fix` |
| **`wc-bundle-packer`**| Packaging | Compiles `.piuu` extension bundles, validates manifests, and calculates SHA-256 hashes. | `wc-bundle-packer pack ./ext dist/ext.piuu` |
| **`wc-benchmark`** | Performance | Benchmark auditor with configurable max-latency budgets and scorecards. | `wc-benchmark ./bin/wc-scan . -n 3 -t 0.5` |
| **`wc-agent-memory`**| Memory & State | SQLite store for agent decisions, persistent state, and workspace rollback snapshots. | `wc-agent-memory set 'key' 'value'` |
| **`wc-contract-check`**| Contracts | Cross-language ABI/IPC contract validator (Kotlin JNI <-> POSIX C <-> Electron). | `wc-contract-check .` |
| **`wc-scaffold`** | Scaffolding | Boilerplate generator for Jetpack Compose components and Kotlin StateFlow repos. | `wc-scaffold compose UIModal.kt` |
| **`wc-crash-doctor`**| Diagnostics | Parses Android logcat dumps, SIGSEGV crashes, and stacktraces to root-cause lines. | `wc-crash-doctor crash.log` |

---

### 🔍 Workspace Context & Discovery Suite

| Tool | Category | Operational Scope | Quick Command Example |
| :--- | :--- | :--- | :--- |
| **`wc-tool-registry`**| Discovery | Instant interactive catalog of all tools with recipes. | `wc-tool-registry` |
| **`wc-search`** | Search | Lightning-fast regex & symbol finder skipping cache/build directories. | `wc-search 'theme' . -e kt` |
| **`wc-deps`** | Dependencies| Multi-manifest inspector for Android Gradle, NPM, Python, and Rust. | `wc-deps .` |
| **`wc-git-sync`** | Git / CI | Synchronizes branch flows (`main` ↔ `master`) and audits clean tree status. | `wc-git-sync sync . main master` |
| **`wc-termux-env`** | Telemetry | Hardware RAM/CPU stats, verified toolchains, and automatic shebang fixer. | `wc-termux-env status` |
| **`wc-scan`** | Architecture| Recursive directory mapper generating structured JSON tree metadata. | `wc-scan .` |
| **`wc-analyze`** | Quality | Computes cyclomatic complexity, LOC metrics, and structural counts. | `wc-analyze summary .` |
| **`wc-manage`** | Sanitization| Workspace cleaner with `--dry-run` safety guards. | `wc-manage sanitize . '*.tmp' -d` |
| **`wc-monitor`** | Health | Continuous anomaly auditor for complexity, size, and forbidden patterns. | `wc-monitor .` |

---

## ⚡ Quickstart & Installation

```bash
# Clone or navigate to the repository
cd ~/AI-Agents-Workspace-Tools-Library

# Make all tool binaries executable
chmod +x bin/*

# Export to PATH (optional, for direct CLI invocation)
export PATH="$HOME/AI-Agents-Workspace-Tools-Library/bin:$PATH"

# Discover available tools
wc-tool-registry
```

---

## 🧪 Test Suite & Verification

The suite includes 18 unit tests validating every tool and core library module:

```bash
python3 -m unittest tests/test_all.py
```
```
..................
----------------------------------------------------------------------
Ran 18 tests in 1.743s

OK
```

---

## 📱 System Compatibility

- **Android Termux**: Fully supported with `/data/data/com.termux/files/usr/bin/env` shebangs and low-RAM footprint.
- **Linux / POSIX**: Fully POSIX compliant, requiring only standard Python 3.9+.
- **Architectures**: ARM64 (`aarch64`), x86_64, ARMv7.

---

## 📚 Citation

If you use this library or its tool specifications in academic research, agent evaluations, or software documentation, please cite:

```bibtex
@software{ai_agents_workspace_tools_2026,
  author = {Polymath, Void and Antigravity Agentic Systems},
  title = {{AI Agents Workspace Tools Library: Autonomous Zero-Resource Task Execution and Workspace Context Ecosystem}},
  url = {https://github.com/polymath-void/AI-Agents-Workspace-Tools-Library},
  version = {1.0.0},
  year = {2026}
}
```

---

## 📄 License

Licensed under the [Apache License, Version 2.0](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/LICENSE).
