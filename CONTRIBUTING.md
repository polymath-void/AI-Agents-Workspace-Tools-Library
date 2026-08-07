# Contributing to AI Agents Workspace Tools Library

We welcome contributions from both human developers and autonomous AI agent systems!

## 🛠️ Development & Testing Workflow

1. Clone or navigate to the repository:
   ```bash
   cd ~/AI-Agents-Workspace-Tools-Library
   ```
2. Add new tools into `lib/` and wire executable wrappers into `bin/`.
3. Register the new tool in `lib/registry.py`.
4. Ensure full test coverage in `tests/test_all.py`.
5. Run the unit test suite:
   ```bash
   python3 -m unittest tests/test_all.py
   ```
6. Format your commit messages following the Conventional Commits specification:
   - `feat(tools): Add new contract validator for RPC schemas`
   - `fix(scanner): Handle symlink loops gracefully`
