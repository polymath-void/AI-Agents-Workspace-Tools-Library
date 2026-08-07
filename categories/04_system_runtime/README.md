# ⚙️ Category 04: System, Diagnostics & Build Operations

Dedicated tools for Android build self-healing, logcat crash diagnosis, `.piuu` extension packaging, Termux hardware telemetry, git branch synchronization, and workspace health monitoring.

---

## 🛠️ Tools Directory & Use-Case Mapping

| Tool Name | Core Use Case | When Agents Should Use This Tool |
| :--- | :--- | :--- |
| [`wc-build-doctor`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-build-doctor) | Android Gradle Build Doctor | When fixing `targetSdk 35`, Compose compiler options, Kotlin 2.0 flags, or 16KB page alignment. |
| [`wc-crash-doctor`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-crash-doctor) | Stacktrace & Crash Analyzer | When diagnosing Android logcat exceptions, SIGSEGV crashes, or Gradle build stacktraces. |
| [`wc-bundle-packer`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-bundle-packer) | `.piuu` Extension Bundle Compiler | When packaging extensions, widgets, or themes into verified `.piuu` archives with SHA256 manifests. |
| [`wc-benchmark`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-benchmark) | Performance & Battery Benchmark | When measuring execution latency and CPU impact against strict performance thresholds. |
| [`wc-termux-env`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-termux-env) | Hardware Telemetry & Toolchains | When inspecting device RAM, CPU load, verifying installed compilers (clang, python), or fixing shebangs. |
| [`wc-git-sync`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-git-sync) | Git Unified Branch Sync | When syncing branches (`main` and `master` in one path) or inspecting git working tree clean states. |
| [`wc-deps`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-deps) | Multi-Ecosystem Dependency Inspector | When auditing Gradle, NPM, Pip, or Cargo dependencies and checking version conflicts. |
| [`wc-scan`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-scan) | Resilient Workspace Tree Scanner | When scanning complete directory hierarchies and calculating total file metrics. |
| [`wc-manage`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-manage) | Safe Workspace Sanitizer | When removing build artifacts (`*.o`, `build/`, `*.tmp`) safely without touching source code. |
| [`wc-monitor`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-monitor) | Workspace Health & Anomaly Detector | When continuously checking repositories for forbidden binary blobs, large files, or style violations. |
| [`wc-agent-memory`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-agent-memory) | Persistent Memory & File Snapshots | When storing architectural preferences, rules, or creating rollback snapshots before modifications. |
| [`wc-task-exec`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-task-exec) | Autonomous Multi-Phase Pipeline | When running full-phase task pipelines (Environment $\rightarrow$ Deps $\rightarrow$ Health $\rightarrow$ Tests) with verifiable receipts. |
| [`wc-tool-registry`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-tool-registry) | Master Interactive Tool Catalog | When querying tools by category, capability, or usage keywords in machine-readable JSON. |

---

## ⚡ Agent Invocation Examples

```bash
# 1. Self-heal Android Gradle configuration
wc-build-doctor ~/repo/Piuu-Unified-Launcher-Android --fix

# 2. Package a custom widget into a .piuu bundle
wc-bundle-packer pack ./my-widget dist/widget.piuu --name "ClockWidget"

# 3. Diagnose a raw logcat crash
logcat -d | wc-crash-doctor

# 4. Check device RAM and hardware telemetry in Termux
wc-termux-env status
```
