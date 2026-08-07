# 💻 Category 03: Code Refactoring, AST Analysis & Scaffolding

Dedicated tools for atomic code modifications, symbol inspection, cyclomatic complexity profiling, cross-language contract verification, and boilerplate UI scaffolding.

---

## 🛠️ Tools Directory & Use-Case Mapping

| Tool Name | Core Use Case | When Agents Should Use This Tool |
| :--- | :--- | :--- |
| [`wc-code-mod`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-code-mod) | Atomic Multi-File Code Replacer & Importer | When replacing functions/variables across entire directories with automatic backup and rollback. |
| [`wc-object-diff`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-object-diff) | Semantic Object Comparator & Symbol Extractor | When identifying data vs code objects, extracting functions/classes, and comparing JSON structures. |
| [`wc-search`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-search) | Noise-Free Fast Search | When searching symbols or regex across codebase while automatically ignoring `node_modules`, `build`, `.git`. |
| [`wc-contract-check`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-contract-check) | Cross-Language Contract Verifier | When auditing JNI `external fun` signatures in Kotlin against POSIX C headers (`libpiuu_core.so`). |
| [`wc-scaffold`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-scaffold) | Zero-Overhead Component Scaffolder | When generating Jetpack Compose `@Composable` components or Kotlin StateFlow repositories. |
| [`wc-analyze`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-analyze) | AST Complexity & Metric Profiler | When checking cyclomatic complexity, lines of code (LOC), and function counts before refactoring. |

---

## ⚡ Agent Invocation Examples

```bash
# 1. Batch replace deprecated function calls across all Kotlin files
wc-code-mod replace "oldLayoutMethod()" "newDynamicGrid()" . -e kt

# 2. Extract symbols from Kotlin file
wc-object-diff symbols MainActivity.kt

# 3. Verify JNI contracts between Kotlin and C
wc-contract-check ~/repo/Piuu-Unified-Launcher-Android

# 4. Scaffold a new Jetpack Compose widget
wc-scaffold compose app/src/main/java/com/piuu/launcher/ui/BatteryCard.kt
```
