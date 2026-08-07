# Agentic Operational Guide: Tool Organization & Categorized Use Cases (`AGENTS.md`)

> **Document Classification**: AI Agent Operational Specification  
> **System**: AI Agents Workspace Tools Library  
> **Architecture**: Modular Isolation (`lib/json/`, `lib/py/`, `lib/workflow/`, `lib/system/`)  
> **Standard Citation**: Polymath et al., *Autonomous Zero-Resource Task Execution and Workspace Context Ecosystem*, 2026. [`CITATION.cff`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/CITATION.cff)  

---

## 🏛️ Modular Package Architecture (Conflict-Free Isolation)

To eliminate cross-domain dependency pollution and avoid runtime collisions across autonomous agent swarms, the library enforces **strict package modularity**:

```
AI-Agents-Workspace-Tools-Library/lib/
├── 📦 json/         ── Isolated JSON & Data Suite (JSONPath Query, RFC 6902 Patch, Schema Validation)
├── 🐍 py/           ── Pure Python Core (AST Analysis, Code Modification, Scaffolding, Runtime)
├── ⚡ workflow/     ── Swarm & Workflow Engine (Task DAG, Agent Mesh, Pub/Sub Channel, Mutex Locks)
└── 🖥️ system/       ── Workspace Context & Maintenance (Inspection, Telemetry, Packaging, Contracts)
```

Agents can import isolated subsystems without pulling in unwanted dependencies:
```python
# Zero-conflict targeted imports
from lib.json import JSONSuite
from lib.py import ComplexityAnalyzer, batch_code_replace
from lib.workflow import TaskDAG, AgentChannel, ResourceLock
from lib.system import scan_directory, validate_jni_contracts
```

---

## 🗺️ Functional Category Taxonomy (10 Categories, 30 Tools)

```
                                  ┌─────────────────────────────────────────────────────────┐
                                  │            AGENT TASK / PROBLEM STATEMENT               │
                                  └────────────────────────────┬────────────────────────────┘
                                                               │
        ┌───────────────────┬───────────────────┬──────────────┼──────────────┬───────────────────┬───────────────────┐
        │                   │                   │              │              │                   │                   │
 ┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐┌──────▼──────┐┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
 │ Category 00 │     │ Category 01 │     │ Category 0  ││ Category 1  ││ Category 2  │     │ Category 3  │     │ Category 4-7│
 │ Multi-Task  │     │ JSON & Data │     │ Agent Loop  ││ Task Pipeline││ Code Mod & │     │ Contracts & │     │ Diagnostics,│
 │ & Mesh      │     │ Processing  │     │ & Autonomy  ││ & Execution ││ Scaffolding │     │ Packaging   │     │ Memory, Tele│
 └─────────────┘     └─────────────┘     └─────────────┘└─────────────┘└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 📂 Category 01: JSON & Data Processing Suite (`lib/json/`)

### Purpose & Trigger Condition
Use this category when manipulating configurations, validating plugin manifests, extracting nested JSONPath keys, or compressing verbose JSON payloads for prompt context savings.

#### 1. `wc-json-query`
* **Citation**: § 01.1 *Fast Dot/Bracket JSONPath Query & Token Minifier*
* **Recipe**:
  ```bash
  # Query nested key without loading full file into prompt context
  wc-json-query "build.targetSdk" config.json --raw

  # Minify JSON for token compression
  wc-json-query "." manifest.json -m
  ```

#### 2. `wc-json-patch`
* **Citation**: § 01.2 *Atomic Nested JSON Patcher & Deep Merger*
* **Recipe**:
  ```bash
  # In-place atomic property update
  wc-json-patch set config.json "build.targetSdk" 35 -i

  # Deep dictionary merge
  wc-json-patch merge manifest.json '{"version": "1.1.0"}' -i
  ```

#### 3. `wc-json-validate`
* **Citation**: § 01.3 *Zero-Overhead JSON Schema & Manifest Validator*
* **Recipe**:
  ```bash
  # Validate extension package manifest
  wc-json-validate manifest.json manifest --json
  ```

---

## 📂 Category 00: Multi-Tasking & Agentive Workflows (`lib/workflow/`)

* **`wc-task-dag`**: Dependency-aware DAG scheduler with parallel worker pools (`wc-task-dag workflow.json -w 4`).
* **`wc-agent-mesh`**: Multi-Agent Swarm Coordinator for role handoffs (`wc-agent-mesh plan "Build Feature"`).
* **`wc-agent-channel`**: SQLite WAL persistent pub/sub messaging bus (`wc-agent-channel pub "status" "OK"`).
* **`wc-context-pack`**: Token density optimizer & log compressor (`wc-context-pack build.log -m 30`).
* **`wc-resource-lock`**: Distributed mutex lock for shared file safety (`wc-resource-lock acquire "db" -t 60`).

---

## 📂 Category 0: Agent Loop & Autonomy (`lib/workflow/`)

* **`wc-agent-loop`**: Autonomous self-healing execution loop with rollback checkpoints.
* **`wc-agent-probe`**: Diagnostic probe for PATH, GitHub CLI auth, and memory limits.
* **`wc-error-healer`**: Deterministic error doctor for Git 403s, shebangs, and SQLite locks.

---

## 📂 Category 2: Python Core, Code Mod & Scaffolding (`lib/py/`)

* **`wc-code-mod`**: Multi-file atomic pattern replacement and import injection.
* **`wc-scaffold`**: Boilerplate generator for Jetpack Compose UI and StateFlow repos.
* **`wc-analyze`**: Cyclomatic complexity and lines-of-code structural analyzer.

---

## 📂 Category 3: Cross-Language Contracts & Packaging (`lib/system/`)

* **`wc-object-diff`**: Semantic entity comparator for JSON schemas, ASTs, and signatures.
* **`wc-contract-check`**: Cross-language ABI/IPC contract validator (Kotlin JNI <-> C <-> Electron).
* **`wc-bundle-packer`**: Cryptographic `.piuu` extension compiler and manifest verifier.

---

## 📊 Complete Tool Selection Decision Matrix

| Task / Scenario | Dedicated Tool | Modular Package | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Extract JSON property** | `wc-json-query` | `lib/json/` | Zero token cost, sub-millisecond JSONPath query |
| **Mutate / Merge JSON config**| `wc-json-patch` | `lib/json/` | In-place atomic update, no syntax breakage |
| **Validate Manifest schema** | `wc-json-validate`| `lib/json/` | Strict type and required field verification |
| **Compare Objects / Schemas** | `wc-object-diff` | `lib/system/` | Deep semantic diff ignoring key reordering |
| **Run Parallel Task DAG** | `wc-task-dag` | `lib/workflow/`| Dependency ordering with deadlock protection |
| **Publish Inter-Agent Event** | `wc-agent-channel`| `lib/workflow/`| Asynchronous pub/sub over persistent SQLite WAL |
| **Protect File from Concurrency**| `wc-resource-lock`| `lib/workflow/`| Cross-agent mutex locking with TTL guards |
| **Refactor Python / Kotlin AST**| `wc-code-mod` | `lib/py/` | Atomic replacement with rollback snapshots |
