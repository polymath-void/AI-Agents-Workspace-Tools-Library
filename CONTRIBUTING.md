# Contributing to AI Agents Workspace Tools Library ⚡

We warmly welcome contributions from **both human developers and autonomous AI agent systems**!

---

## 🏛️ Core Principles & Non-Negotiables

1. **Zero External Dependencies**:
   - Everything must be built using pure Python 3 standard libraries and POSIX core utilities.
   - Do NOT introduce external `pip` dependencies (e.g., `requests`, `numpy`, `pandas`).
2. **Universal Portability**:
   - Every executable CLI tool in `bin/` must use the universal shebang: `#!/usr/bin/env python3`.
   - All tools must execute cleanly across Linux, macOS, Windows (WSL), and Android Termux.
3. **Sub-100ms Performance**:
   - Design algorithms for minimal latency and memory footprint to prevent mobile battery drain and swarm lag.
4. **Context Window Economy**:
   - Implement structured `--json` and `--compact` flags to keep LLM context consumption minimal.

---

## 🛠️ The 7-Point Unified Tool Submission Standard

When introducing a new tool or agent skill, contributors and autonomous agents MUST fulfill all 7 stages:

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                   TOOL SUBMISSION VERIFICATION PIPELINE                │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
   1. [Core Implementation] ─────────┼──► lib/<package>/<module>.py
   2. [CLI Entrypoint]      ─────────┼──► bin/<tool_name> (chmod +x, universal shebang)
   3. [Catalog Registration]─────────┼──► lib/registry.py (TOOLS_CATALOG entry)
   4. [Dedicated Overview]  ─────────┼──► docs/tools/<tool_name>.md (Specs & use cases)
   5. [Category Symlink]    ─────────┼──► categories/<cat_dir>/<tool_name>
   6. [Unit Regression Test]─────────┼──► tests/ (100% passing tests)
   7. [Single-Path Git Sync]─────────┴──► Commit & push directly to main
```

### Step-by-Step Instructions:

1. **Core Package Logic (`lib/`)**:
   - Place your module in the appropriate package (`lib/json/`, `lib/workflow/`, `lib/py/`, or `lib/system/`).
   - Export public interfaces in `lib/<package>/__init__.py`.
2. **CLI Executable (`bin/`)**:
   - Add entrypoint in `bin/<tool_name>` with `#!/usr/bin/env python3`.
   - Implement `argparse` with `--help`, stdin pipe handling, and `--json` formatting.
   - Mark executable: `chmod +x bin/<tool_name>`.
3. **Registry Registration (`lib/registry.py`)**:
   - Add tool metadata to `TOOLS_CATALOG` with name, category, description, and usage examples.
4. **Documentation (`docs/tools/<tool_name>.md`)**:
   - Create documentation covering use-cases, flags, examples, and agent activation triggers.
5. **Category Symlink (`categories/`)**:
   - Create symlink: `ln -s ../../bin/<tool_name> categories/<cat_dir>/<tool_name>`.
6. **Testing (`tests/`)**:
   - Add unit tests. Verify passing suite:
     ```bash
     python3 -m unittest discover tests
     ```
7. **Commit & Push**:
   - Format commit message using Conventional Commits: `feat(tools): add <tool-name> for <purpose>`.

---

## 🤖 Agent Skill Creation & Packaging (`.skill`)

Agents crafting modular skills for Gemini CLI, Antigravity, or Hermes must:
1. Include valid YAML frontmatter in `SKILL.md`:
   ```yaml
   ---
   name: my-new-skill
   description: Specific trigger description for agent activation.
   ---
   ```
2. Lint and package using `wc-skill-pack`:
   ```bash
   wc-skill-pack --lint path/to/skill/
   wc-skill-pack --build path/to/skill/ --out ./dist/
   ```

---

## 📄 License
By contributing, you agree that your contributions will be licensed under the [Apache-2.0 License](LICENSE).
