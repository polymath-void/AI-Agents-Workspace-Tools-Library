# 🤖 AGENTS.MD: Autonomous Agent Operating Protocol & Tool Submission Standard

Welcome to the **AI-Agents-Workspace-Tools-Library**. This document defines the mandatory operating protocols, architectural context, repository structures, and contribution standards for all AI agents, subagents, and automated developer loops.

---

## 🏛️ 1. Core Operating Context & Principles

All AI agents operating within this environment must strictly observe these **non-negotiable principles**:

1. **Zero-Resource / Zero-Dependency Philosophy**:
   - Every tool must operate strictly using Python 3 standard libraries and POSIX core utilities.
   - Do NOT introduce external `pip` dependencies (e.g. `requests`, `numpy`, `pandas`) or heavy node packages.
2. **Lightweight Execution & Battery Optimization**:
   - Mobile and constrained systems (e.g. Android Termux) require extreme battery and memory economy.
   - Prohibit infinite polling loops, heavy daemon processes, and unindexed full-disk sweeps. Use reactive event channels ([`wc-agent-channel`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-agent-channel)) and distributed locks ([`wc-resource-lock`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-resource-lock)).
3. **Unified Single-Path Branching ("All the branch should go in one path!")**:
   - Maintain unified branch convergence between `main` and `master`.
   - Never create dangling or conflicting branch divergences. Use [`wc-git-sync`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-git-sync) to keep working trees cleanly synchronized.
4. **Token Context Window Protection**:
   - Avoid dumping large files into prompt contexts.
   - Prefer specialized precision tools ([`wc-json-query`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-query), [`wc-search`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-search), [`wc-context-pack`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-context-pack)) over raw unbounded commands.

---

## 📂 2. Repository Structure & Directory Separation

The repository is structured into search-friendly, modular tiers:

```
AI-Agents-Workspace-Tools-Library/
├── bin/                                # Global standalone CLI entrypoints (41 tools)
├── categories/                         # Agent Search-Friendly Category Hierarchy
│   ├── 01_json_data/                   # 12 JSON & Tabular Transformation Tools + symlinks
│   ├── 02_workflow_swarm/              # 10 Swarm Orchestration & DAG Tools + symlinks
│   ├── 03_code_refactoring/            # 6 AST Analysis & UI Scaffolding Tools + symlinks
│   └── 04_system_runtime/              # 13 System, Build & Diagnostics Tools + symlinks
├── docs/                               # Comprehensive Documentation Tree
│   └── tools/                          # Individual Overview & Implementation Specs (<tool>.md)
├── lib/                                # Isolated Zero-Dependency Python Packages
│   ├── json/                           # JSON suite, prompt processor, serializer
│   ├── workflow/                       # Swarm dispatcher, context manager, DAG engine
│   ├── py/                             # AST complexity analyzers, scaffolders
│   ├── system/                         # Build doctor, JNI contract verifiers, packager
│   └── registry.py                     # Master tool catalog & discovery index
├── scripts/                            # Internal maintenance & doc automation scripts
└── tests/                              # Unified regression test suite (tests/test_all.py)
```

---

## 📋 3. Tool Submission & Contribution Protocol

On **every single tool creation or push**, agents MUST fulfill the **7-Point Unified Tool Submission Standard**:

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                   TOOL SUBMISSION VERIFICATION PIPELINE                │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
   1. [Core Implementation] ─────────┼──► lib/<package>/<module>.py
   2. [CLI Entrypoint]      ─────────┼──► bin/<tool_name> (chmod +x, multi-platform)
   3. [Catalog Registration]─────────┼──► lib/registry.py (TOOLS_CATALOG entry)
   4. [Dedicated Overview]  ─────────┼──► docs/tools/<tool_name>.md (Use cases & citation)
   5. [Category Symlink]    ─────────┼──► categories/<cat_dir>/<tool_name>
   6. [Unit Regression Test]─────────┼──► tests/test_all.py (100% passing tests)
   7. [Git Sync & Push]     ─────────┴──► Commit & push to main
