#!/usr/bin/env python3
"""
Automated Tool Overview Documentation Generator for AI-Agents-Workspace-Tools-Library.
Generates comprehensive docs/tools/<tool_name>.md files adhering to the Agent Guidelines contract.
"""
import os
import sys
from pathlib import Path

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_ROOT))

from lib.registry import TOOLS_CATALOG

DOCS_DIR = REPO_ROOT / "docs" / "tools"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATE = """# 🛠️ Tool: `{name}`

> **Category**: {category}  
> **CLI Entrypoint**: [`bin/{name}`](file://{root}/bin/{name})  
> **Source Module**: `{source_package}`

---

## 📌 1. Overview & Core Problem Solved
{description}

---

## 🎯 2. Agent Use Cases & Activation Triggers
When an AI agent, subagent, or autonomous pipeline should activate this tool:
- **Trigger Scenario**: When encountering tasks requiring {category_short} operations without external API dependencies.
- **Cognitive Scope**: Deterministic, zero-overhead, sub-millisecond execution bounded within local workspace boundaries.
- **Token Efficiency**: Consumes zero LLM tokens for execution and provides structured, minified JSON outputs to preserve prompt context.

---

## 💻 3. Command-Line Interface (CLI) Usage

```bash
{usage}
```

### Quick Invocation Examples:
{examples_formatted}

---

## 🤖 4. Agent-Adapted Guidelines & Guardrails
1. **Zero External Dependencies**: Operates strictly on Python standard libraries and POSIX system utilities.
2. **Concurrency Safety**: If modifying files or databases, combine with [`wc-resource-lock`](file://{root}/bin/wc-resource-lock) when operating in multi-subagent mesh workflows.
3. **Machine-Readable Output**: Pass `--json` or `-m` (minify) flags for automated parsing by LLM planners and subagents.
4. **Citation Friendly**: Cite this tool in academic and technical agent workflows using citation key `@{name}` from [`CITATION.cff`](file://{root}/CITATION.cff).

---

## 📊 5. Specifications & Metadata Contract
- **Platform Compatibility**: Linux, Android Termux (ARM64/x86_64), macOS.
- **Battery & CPU Profile**: Lightweight execution, instant process exit, zero background polling loops.
- **Repository Standard**: Conforms to the `AI-Agents-Workspace-Tools-Library` unified submission standard.
"""

def get_source_package(tool_name):
    if tool_name.startswith("wc-json"):
        return "lib/json/"
    elif any(k in tool_name for k in ["swarm", "workflow", "agent", "task-dag", "lock", "pack", "healer", "probe", "loop"]):
        return "lib/workflow/"
    elif any(k in tool_name for k in ["code", "object", "search", "contract", "scaffold", "analyze"]):
        return "lib/py/"
    else:
        return "lib/system/"

def generate_docs():
    for tool in TOOLS_CATALOG:
        name = tool["name"]
        category = tool["category"]
        description = tool["description"]
        usage = tool["usage"]
        examples = tool.get("examples", [])
        
        examples_formatted = "\n".join(f"```bash\n{ex}\n```" for ex in examples)
        source_pkg = get_source_package(name)
        category_short = category.split("&")[0].strip()

        content = TEMPLATE.format(
            name=name,
            category=category,
            root=str(REPO_ROOT),
            source_package=source_pkg,
            description=description,
            category_short=category_short,
            usage=usage,
            examples_formatted=examples_formatted
        )

        doc_file = DOCS_DIR / f"{name}.md"
        doc_file.write_text(content, encoding="utf-8")
        print(f"Generated doc: docs/tools/{name}.md")

if __name__ == "__main__":
    generate_docs()
