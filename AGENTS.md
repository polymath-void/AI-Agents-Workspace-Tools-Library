# Agentic Operational Guide: Tool Organization & Categorized Use Cases (`AGENTS.md`)

> **Document Classification**: AI Agent Operational Specification  
> **System**: AI Agents Workspace Tools Library  
> **Standard Citation**: Polymath et al., *Autonomous Zero-Resource Task Execution and Workspace Context Ecosystem*, 2026. [`CITATION.cff`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/CITATION.cff)  
> **Target Audience**: Autonomous AI Agents (Antigravity AGY, Gemini CLI, Hermes), Multi-Agent Mesh Systems, and Human Orchestrators.

---

## 🧭 Executive Summary for Autonomous Agents

This document provides a cognitive taxonomy and decision matrix for AI agents operating within software workspaces. Rather than executing unbounded shell commands or consuming tokens on broad file scans, agents **must classify their operational intent** into one of the **9 Core Functional Categories** below and select the specialized tool that zero-outs token and execution overhead.

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
 │ Category 00 │     │ Category 0  │     │ Category 1  ││ Category 2  ││ Category 3  │     │ Category 4  │     │ Category 5  │
 │ Multi-Task  │     │ Agent Loop  │     │ Task Pipeline││ Code Mod & ││ Contract &  │     │ Build &     │     │ Memory &    │
 │ & Mesh      │     │ & Autonomy  │     │ & Execution ││ Scaffolding ││ Packaging   │     │ Diagnostics │     │ State Store │
 └─────────────┘     └─────────────┘     └─────────────┘└─────────────┘└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 📂 Category 00: Multi-Tasking & Agentive Workflows

### Purpose & Trigger Condition
Use this category when coordinating parallel subtasks, orchestrating multi-agent swarms (e.g. Architect, Implementer, Verifier), passing messages between background workers, compressing bloated context windows, or acquiring resource mutexes.

### Tools & Cited Use Cases

#### 1. `wc-task-dag`
* **Citation**: § 00.1 *Dependency-Aware Task DAG Scheduler with Deadlock Avoidance*
* **Trigger Condition**: When executing multi-phase workflows where tasks run in parallel or depend on previous task outputs.
* **Operational Recipe**:
  ```bash
  # Execute DAG workflow with 4 parallel worker threads
  bin/wc-task-dag workflow.json -w 4
  ```

#### 2. `wc-agent-mesh`
* **Citation**: § 00.2 *Multi-Agent Swarm Role Mesh & Consensus Coordinator*
* **Trigger Condition**: When orchestrating multi-agent teams across specialized roles (Architect, Implementer, BuildDoctor, Verifier, Auditor).
* **Operational Recipe**:
  ```bash
  # List predefined agent swarm roles
  bin/wc-agent-mesh roles

  # Generate structured swarm execution plan for a goal
  bin/wc-agent-mesh plan "Build Native JNI Memory Buffer"
  ```

#### 3. `wc-agent-channel`
* **Citation**: § 00.3 *Persistent Inter-Agent Pub/Sub Communication Bus*
* **Trigger Condition**: When background tasks or subagents need to communicate asynchronously without blocking or polling.
* **Operational Recipe**:
  ```bash
  # Publish a task completion event
  bin/wc-agent-channel pub "build:status" "SUCCESS" -s "BuilderAgent"

  # Subscribe and read incoming messages
  bin/wc-agent-channel sub "build:status" --mark-read
  ```

#### 4. `wc-context-pack`
* **Citation**: § 00.4 *Token Density & Context Window Optimization*
* **Trigger Condition**: When terminal dumps, crash logs, or diffs are too large and threaten to exhaust agent context limits.
* **Operational Recipe**:
  ```bash
  # Compress bloated build trace or logs
  bin/wc-context-pack build.log crash.log -m 30

  # Pipe live stream into token compressor
  logcat -d | bin/wc-context-pack
  ```

#### 5. `wc-resource-lock`
* **Citation**: § 00.5 *Distributed Workspace Mutex Lock*
* **Trigger Condition**: When parallel agents or background threads risk editing the same file or database concurrently.
* **Operational Recipe**:
  ```bash
  # Acquire mutex lock with 60s TTL
  bin/wc-resource-lock acquire "sqlite_database" -H "WriterAgent" -t 60

  # Release mutex lock
  bin/wc-resource-lock release "sqlite_database" -H "WriterAgent"
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
  bin/wc-agent-loop git push origin main
  ```

#### 2. `wc-agent-probe`
* **Citation**: § 0.2 *Internal Agent Environment Diagnostic Probe*
* **Trigger Condition**: When troubleshooting agent execution failures, missing PATH binaries, or Git 403 errors.
* **Operational Recipe**:
  ```bash
  bin/wc-agent-probe
  ```

#### 3. `wc-error-healer`
* **Citation**: § 0.3 *Deterministic Self-Healing Error Remediation*
* **Trigger Condition**: When commands fail with Git 403 permission errors, missing Termux shebangs, or SQLite WAL locks.
* **Operational Recipe**:
  ```bash
  bin/wc-error-healer --fix-path
  ```

---

## 📂 Category 1: Autonomous Pipeline & Task Execution

#### 1. `wc-task-exec`
* **Citation**: § 1.1 *Deterministic Task Receipts in Autonomous Systems*
* **Operational Recipe**:
  ```bash
  bin/wc-task-exec "Verify Launcher Refactoring" /path/to/project
  ```