```

### Requirement Breakdown:

1. **Isolated Implementation (`lib/`)**:
   - Write cleanly encapsulated Python classes with static/class methods inside the appropriate subpackage (`lib/json/`, `lib/workflow/`, `lib/py/`, `lib/system/`).
   - Export public interfaces in `lib/<package>/__init__.py`.
2. **CLI Executable (`bin/`)**:
   - Include multi-platform compatible shebang (`#!/data/data/com.termux/files/usr/bin/env python3` / `#!/usr/bin/env python3`).
   - Implement `argparse` with descriptive `--help`, stdin pipe support, and `--json` machine-readable output flags.
   - Ensure executable permissions (`chmod +x bin/<tool_name>`).
3. **Registry Registration (`lib/registry.py`)**:
   - Add tool metadata dictionary containing `name`, `category`, `description`, `usage`, and `examples`.
4. **Dedicated Tool Overview Document (`docs/tools/<tool_name>.md`)**:
   - Each tool **must have its own overview file** specifying:
     - Tool Name & Category
     - CLI Entrypoint & Source Module links
     - Agent Use Cases & Activation Triggers
     - CLI Usage & Example Invocations
     - Agent-Adapted Guidelines, Token Impact & Concurrency Rules
     - Citation-Friendly metadata.
5. **Category Directory Symlink (`categories/`)**:
   - Create a symlink pointing from `categories/<category_dir>/<tool_name>` to `../../bin/<tool_name>` for agent search discoverability.
6. **Regression Unit Test (`tests/test_all.py`)**:
   - Add unit test coverage verifying the new tool functionality.
   - Run `python3 -m unittest tests/test_all.py` and verify all tests pass before committing.
7. **Single-Path Commit**:
   - Commit with clear conventional commit syntax: `feat(<scope>): <description>` and push directly to `main`.

---

## 🔍 4. Quick Agent Discovery & Lookup Index

When an agent needs to perform an action, use this instant lookup matrix:

