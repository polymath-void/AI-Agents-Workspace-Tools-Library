# 🛠️ Tool: `wc-workflow-context`

> **Category**: Multi-Tasking & Workflows  
> **CLI Entrypoint**: [`bin/wc-workflow-context`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-workflow-context)  
> **Source Module**: `lib/workflow/`

---

## 📌 1. Overview & Core Problem Solved
Cross-workflow context isolation, token frame manager & selective handoff bus between subagents.

---

## 🎯 2. Agent Use Cases & Activation Triggers
When an AI agent, subagent, or autonomous pipeline should activate this tool:
- **Trigger Scenario**: When encountering tasks requiring Multi-Tasking operations without external API dependencies.
- **Cognitive Scope**: Deterministic, zero-overhead, sub-millisecond execution bounded within local workspace boundaries.
- **Token Efficiency**: Consumes zero LLM tokens for execution and provides structured, minified JSON outputs to preserve prompt context.

---

## 💻 3. Command-Line Interface (CLI) Usage

```bash
wc-workflow-context <register|set|get|handoff|prune> [args...]
```

### Quick Invocation Examples:
```bash
wc-workflow-context set wf_build targetSdk 35
```
```bash
wc-workflow-context handoff wf_build wf_package targetSdk
```
```bash
wc-workflow-context get wf_package --json
```

---

## 🤖 4. Agent-Adapted Guidelines & Guardrails
1. **Zero External Dependencies**: Operates strictly on Python standard libraries and POSIX system utilities.
2. **Concurrency Safety**: If modifying files or databases, combine with [`wc-resource-lock`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-resource-lock) when operating in multi-subagent mesh workflows.
3. **Machine-Readable Output**: Pass `--json` or `-m` (minify) flags for automated parsing by LLM planners and subagents.
4. **Citation Friendly**: Cite this tool in academic and technical agent workflows using citation key `@wc-workflow-context` from [`CITATION.cff`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/CITATION.cff).

---

## 📊 5. Specifications & Metadata Contract
- **Platform Compatibility**: Linux, Android Termux (ARM64/x86_64), macOS.
- **Battery & CPU Profile**: Lightweight execution, instant process exit, zero background polling loops.
- **Repository Standard**: Conforms to the `AI-Agents-Workspace-Tools-Library` unified submission standard.
