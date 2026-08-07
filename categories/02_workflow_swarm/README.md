# 🐝 Category 02: Multi-Tasking, Workflows & Swarm Coordination

Dedicated tools for subagent orchestration, task DAG execution, cross-workflow context isolation, distributed mutex locks, and inter-agent pub/sub messaging.

---

## 🛠️ Tools Directory & Use-Case Mapping

| Tool Name | Core Use Case | When Agents Should Use This Tool |
| :--- | :--- | :--- |
| [`wc-swarm-dispatch`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-swarm-dispatch) | Swarm Decision & Dispatch Synthesizer | When deciding whether to launch a subagent vs run locally, generating dispatch prompts, and aggregating outcomes. |
| [`wc-workflow-context`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-workflow-context) | Cross-Workflow Context Isolation | When maintaining state across multiple workflows and handing off discrete context frames between subagents. |
| [`wc-task-dag`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-task-dag) | Multi-Task Dependency DAG Engine | When scheduling parallel or sequential tasks with worker pools and deadlock prevention. |
| [`wc-agent-mesh`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-agent-mesh) | Swarm Role Assignment Coordinator | When assigning subagent roles (`Architect`, `Implementer`, `BuildDoctor`, `Verifier`, `Auditor`). |
| [`wc-agent-channel`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-agent-channel) | Inter-Agent Pub/Sub Event Bus | When subagents need to communicate asynchronously via persistent topic channels (`build:status`, `alerts`). |
| [`wc-resource-lock`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-resource-lock) | Distributed Concurrency Mutex | When guarding shared files, build directories, or SQLite databases against concurrent write races. |
| [`wc-context-pack`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-context-pack) | Context Compression & Deduplication | When feeding noisy compiler logs, stack traces, or logcat dumps into the prompt without token blowout. |
| [`wc-agent-loop`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-agent-loop) | Self-Healing Autonomous Execution Loop | When executing risky multi-step commands with automated snapshot rollback and retry healing. |
| [`wc-agent-probe`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-agent-probe) | Environment & Toolchain Diagnostic Probe | When verifying execution PATH, GitHub CLI auth, memory limits, and Python engines before starting work. |
| [`wc-error-healer`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-error-healer) | Deterministic Error Doctor | When encountering Git 403 permissions, missing shebangs, or SQLite database locks. |

---

## ⚡ Agent Invocation Examples

```bash
# 1. Evaluate whether a task warrants a subagent
wc-swarm-dispatch eval "Broad search across 30 repositories" -e -f 30

# 2. Acquire a distributed mutex before editing build.gradle
wc-resource-lock acquire "gradle_build" -H "BuildDoctor" -t 120

# 3. Transfer build properties between workflows
wc-workflow-context handoff "wf_build" "wf_release" targetSdk compose_version

# 4. Broadcast task completion on the agent pub/sub bus
wc-agent-channel pub "build:status" '{"status": "SUCCESS"}' -s "Builder"
```