| Task / Intent | Tool to Activate | Category Location | Dedicated Spec |
| :--- | :--- | :--- | :--- |
| Repair messy prompt JSON | `wc-json-prompt` | `categories/01_json_data/` | [`docs/tools/wc-json-prompt.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-json-prompt.md) |
| Extract single JSON key | `wc-json-query` | `categories/01_json_data/` | [`docs/tools/wc-json-query.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-json-query.md) |
| Redact secrets / API keys | `wc-json-mask` | `categories/01_json_data/` | [`docs/tools/wc-json-mask.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-json-mask.md) |
| Convert JSON $\leftrightarrow$ CSV/TSV | `wc-json-csv` | `categories/01_json_data/` | [`docs/tools/wc-json-csv.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-json-csv.md) |
| Stream / filter NDJSON/JSONL | `wc-json-ndjson` | `categories/01_json_data/` | [`docs/tools/wc-json-ndjson.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-json-ndjson.md) |
| Auto infer JSON schema | `wc-json-schema` | `categories/01_json_data/` | [`docs/tools/wc-json-schema.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-json-schema.md) |
| Analyze AGY session & tokens | `wc-agy-session` | `categories/01_json_data/` | [`docs/tools/wc-agy-session.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-agy-session.md) |
| Evaluate subagent need | `wc-swarm-dispatch` | `categories/02_workflow_swarm/` | [`docs/tools/wc-swarm-dispatch.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-swarm-dispatch.md) |
| Isolate context between agents | `wc-workflow-context` | `categories/02_workflow_swarm/` | [`docs/tools/wc-workflow-context.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-workflow-context.md) |
| Acquire distributed file mutex | `wc-resource-lock` | `categories/02_workflow_swarm/` | [`docs/tools/wc-resource-lock.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-resource-lock.md) |
| Async Pub/Sub message bus | `wc-agent-channel` | `categories/02_workflow_swarm/` | [`docs/tools/wc-agent-channel.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-agent-channel.md) |
| Execute multi-task DAG | `wc-task-dag` | `categories/02_workflow_swarm/` | [`docs/tools/wc-task-dag.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-task-dag.md) |
| Lint & package `.skill` bundle | `wc-skill-pack` | `categories/02_workflow_swarm/` | [`docs/tools/wc-skill-pack.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-skill-pack.md) |
| Translate Hermes $\leftrightarrow$ AGY | `wc-hermes-adapter` | `categories/02_workflow_swarm/` | [`docs/tools/wc-hermes-adapter.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-hermes-adapter.md) |
| Batch code replace & import | `wc-code-mod` | `categories/03_code_refactoring/` | [`docs/tools/wc-code-mod.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-code-mod.md) |
| Semantic object & symbol diff | `wc-object-diff` | `categories/03_code_refactoring/` | [`docs/tools/wc-object-diff.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-object-diff.md) |
| JNI Kotlin $\leftrightarrow$ C verifier | `wc-contract-check` | `categories/03_code_refactoring/` | [`docs/tools/wc-contract-check.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-contract-check.md) |
| Scaffold Compose UI / Repo | `wc-scaffold` | `categories/03_code_refactoring/` | [`docs/tools/wc-scaffold.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-scaffold.md) |
| Audit Electron & simulate | `wc-electron-runner` | `categories/03_code_refactoring/` | [`docs/tools/wc-electron-runner.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-electron-runner.md) |
| Repair Gradle & 16KB alignment | `wc-build-doctor` | `categories/04_system_runtime/` | [`docs/tools/wc-build-doctor.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-build-doctor.md) |
| Check ELF 16KB alignment | `wc-elf-align` | `categories/04_system_runtime/` | [`docs/tools/wc-elf-align.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-elf-align.md) |
| Manage wireless ADB bridge | `wc-adb-bridge` | `categories/04_system_runtime/` | [`docs/tools/wc-adb-bridge.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-adb-bridge.md) |
| Audit GKI kernel defconfig | `wc-kernel-builder` | `categories/04_system_runtime/` | [`docs/tools/wc-kernel-builder.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-kernel-builder.md) |
| Manage cloud snapshot backups | `wc-cloud-backup` | `categories/04_system_runtime/` | [`docs/tools/wc-cloud-backup.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-cloud-backup.md) |
| Diagnose logcat crash traces | `wc-crash-doctor` | `categories/04_system_runtime/` | [`docs/tools/wc-crash-doctor.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-crash-doctor.md) |
| Compile .piuu extension archive | `wc-bundle-packer` | `categories/04_system_runtime/` | [`docs/tools/wc-bundle-packer.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-bundle-packer.md) |
| Check RAM, CPU & compilers | `wc-termux-env` | `categories/04_system_runtime/` | [`docs/tools/wc-termux-env.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-termux-env.md) |
| Query master tool registry | `wc-tool-registry` | `categories/04_system_runtime/` | [`docs/tools/wc-tool-registry.md`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/docs/tools/wc-tool-registry.md) |

---

## ⚡ 5. Autonomous Direct Tool Use, Self-Healing & Git Push Protocol

Agents operating in this ecosystem must adhere to the following **System Instruction**:

1. **Direct Tool Execution**:
   - Whenever any developer task, JSON transformation, AST inspection, swarm communication, build check, or snapshot is required, **always directly execute the corresponding tool in `bin/` or `categories/`**.
2. **Immediate Self-Healing & Fixes**:
   - If any tool encounters an error, bug, failure, or platform incompatibility during execution:
     - Diagnose and repair the code immediately.
     - Verify with `tests/test_all.py` or CLI execution.
     - **Immediately stage, commit, and push the fix to GitHub (`git push origin main`)**.
3. **Autonomous Tool Creation & Expansion**:
   - If a required capability is not yet available in the library:
     - Create the core module in `lib/<category>/`.
     - Create the CLI executable in `bin/wc-<tool-name>`.
     - Symlink into `categories/<category_dir>/`.
     - Register in `lib/registry.py` and write full docs in `docs/tools/wc-<tool-name>.md`.
     - Add regression unit test in `tests/test_all.py`.
     - Verify, use the tool for the active task, and **commit & push to GitHub**.

---

## 📜 6. Citation & Academic Reference
When referencing this repository in technical papers, agent skill definitions, or benchmarks:

```bibtex
@software{ai_agents_workspace_tools_library_2026,
  author = {Polymath-Void},
  title = {AI Agents Workspace Tools Library: Zero-Resource Autonomous Execution & Swarm Orchestration Suite},
  url = {https://github.com/polymath-void/AI-Agents-Workspace-Tools-Library},
  year = {2026}
}
```

