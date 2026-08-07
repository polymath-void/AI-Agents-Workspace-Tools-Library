# Agentic Operational Guide: Tool Organization & Categorized Use Cases (`AGENTS.md`)

> **Document Classification**: AI Agent Operational Specification  
> **System**: AI Agents Workspace Tools Library  
> **Standard Citation**: Polymath et al., *Autonomous Zero-Resource Task Execution and Workspace Context Ecosystem*, 2026. [`CITATION.cff`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/CITATION.cff)  
> **Target Audience**: Autonomous AI Agents (Antigravity AGY, Gemini CLI, Hermes), Multi-Agent Mesh Systems, and Human Orchestrators.

---

## 🧭 Executive Summary for Autonomous Agents

This document provides a cognitive taxonomy and decision matrix for AI agents operating within software workspaces. Rather than executing unbounded shell commands or consuming tokens on broad file scans, agents **must classify their operational intent** into one of the **8 Core Functional Categories** below and select the specialized tool that zero-outs token and execution overhead.

---

## 🗺️ Functional Category Taxonomy

```
                                  ┌─────────────────────────────────────────────────────────┐
                                  │            AGENT TASK / PROBLEM STATEMENT               │
                                  └────────────────────────────┬────────────────────────────┘
                                                               │
        ┌───────────────────┬───────────────────┬──────────────┼──────────────┬───────────────────┬───────────────────┐
        │                   │                   │              │              │                   │                   │
 ┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐┌──────▼──────┐┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
 │ Category 0  │     │ Category 1  │     │ Category 2  ││ Category 3  ││ Category 4  │     │ Category 5  │     │ Category 6  │
 │ Agent Loop  │     │ Task Pipeline│    │ Code Mod &  ││ Contract &  ││ Build &     │     │ Memory &    │     │ Discovery & │
 │ & Autonomy  │     │ & Execution │     │ Scaffolding ││ Packaging   ││ Diagnostics │     │ State Store │     │ Inspection  │
 └─────────────┘     └─────────────┘     └─────────────┘└─────────────┘└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 📂 Category 0: Agent Self-Healing Loop & Autonomy

### Purpose & Trigger Condition
Use this category to run agent commands inside a protected wrapper with pre-flight environment checks, automatic rollback snapshot checkpoints, and deterministic error healing.

### Tools & Cited Use Cases

#### 1. `wc-agent-loop`
* **Citation**: § 0.1 *Autonomous Self-Healing Loop Engine with Checkpoint Rollback*
* **Trigger Condition**: When executing high-risk commands (e.g. Git push, build runs, multi-file refactoring).
* **Operational Recipe**:
  ```bash
  # Execute task inside self-healing loop with rollback safety
  bin/wc-agent-loop git push origin main
  bin/wc-agent-loop ./bin/wc-task-exec "Verify Feature" .
  ```

#### 2. `wc-agent-probe`
* **Citation**: § 0.2 *Internal Agent Environment Diagnostic Probe*
* **Trigger Condition**: When troubleshooting agent execution failures, missing PATH binaries, or Git 403 errors.
* **Operational Recipe**:
  ```bash
  # Audit agent runtime health
  bin/wc-agent-probe

  # Output structured JSON for agent processing
  bin/wc-agent-probe --json
  ```

#### 3. `wc-error-healer`
* **Citation**: § 0.3 *Deterministic Self-Healing Error Remediation*
* **Trigger Condition**: When commands fail with Git 403 permission errors, missing Termux shebangs, or SQLite WAL locks.
* **Operational Recipe**:
  ```bash
  # Auto-configure tools in shell PATH
  bin/wc-error-healer --fix-path

  # Auto-remediate a captured error message
  bin/wc-error-healer "Permission to polymath-void/repo.git denied to user"
  ```

---

## 📂 Category 1: Autonomous Pipeline & Task Execution

### Purpose & Trigger Condition
Use this category when the agent is assigned a multi-step task and needs to run pre-flight environment checks, verify dependency trees, validate health, execute unit tests, and emit a structured execution receipt.

### Tools & Cited Use Cases

#### 1. `wc-task-exec`
* **Citation**: § 1.1 *Deterministic Task Receipts in Autonomous Systems*
* **Trigger Condition**: When finalizing a coding task or starting a major milestone validation.
* **Operational Recipe**:
  ```bash
  # Execute full multi-phase verification pipeline
  bin/wc-task-exec "Verify Launcher Refactoring" /path/to/project
  ```

#### 2. `wc-benchmark`
* **Citation**: § 1.2 *Latency-Constrained Mobile Process Execution*
* **Trigger Condition**: When optimizing performance or verifying that changes do not cause battery/CPU regressions on Termux.
* **Operational Recipe**:
  ```bash
  # Verify command executes within 500ms budget across 3 runs
  bin/wc-benchmark bin/wc-search "MainActivity" . -n 3 -t 0.5
  ```

---

## 📂 Category 2: Atomic Code Modification & Scaffolding

### Purpose & Trigger Condition
Use this category when the agent needs to generate new components or modify code across multiple project files simultaneously without manual regex scripts or risking file corruption.

### Tools & Cited Use Cases

#### 1. `wc-code-mod`
* **Citation**: § 2.1 *Atomic Multi-File Transformations with Automatic Rollback*
* **Trigger Condition**: Project-wide method renaming, parameter updating, or import statement injection.
* **Operational Recipe**:
  ```bash
  # Preview replacement without modifying disk
  bin/wc-code-mod replace "oldApi()" "newApi()" . -e kt,java --dry-run

  # Apply replacement with automatic atomic backup in .wc_backups/
  bin/wc-code-mod replace "oldApi()" "newApi()" . -e kt,java

  # Inject missing import across all Kotlin UI files
  bin/wc-code-mod import "import com.piuu.launcher.ui.theme.*" app/src -e kt
  ```

#### 2. `wc-scaffold`
* **Citation**: § 2.2 *Zero-Overhead Component Generation for Jetpack Compose*
* **Trigger Condition**: Creating new UI cards, modals, StateFlow repositories, or extension templates.
* **Operational Recipe**:
  ```bash
  # Scaffold a Jetpack Compose modal
  bin/wc-scaffold compose app/src/main/java/com/piuu/launcher/ui/components/WallpaperSheet.kt

  # Scaffold a Kotlin StateFlow repository
  bin/wc-scaffold repo app/src/main/java/com/piuu/launcher/repository/GridRepository.kt

  # Scaffold a standalone .piuu extension project
  bin/wc-scaffold extension ./clock-widget --name "Digital Clock" --version "1.0.0"
  ```

---

## 📂 Category 3: Cross-Language Contracts & Packaging

### Purpose & Trigger Condition
Use this category when working on hybrid systems crossing Kotlin (JNI), POSIX C native shared libraries (`.so`), Electron Desktop IPC (`contextBridge`), or `.piuu` extension zip bundles.

### Tools & Cited Use Cases

#### 1. `wc-contract-check`
* **Citation**: § 3.1 *Cross-Language ABI Interface Verification*
* **Trigger Condition**: After editing Kotlin `external fun` declarations or native C functions in `libpiuu_core.c`.
* **Operational Recipe**:
  ```bash
  # Check for unexported JNI methods or missing C implementations
  bin/wc-contract-check ~/repo/Piuu-Unified-Launcher-Android
  ```

#### 2. `wc-bundle-packer`
* **Citation**: § 3.2 *Cryptographic Extension Packaging and Integrity Verification*
* **Trigger Condition**: Compiling extension packages into `.piuu` zip bundles with SHA-256 hashes.
* **Operational Recipe**:
  ```bash
  # Pack extension directory into a validated .piuu bundle
  bin/wc-bundle-packer pack ./my-extension dist/extension.piuu --name "Weather Widget"

  # Verify bundle manifest schema and checksum integrity
  bin/wc-bundle-packer verify dist/extension.piuu
  ```

---

## 📂 Category 4: Build Healing & Crash Diagnostics

### Purpose & Trigger Condition
Use this category when a build fails, an app crashes with a SIGSEGV / ANR, or Gradle fails with cryptic stack traces.

### Tools & Cited Use Cases

#### 1. `wc-build-doctor`
* **Citation**: § 4.1 *Self-Healing Build Systems for Android and Gradle*
* **Trigger Condition**: Gradle compilation failures, targetSdk mismatches, or missing 16KB page alignment linker flags.
* **Operational Recipe**:
  ```bash
  # Diagnose Android build health and configuration
  bin/wc-build-doctor ~/repo/Piuu-Unified-Launcher-Android

  # Apply automatic repairs to build scripts and shebangs
  bin/wc-build-doctor ~/repo/Piuu-Unified-Launcher-Android --fix
  ```

#### 2. `wc-crash-doctor`
* **Citation**: § 4.2 *Automated Stacktrace and Logcat Root-Cause Isolation*
* **Trigger Condition**: Analyzing crash logs or runtime exceptions.
* **Operational Recipe**:
  ```bash
  # Analyze crash dump file
  bin/wc-crash-doctor crash.log

  # Pipe live logcat stream directly into diagnostic parser
  logcat -d | bin/wc-crash-doctor
  ```

---

## 📂 Category 5: Persistent Agent Memory & Rollback State

### Purpose & Trigger Condition
Use this category to store architectural decisions, user preferences, and full workspace backup snapshots across turns.

### Tools & Cited Use Cases

#### 1. `wc-agent-memory`
* **Citation**: § 5.1 *Long-Term Agent State Persistence in SQLite*
* **Trigger Condition**: Storing user rules, task milestones, or creating rollback safety checkpoints before high-risk changes.
* **Operational Recipe**:
  ```bash
  # Store agent preference / user directive
  bin/wc-agent-memory set "perf_priority" "Keep RAM under 150MB" -c "rules"

  # Retrieve stored preference
  bin/wc-agent-memory get "perf_priority"

  # Create a named directory rollback snapshot before refactoring
  bin/wc-agent-memory snapshot ~/repo/Piuu-Unified-Launcher-Android -t "pre-compose-v2"

  # List existing snapshots
  bin/wc-agent-memory snapshots
  ```

---

## 📂 Category 6: Discovery, Search & Workspace Context

### Purpose & Trigger Condition
Use this category when the agent needs immediate answers about workspace topology, code symbols, dependencies, or tool capabilities without loading large files into context.

### Tools & Cited Use Cases

#### 1. `wc-tool-registry`
* **Citation**: § 6.1 *Zero-Resource Meta-Tool Capability Discovery*
* **Trigger Condition**: Agent needs to check which tool or parameter to use.
* **Operational Recipe**:
  ```bash
  bin/wc-tool-registry
  bin/wc-tool-registry "refactoring"
  ```

#### 2. `wc-search`
* **Citation**: § 6.2 *Noise-Filtered Codebase Symbol Discovery*
* **Trigger Condition**: Searching for symbols, classes, or patterns across code files while automatically excluding `.git`, `node_modules`, and `build`.
* **Operational Recipe**:
  ```bash
  bin/wc-search "wallpaperTransparency" . -e kt,xml -C 2
  ```

#### 3. `wc-deps`
* **Citation**: § 6.3 *Multi-Ecosystem Manifest Inspection*
* **Trigger Condition**: Auditing Gradle, NPM, Python, or Rust dependencies.
* **Operational Recipe**:
  ```bash
  bin/wc-deps .
  ```

#### 4. `wc-scan` & `wc-analyze`
* **Citation**: § 6.4 *Structural Metrics and Cyclomatic Complexity Analysis*
* **Trigger Condition**: Mapping workspace depth or identifying high-complexity hotspots.
* **Operational Recipe**:
  ```bash
  bin/wc-scan .
  bin/wc-analyze summary .
  ```

---

## 📂 Category 7: System Telemetry & Workspace Maintenance

### Purpose & Trigger Condition
Use this category for hardware telemetry on mobile/Termux environments and clean sanitization of build caches.

### Tools & Cited Use Cases

#### 1. `wc-termux-env`
* **Citation**: § 7.1 *Hardware Telemetry and Script Environment Harmonization*
* **Trigger Condition**: Verifying available RAM/CPU before heavy tasks and repairing script shebangs.
* **Operational Recipe**:
  ```bash
  bin/wc-termux-env status
  bin/wc-termux-env fix-shebangs ./scripts
  ```

#### 2. `wc-manage` & `wc-monitor`
* **Citation**: § 7.2 *Protected Workspace Sanitization and Anomaly Auditing*
* **Trigger Condition**: Purging temporary files with safety bounds and monitoring large file additions.
* **Operational Recipe**:
  ```bash
  bin/wc-manage sanitize . "*.tmp" "*.bak" --dry-run
  bin/wc-monitor .
  ```

#### 3. `wc-git-sync`
* **Citation**: § 7.3 *Multi-Branch Flow Coordination*
* **Trigger Condition**: Fast-forwarding branch flows (e.g. `main` ↔ `master`) and checking tree cleanliness.
* **Operational Recipe**:
  ```bash
  bin/wc-git-sync sync . main master
  ```

---

## 📊 Quick Category & Tool Selection Matrix

| Operational Goal | Recommended Category | Primary Tool | Fallback / Complementary Tool |
| :--- | :--- | :--- | :--- |
| **Run Command with Auto-Heal**| Cat 0: Agent Autonomy | `wc-agent-loop` | `wc-agent-probe`, `wc-error-healer` |
| **Verify Multi-Step Task** | Cat 1: Pipeline | `wc-task-exec` | `wc-benchmark` |
| **Refactor Code Across Files**| Cat 2: Code Mod | `wc-code-mod` | `wc-scaffold` |
| **Verify JNI / IPC Contracts**| Cat 3: Contracts | `wc-contract-check` | `wc-bundle-packer` |
| **Fix Build / Debug Crash** | Cat 4: Diagnostics | `wc-build-doctor` | `wc-crash-doctor` |
| **Save Checkpoint / Prefs** | Cat 5: Memory | `wc-agent-memory` | `wc-manage` |
| **Find Symbols / Code** | Cat 6: Context | `wc-search` | `wc-deps` |
| **Check RAM / Clean Caches** | Cat 7: Telemetry | `wc-termux-env` | `wc-manage` |

---

## 📚 Academic & System Citation

To reference this categorization and tool operational schema:

```bibtex
@article{polymath2026agentsworkspace,
  author = {Polymath, Void and Antigravity Agentic Systems},
  title = {A Categorized Operational Matrix for Zero-Resource Autonomous Agent Problem Solving},
  journal = {Antigravity Agentic System Specifications},
  year = {2026},
  volume = {1},
  number = {4},
  pages = {1--21}
}
```
