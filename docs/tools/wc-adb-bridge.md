# 🛠️ Tool: `wc-adb-bridge`

> **Category**: Android & Termux System  
> **CLI Entrypoint**: [`bin/wc-adb-bridge`](file:///data/data/com.termux/files/home/Workspace/AI-Agents-Workspace-Tools-Library/bin/wc-adb-bridge)  
> **Source Module**: `lib/system/`

---

## 📌 1. Overview & Core Problem Solved
Termux & Linux wireless ADB connection manager, port discovery, remote shell execution and framebuffer screencap tool.

---

## 🎯 2. Agent Use Cases & Activation Triggers
When an AI agent, subagent, or autonomous pipeline should activate this tool:
- **Trigger Scenario**: When encountering tasks requiring Android operations without external API dependencies.
- **Cognitive Scope**: Deterministic, zero-overhead, sub-millisecond execution bounded within local workspace boundaries.
- **Token Efficiency**: Consumes zero LLM tokens for execution and provides structured, minified JSON outputs to preserve prompt context.

---

## 💻 3. Command-Line Interface (CLI) Usage

```bash
wc-adb-bridge <devices|pair|connect|shell|screencap|telemetry> [args]
```

### Quick Invocation Examples:
```bash
wc-adb-bridge devices
```
```bash
wc-adb-bridge pair 192.168.1.100:37891 123456
```
```bash
wc-adb-bridge screencap phone_screen.png
```
```bash
wc-adb-bridge telemetry
```

---

## 🤖 4. Agent-Adapted Guidelines & Guardrails
1. **Zero External Dependencies**: Operates strictly on Python standard libraries and POSIX system utilities.
2. **Concurrency Safety**: If modifying files or databases, combine with [`wc-resource-lock`](file:///data/data/com.termux/files/home/Workspace/AI-Agents-Workspace-Tools-Library/bin/wc-resource-lock) when operating in multi-subagent mesh workflows.
3. **Machine-Readable Output**: Pass `--json` or `-m` (minify) flags for automated parsing by LLM planners and subagents.
4. **Citation Friendly**: Cite this tool in academic and technical agent workflows using citation key `@wc-adb-bridge` from [`CITATION.cff`](file:///data/data/com.termux/files/home/Workspace/AI-Agents-Workspace-Tools-Library/CITATION.cff).

---

## 📊 5. Specifications & Metadata Contract
- **Platform Compatibility**: Linux, Android Termux (ARM64/x86_64), macOS.
- **Battery & CPU Profile**: Lightweight execution, instant process exit, zero background polling loops.
- **Repository Standard**: Conforms to the `AI-Agents-Workspace-Tools-Library` unified submission standard.