#### 2. `wc-benchmark`
* **Citation**: § 1.2 *Latency-Constrained Mobile Process Execution*
* **Operational Recipe**:
  ```bash
  bin/wc-benchmark bin/wc-search "MainActivity" . -n 3 -t 0.5
  ```

---

## 📂 Category 2: Atomic Code Modification & Scaffolding

#### 1. `wc-code-mod`
* **Citation**: § 2.1 *Atomic Multi-File Transformations with Automatic Rollback*
* **Operational Recipe**:
  ```bash
  bin/wc-code-mod replace "oldApi()" "newApi()" . -e kt,java
  bin/wc-code-mod import "import com.piuu.launcher.ui.theme.*" app/src -e kt
  ```

#### 2. `wc-scaffold`
* **Citation**: § 2.2 *Zero-Overhead Component Generation for Jetpack Compose*
* **Operational Recipe**:
  ```bash
  bin/wc-scaffold compose app/src/main/java/com/piuu/launcher/ui/components/WallpaperSheet.kt
  bin/wc-scaffold repo app/src/main/java/com/piuu/launcher/repository/GridRepository.kt
  ```

---

## 📂 Category 3: Cross-Language Contracts & Packaging

#### 1. `wc-contract-check`
* **Citation**: § 3.1 *Cross-Language ABI Interface Verification*
* **Operational Recipe**:
  ```bash
  bin/wc-contract-check ~/repo/Piuu-Unified-Launcher-Android
  ```

#### 2. `wc-bundle-packer`
* **Citation**: § 3.2 *Cryptographic Extension Packaging and Integrity Verification*
* **Operational Recipe**:
  ```bash
  bin/wc-bundle-packer pack ./my-extension dist/extension.piuu --name "Weather Widget"
  bin/wc-bundle-packer verify dist/extension.piuu
  ```

---

## 📂 Category 4: Build Healing & Crash Diagnostics

#### 1. `wc-build-doctor`
* **Citation**: § 4.1 *Self-Healing Build Systems for Android and Gradle*
* **Operational Recipe**:
  ```bash
  bin/wc-build-doctor ~/repo/Piuu-Unified-Launcher-Android --fix
  ```

#### 2. `wc-crash-doctor`
* **Citation**: § 4.2 *Automated Stacktrace and Logcat Root-Cause Isolation*
* **Operational Recipe**:
  ```bash
  bin/wc-crash-doctor crash.log
  ```

---

## 📂 Category 5: Persistent Agent Memory & Rollback State

#### 1. `wc-agent-memory`
* **Citation**: § 5.1 *Long-Term Agent State Persistence in SQLite*
* **Operational Recipe**:
  ```bash
  bin/wc-agent-memory set "perf_priority" "Keep RAM under 150MB" -c "rules"
  bin/wc-agent-memory snapshot ~/repo/Piuu-Unified-Launcher-Android -t "pre-compose-v2"
  ```

---

## 📂 Category 6: Discovery, Search & Workspace Context

#### 1. `wc-tool-registry` | `wc-search` | `wc-deps` | `wc-scan` | `wc-analyze`
* **Citation**: § 6.1--6.4 *Workspace Context Exploration*
* **Operational Recipe**:
  ```bash
  bin/wc-tool-registry
  bin/wc-search "wallpaperTransparency" . -e kt,xml
  bin/wc-deps .
  bin/wc-scan .
  bin/wc-analyze summary .
  ```

---

## 📂 Category 7: System Telemetry & Workspace Maintenance

#### 1. `wc-termux-env` | `wc-manage` | `wc-monitor` | `wc-git-sync`
* **Citation**: § 7.1--7.3 *System Telemetry & Multi-Branch Flow*
* **Operational Recipe**:
  ```bash
  bin/wc-termux-env status
  bin/wc-manage sanitize . "*.tmp" --dry-run
  bin/wc-git-sync sync . main master
  ```

---

## 📊 Quick Category & Tool Selection Matrix

| Operational Goal | Recommended Category | Primary Tool | Fallback / Complementary Tool |
| :--- | :--- | :--- | :--- |
| **Run Parallel / DAG Tasks** | Cat 00: Multi-Tasking| `wc-task-dag` | `wc-agent-mesh`, `wc-agent-channel` |
| **Coordinate Agent Swarm** | Cat 00: Multi-Tasking| `wc-agent-mesh` | `wc-agent-channel`, `wc-resource-lock`|
| **Compress Context & Logs** | Cat 00: Multi-Tasking| `wc-context-pack`| `wc-crash-doctor` |
| **Run Command with Auto-Heal**| Cat 0: Agent Autonomy | `wc-agent-loop` | `wc-agent-probe`, `wc-error-healer` |
| **Verify Multi-Step Task** | Cat 1: Pipeline | `wc-task-exec` | `wc-benchmark` |
| **Refactor Code Across Files**| Cat 2: Code Mod | `wc-code-mod` | `wc-scaffold` |
| **Verify JNI / IPC Contracts**| Cat 3: Contracts | `wc-contract-check` | `wc-bundle-packer` |
| **Fix Build / Debug Crash** | Cat 4: Diagnostics | `wc-build-doctor` | `wc-crash-doctor` |
| **Save Checkpoint / Prefs** | Cat 5: Memory | `wc-agent-memory` | `wc-manage` |
| **Find Symbols / Code** | Cat 6: Context | `wc-search` | `wc-deps` |
| **Check RAM / Clean Caches** | Cat 7: Telemetry | `wc-termux-env` | `wc-manage` |
