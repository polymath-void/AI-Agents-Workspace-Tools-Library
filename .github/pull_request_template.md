## 📋 Description of Changes

<!-- Provide a concise description of the new tool, bug fix, or skill added. -->

## 🤖 Contributor Type
- [ ] Human Developer
- [ ] Autonomous AI Agent (AGY / Gemini / Hermes / Claude / Other)

## 🛠️ 7-Point Unified Tool Submission Checklist
- [ ] **1. Core Logic**: Module placed in `lib/<category>/` using pure Python stdlib (0 pip dependencies).
- [ ] **2. CLI Executable**: Created in `bin/<tool-name>` with `chmod +x` and `#!/usr/bin/env python3`.
- [ ] **3. Tool Registry**: Registered in `lib/registry.py` under `TOOLS_CATALOG`.
- [ ] **4. Dedicated Spec**: Overview document written at `docs/tools/<tool-name>.md`.
- [ ] **5. Category Symlink**: Symlinked under `categories/<category_dir>/<tool-name>`.
- [ ] **6. Regression Tests**: Added unit tests in `tests/` and verified with `python3 -m unittest discover tests`.
- [ ] **7. Single-Path Git Sync**: Verified branch convergence.
