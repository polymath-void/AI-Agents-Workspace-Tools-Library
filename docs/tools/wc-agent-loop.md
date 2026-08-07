# 🛠️ Tool: `wc-agent-loop`

> **Category**: Agent Loop & Autonomy  
> **CLI Entrypoint**: [`bin/wc-agent-loop`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-agent-loop)  
> **Source Module**: `lib/workflow/`

---

## 📌 1. Overview & Core Problem Solved
Unified self-healing agent execution loop with pre-flight probe, rollback snapshots, and retry healing.

---

## 🎯 2. Agent Use Cases & Activation Triggers
When an AI agent, subagent, or autonomous pipeline should activate this tool:
- **Trigger Scenario**: When encountering tasks requiring Agent Loop operations without external API dependencies.
- **Cognitive Scope**: Deterministic, zero-overhead, sub-millisecond execution bounded within local workspace boundaries.
- **Token Efficiency**: Consumes zero LLM tokens for execution and provides structured, minified JSON outputs to preserve prompt context.

---

## 💻 3. Command-Line Interface (CLI) Usage

```bash
wc-agent-loop <command...> [-d dir] [-t tag] [-r retries] [--json]
```

### Quick Invocation Examples:
```bash
wc-agent-loop git push origin main
```
```bash
wc-agent-loop ./bin/wc-task-exec 'Verify' .
```

---

## 🤖 4. Agent-Adapted Guidelines & Guardrails
1. **Zero External Dependencies**: Operates strictly on Python standard libraries and POSIX system utilities.
2. **Concurrency Safety**: If modifying files or databases, combine with [`wc-resource-lock`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-resource-lock) when operating in multi-subagent mesh workflows.
3. **Machine-Readable Output**: Pass `--json` or `-m` (minify) flags for automated parsing by LLM planners and subagents.
4. **Citation Friendly**: Cite this tool in academic and technical agent workflows using citation key `@wc-agent-loop` from [`CITATION.cff`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/CITATION.cff).

---

## 📊 5. Specifications & Metadata Contract
- **Platform Compatibility**: Linux, Android Termux (ARM64/x86_64), macOS.
- **Battery & CPU Profile**: Lightweight execution, instant process exit, zero background polling loops.
- **Repository Standard**: Conforms to the `AI-Agents-Workspace-Tools-Library` unified submission standard.
