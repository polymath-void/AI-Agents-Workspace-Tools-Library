# AI Agents Workspace Tools Library ⚡

[![Build & Test Status](https://img.shields.io/badge/tests-33%2F33%20passing-brightgreen.svg)](#-test-suite--verification)
[![Tools Count](https://img.shields.io/badge/tools-41%20tools-blue.svg)](#-complete-41-tool-catalog)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Android%20Termux-orange.svg)](#-system-compatibility)
[![Zero Overhead](https://img.shields.io/badge/overhead-zero--resource-purple.svg)](#-zero-resource-philosophy)

> **The definitive zero-resource, self-healing, high-throughput autonomous task execution, JSON data transformation, and workspace context library for AI agents, multi-agent swarms, and mobile-native workflows.**

---

## 📂 Search-Friendly Category Layout

Tools are cleanly partitioned into 4 search-friendly category directories under `categories/` with direct execution links in `bin/`:

```
AI-Agents-Workspace-Tools-Library/
├── bin/                                # 41 CLI tools
├── categories/
│   ├── 01_json_data/                   # 12 JSON & tabular transformation tools
│   ├── 02_workflow_swarm/              # 10 Swarm orchestration & DAG tools
│   ├── 03_code_refactoring/            # 6 AST analysis & scaffolding tools
│   └── 04_system_runtime/              # 13 System, build & diagnostic tools
└── lib/
    ├── json/                           # JSON suite & prompt processors
    ├── workflow/                       # Swarm dispatcher & context managers
    ├── py/                             # AST analyzers & scaffolders
    └── system/                         # Diagnostics, packagers & verifiers
```

---

## 🛠️ Complete 41-Tool Categorized Catalog

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

### 💻 Category 03: Code Refactoring & AST Analysis (`categories/03_code_refactoring/`)
* **`wc-code-mod`**: Multi-file batch code modifier, regex replacer & import injector with rollback.
* **`wc-object-diff`**: Semantic object comparator, JSON schema differ & code symbol extractor.
* **`wc-search`**: Noise-free symbol and regex search ignoring build/cache directories.
* **`wc-contract-check`**: Cross-language contract verifier for Kotlin JNI $\leftrightarrow$ POSIX C exports.
* **`wc-scaffold`**: Component generator for Jetpack Compose UI and StateFlow repositories.
* **`wc-analyze`**: AST cyclomatic complexity, LOC, and function metrics profiler.

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

---

## 🧪 Test Suite & Verification

Run the unified regression test suite:
```bash
python3 -m unittest tests/test_all.py
```
**Result**:
```
Ran 33 tests in 4.85s
OK
```

---

## 📄 License
Apache-2.0 © 2026 Polymath-Void
