# 🤖 AI Agents Workspace Tools Reference & Category Guide

This guide defines how AI agents, subagents, and automated workflows navigate, discover, and execute tools within the **AI-Agents-Workspace-Tools-Library**.

All 41 tools are organized into 4 search-friendly category directories under `categories/` and accessible via `bin/`.

---

## 📂 Search-Friendly Category Hierarchy

```
AI-Agents-Workspace-Tools-Library/
├── bin/                                # Global binary path (41 tools)
│   ├── wc-json-*
│   ├── wc-agent-*
│   ├── wc-task-*
│   └── ...
├── categories/                         # Category-separated directory views
│   ├── 01_json_data/                   # 12 JSON & data transformation tools
│   ├── 02_workflow_swarm/              # 10 Swarm orchestration & DAG tools
│   ├── 03_code_refactoring/            # 6 AST analysis & scaffolding tools
│   └── 04_system_runtime/              # 13 System, build & diagnostic tools
└── lib/                                # Zero-dependency Python modules
    ├── json/                           # JSON suite & prompt processors
    ├── workflow/                       # Swarm dispatcher & context managers
    ├── py/                             # AST analyzers & scaffolders
    └── system/                         # Diagnostics, packagers & verifiers
```

---

## 🧭 Fast Agent Capability Lookup Matrix

| If You Need To... | Use This Tool | Category Path |
| :--- | :--- | :--- |
| **Parse messy/unquoted JSON from user chat** | [`wc-json-prompt`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-prompt) | `categories/01_json_data/` |
| **Query a single nested key from large JSON** | [`wc-json-query`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-query) | `categories/01_json_data/` |
| **Mutate or patch JSON keys in place** | [`wc-json-patch`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-patch) | `categories/01_json_data/` |
| **Mask secrets, tokens & API keys in JSON** | [`wc-json-mask`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-mask) | `categories/01_json_data/` |
| **Convert JSON arrays to/from CSV or TSV** | [`wc-json-csv`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-csv) | `categories/01_json_data/` |
| **Stream or filter JSON Lines (NDJSON)** | [`wc-json-ndjson`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-ndjson) | `categories/01_json_data/` |
| **Infer JSON Schema Draft 7 from sample** | [`wc-json-schema`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-schema) | `categories/01_json_data/` |
| **Evaluate if a task needs a subagent** | [`wc-swarm-dispatch`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-swarm-dispatch) | `categories/02_workflow_swarm/` |
| **Isolate context frames between subagents** | [`wc-workflow-context`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-workflow-context) | `categories/02_workflow_swarm/` |
| **Acquire mutex lock on shared files** | [`wc-resource-lock`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-resource-lock) | `categories/02_workflow_swarm/` |
| **Publish/Subscribe async events** | [`wc-agent-channel`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-agent-channel) | `categories/02_workflow_swarm/` |
| **Execute multi-task dependency DAGs** | [`wc-task-dag`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-task-dag) | `categories/02_workflow_swarm/` |
| **Batch replace code across directory** | [`wc-code-mod`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-code-mod) | `categories/03_code_refactoring/` |
| **Compare objects & extract symbols** | [`wc-object-diff`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-object-diff) | `categories/03_code_refactoring/` |
| **Verify Kotlin JNI $\leftrightarrow$ C signatures** | [`wc-contract-check`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-contract-check) | `categories/03_code_refactoring/` |
| **Scaffold Compose UI or Repositories** | [`wc-scaffold`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-scaffold) | `categories/03_code_refactoring/` |
| **Fix Gradle configs & 16KB alignment** | [`wc-build-doctor`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-build-doctor) | `categories/04_system_runtime/` |
| **Analyze logcat crashes & SIGSEGV** | [`wc-crash-doctor`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-crash-doctor) | `categories/04_system_runtime/` |
| **Pack .piuu extension archives** | [`wc-bundle-packer`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-bundle-packer) | `categories/04_system_runtime/` |
| **Check RAM, CPU & verify compilers** | [`wc-termux-env`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-termux-env) | `categories/04_system_runtime/` |

---

## 🔍 Instant Registry Query Command

Agents can search the entire tool suite dynamically via CLI:
```bash
# Query tools by keyword
wc-tool-registry "json"

# Output machine-readable JSON catalog
wc-tool-registry --json
```
