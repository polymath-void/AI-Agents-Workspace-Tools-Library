import os
import json
from pathlib import Path

TOOLS_CATALOG = [
    # --- UNIFIED JSON SUITE & DATA TRANSFORMATION ---
    {
        "name": "wc-json-format",
        "category": "JSON & Data Processing",
        "description": "High-performance JSON prettifier, colorizer, alphabetical key sorter & dense token minifier.",
        "usage": "wc-json-format [target] [-i indent] [-s] [-m] [-c]",
        "examples": [
            "wc-json-format config.json -s -i 4",
            "wc-json-format package.json -m"
        ]
    },
    {
        "name": "wc-json-schema",
        "category": "JSON & Data Processing",
        "description": "Zero-overhead automatic JSON Schema Draft 7 generator inferred from arbitrary JSON payloads.",
        "usage": "wc-json-schema [target] [-t title]",
        "examples": [
            "wc-json-schema sample.json -t 'UserSchema'",
            "wc-json-schema manifest.json"
        ]
    },
    {
        "name": "wc-json-flatten",
        "category": "JSON & Data Processing",
        "description": "Bidirectional JSON flattener & un-flattener for converting deep object hierarchies to dot-notation keys.",
        "usage": "wc-json-flatten <flatten|unflatten> [target] [-d delimiter]",
        "examples": [
            "wc-json-flatten flatten nested.json",
            "wc-json-flatten unflatten flat.json -d '.'"
        ]
    },
    {
        "name": "wc-json-ndjson",
        "category": "JSON & Data Processing",
        "description": "High-throughput NDJSON (Newline Delimited JSON) / JSONL converter and memory-efficient streaming line filter.",
        "usage": "wc-json-ndjson <to-ndjson|to-json|filter> [target] [-k key] [-v val]",
        "examples": [
            "wc-json-ndjson to-ndjson records.json > records.jsonl",
            "wc-json-ndjson filter records.jsonl -k status -v SUCCESS"
        ]
    },
    {
        "name": "wc-json-csv",
        "category": "JSON & Data Processing",
        "description": "Bidirectional tabular bridge: converts JSON arrays to standard CSV/TSV and parses CSV tables into typed JSON.",
        "usage": "wc-json-csv <to-csv|to-json> [target] [-t]",
        "examples": [
            "wc-json-csv to-csv data.json > data.csv",
            "wc-json-csv to-json table.csv"
        ]
    },
    {
        "name": "wc-json-stats",
        "category": "JSON & Data Processing",
        "description": "Deep structural, depth, type distribution, null ratio & token density profiler for JSON payloads.",
        "usage": "wc-json-stats [target] [--json]",
        "examples": [
            "wc-json-stats response.json",
            "wc-json-stats dataset.json --json"
        ]
    },
    {
        "name": "wc-json-filter",
        "category": "JSON & Data Processing",
        "description": "Predicate expression engine for querying and filtering JSON array collections (==, !=, >, <, contains, startswith).",
        "usage": "wc-json-filter <field> <op> <value> [target] [-m]",
        "examples": [
            "wc-json-filter 'age' '>' '25' users.json",
            "wc-json-filter 'role' '==' 'admin' users.json -m"
        ]
    },
    {
        "name": "wc-json-mask",
        "category": "JSON & Data Processing",
        "description": "Automated security & privacy redactor: scans and masks passwords, API keys, auth tokens, and emails in JSON structures.",
        "usage": "wc-json-mask [target] [-m mask] [-i]",
        "examples": [
            "wc-json-mask payload.json",
            "wc-json-mask server_config.json -i"
        ]
    },
    {
        "name": "wc-json-prompt",
        "category": "JSON & Data Processing",
        "description": "Unformatted prompt JSON extractor, heuristic syntax auto-repairer & dynamic context relevance adjuster.",
        "usage": "wc-json-prompt <extract|intent> [text] [-m]",
        "examples": [
            "wc-json-prompt extract \"update config: {targetSdk: 35, 'active': True, }\"",
            "wc-json-prompt intent \"fix build errors in app/build.gradle\""
        ]
    },
    {
        "name": "wc-json-query",
        "category": "JSON & Data Processing",
        "description": "Lightning-fast dot/bracket JSONPath query & token minifier engine: extracts nested keys and compresses JSON payloads.",
        "usage": "wc-json-query [path_expr] [target] [-m] [--raw]",
        "examples": [
            "wc-json-query 'build.targetSdk' config.json --raw",
            "wc-json-query 'users[0].name' data.json -m"
        ]
    },
    {
        "name": "wc-json-patch",
        "category": "JSON & Data Processing",
        "description": "Atomic JSON modifier, key patcher & deep merger: sets nested paths and merges JSON objects with in-place safety.",
        "usage": "wc-json-patch <set|merge> <file> [args...] [-i]",
        "examples": [
            "wc-json-patch set config.json 'build.targetSdk' 35 -i",
            "wc-json-patch merge manifest.json '{\"version\": \"1.1.0\"}' -i"
        ]
    },
    {
        "name": "wc-json-validate",
        "category": "JSON & Data Processing",
        "description": "Zero-overhead JSON schema validator: checks manifests, extension packages, and agent configs against required types and fields.",
        "usage": "wc-json-validate <target> [schema] [--json]",
        "examples": [
            "wc-json-validate manifest.json manifest",
            "wc-json-validate extension.json extension --json"
        ]
    },

    # --- OBJECT IDENTIFICATION & SEMANTIC COMPARISON ---
    {
        "name": "wc-object-diff",
        "category": "Object Identification & Comparison",
        "description": "Autonomous semantic object comparator & entity identifier: performs deep JSON schema diffs, extracts code symbols, and detects signature drift.",
        "usage": "wc-object-diff <identify|symbols|compare> [args...] [--json]",
        "examples": [
            "wc-object-diff identify package.json",
            "wc-object-diff symbols MainActivity.kt",
            "wc-object-diff compare old_config.json new_config.json --json"
        ]
    },

    # --- MULTI-TASKING & AGENTIVE WORKFLOW SUITE ---
    {
        "name": "wc-swarm-dispatch",
        "category": "Multi-Tasking & Workflows",
        "description": "Subagent swarm evaluation, dispatch payload synthesizer & consensus barrier aggregator.",
        "usage": "wc-swarm-dispatch <eval|spec|aggregate> [args...]",
        "examples": [
            "wc-swarm-dispatch eval 'Broad search of JNI memory buffers' -e -f 20",
            "wc-swarm-dispatch spec 'BuildDoctor' 'Repair Gradle targetSdk' -m flash"
        ]
    },
    {
        "name": "wc-workflow-context",
        "category": "Multi-Tasking & Workflows",
        "description": "Cross-workflow context isolation, token frame manager & selective handoff bus between subagents.",
        "usage": "wc-workflow-context <register|set|get|handoff|prune> [args...]",
        "examples": [
            "wc-workflow-context set wf_build targetSdk 35",
            "wc-workflow-context handoff wf_build wf_package targetSdk",
            "wc-workflow-context get wf_package --json"
        ]
    },
    {
        "name": "wc-task-dag",
        "category": "Multi-Tasking & Workflows",
        "description": "Dependency-aware multi-task DAG executor: runs parallel & sequential tasks with worker pools and deadlock protection.",
        "usage": "wc-task-dag <workflow.json> [-w workers] [-d dir] [--json]",
        "examples": [
            "wc-task-dag workflow.json -w 4",
            "wc-task-dag pipeline.json --json"
        ]
    },
    {
        "name": "wc-agent-mesh",
        "category": "Multi-Tasking & Workflows",
        "description": "Multi-Agent Swarm Coordinator: manages agent swarm roles (Architect, Implementer, Verifier, Auditor) and consensus handoffs.",
        "usage": "wc-agent-mesh <roles|plan|status> [args...]",
        "examples": [
            "wc-agent-mesh roles",
            "wc-agent-mesh plan 'Implement Modular Extension Marketplace'"
        ]
    },
    {
        "name": "wc-agent-channel",
        "category": "Multi-Tasking & Workflows",
        "description": "High-throughput persistent inter-agent pub/sub messaging bus for task completion events, alerts, and payload routing.",
        "usage": "wc-agent-channel <pub|sub|clear> [args...]",
        "examples": [
            "wc-agent-channel pub 'build:status' 'SUCCESS' -s 'BuildDoctor'",
            "wc-agent-channel sub 'build:status' --mark-read"
        ]
    },
    {
        "name": "wc-context-pack",
        "category": "Multi-Tasking & Workflows",
        "description": "Context window & token density compressor: strips ANSI codes, deduplicates traces, and packs multi-task payloads.",
        "usage": "wc-context-pack [files...] [-m max_lines]",
        "examples": [
            "wc-context-pack build.log crash.log -m 30",
            "logcat -d | wc-context-pack"
        ]
    },
    {
        "name": "wc-resource-lock",
        "category": "Multi-Tasking & Workflows",
        "description": "Distributed mutex locking to protect files, databases, and build artifacts from race conditions across subagents.",
        "usage": "wc-resource-lock <acquire|release|status> <resource> [-H holder] [-t ttl]",
        "examples": [
            "wc-resource-lock acquire 'gradle_build' -H 'BuilderAgent' -t 120",
            "wc-resource-lock release 'gradle_build'"
        ]
    },

    # --- AGENT LOOP & AUTONOMY SUITE ---
    {
        "name": "wc-agent-loop",
        "category": "Agent Loop & Autonomy",
        "description": "Unified self-healing agent execution loop with pre-flight probe, rollback snapshots, and retry healing.",
        "usage": "wc-agent-loop <command...> [-d dir] [-t tag] [-r retries] [--json]",
        "examples": [
            "wc-agent-loop git push origin main",
            "wc-agent-loop ./bin/wc-task-exec 'Verify' ."
        ]
    },
    {
        "name": "wc-agent-probe",
        "category": "Agent Loop & Autonomy",
        "description": "Internal agent environment diagnostic probe: audits PATH, GitHub CLI auth, memory limits, and Python engines.",
        "usage": "wc-agent-probe [--json]",
        "examples": [
            "wc-agent-probe",
            "wc-agent-probe --json"
        ]
    },
    {
        "name": "wc-error-healer",
        "category": "Agent Loop & Autonomy",
        "description": "Deterministic self-healing error doctor: remediates Git 403s, missing Termux shebangs, and SQLite database locks.",
        "usage": "wc-error-healer [error_text] [--fix-path]",
        "examples": [
            "wc-error-healer --fix-path",
            "wc-error-healer 'Permission to user/repo.git denied'"
        ]
    },

    # --- TASK PIPELINE & REFACTORING ---
    {
        "name": "wc-task-exec",
        "category": "Task Automation",
        "description": "Executes complete multi-phase task validation pipelines (environment, dependencies, health audit, tests) and generates receipts.",
        "usage": "wc-task-exec [task_title] [path] [--json]",
        "examples": [
            "wc-task-exec 'Refactor App Drawer Context Menu' .",
            "wc-task-exec 'Verify Launcher Build' ~/repo/Piuu-Unified-Launcher-Android"
        ]
    },
    {
        "name": "wc-code-mod",
        "category": "Code Refactoring",
        "description": "Atomic multi-file code modifier, regex replacer, and import injector with automatic safety backups and rollback.",
        "usage": "wc-code-mod <replace|import> [args...] [-e ext] [-d]",
        "examples": [
            "wc-code-mod replace 'oldMethod()' 'newMethod()' . -e kt --dry-run",
            "wc-code-mod import 'import com.piuu.launcher.utils.*' . -e kt"
        ]
    },
    {
        "name": "wc-build-doctor",
        "category": "Build & Self-Healing",
        "description": "Self-healing build doctor: analyzes Gradle/Android configs (targetSdk, composeOptions, 16KB alignment) and auto-repairs scripts.",
        "usage": "wc-build-doctor [path] [--fix]",
        "examples": [
            "wc-build-doctor ~/repo/Piuu-Unified-Launcher-Android",
            "wc-build-doctor . --fix"
        ]
    },
    {
        "name": "wc-bundle-packer",
        "category": "Packaging & Release",
        "description": "End-to-end packager: compiles .piuu extension bundles, auto-generates manifest.json, and computes SHA256 hashes.",
        "usage": "wc-bundle-packer <pack|verify> [args...]",
        "examples": [
            "wc-bundle-packer pack ./my-extension dist/my-extension.piuu --name 'Clock Widget'",
            "wc-bundle-packer verify dist/my-extension.piuu"
        ]
    },
    {
        "name": "wc-benchmark",
        "category": "Performance & Latency",
        "description": "Execution benchmark and battery-friendly latency scorecard runner with pass/fail performance thresholds.",
        "usage": "wc-benchmark <command...> [-n runs] [-t max_seconds]",
        "examples": [
            "wc-benchmark python3 -m unittest tests/test_all.py -n 5 -t 1.0",
            "wc-benchmark ./bin/wc-scan . -n 3"
        ]
    },
    {
        "name": "wc-agent-memory",
        "category": "Agent Memory & State",
        "description": "Persistent SQLite storage for agent decisions, architectural preferences, and directory rollback snapshots.",
        "usage": "wc-agent-memory <set|get|list|snapshot|snapshots> [args...]",
        "examples": [
            "wc-agent-memory set 'battery_rule' 'prioritize light builds' -c 'rules'",
            "wc-agent-memory snapshot ~/repo/Piuu-Unified-Launcher-Android -t 'pre-refactor'"
        ]
    },
    {
        "name": "wc-contract-check",
        "category": "Cross-Language Contracts",
        "description": "Cross-language contract verifier for Kotlin external fun JNI signatures, POSIX C exports, and Electron IPC APIs.",
        "usage": "wc-contract-check [path] [--json]",
        "examples": [
            "wc-contract-check ~/repo/Piuu-Unified-Launcher-Android",
            "wc-contract-check . --json"
        ]
    },
    {
        "name": "wc-scaffold",
        "category": "Code Scaffolding",
        "description": "Zero-overhead component generator for Jetpack Compose UI, Kotlin StateFlow repositories, and extension bundles.",
        "usage": "wc-scaffold <compose|repo|extension> [args...]",
        "examples": [
            "wc-scaffold compose app/src/main/java/com/piuu/launcher/ui/components/NewCard.kt",
            "wc-scaffold repo app/src/main/java/com/piuu/launcher/repository/ThemeRepository.kt"
        ]
    },
    {
        "name": "wc-crash-doctor",
        "category": "Diagnostics & Crashes",
        "description": "Parses Android logcat, stacktraces, SIGSEGV signals, and build traces to isolate root-cause exception lines.",
        "usage": "wc-crash-doctor [log_file] [--json]",
        "examples": [
            "wc-crash-doctor crash.log",
            "logcat -d | wc-crash-doctor"
        ]
    },

    # --- WORKSPACE CONTEXT & INSPECTION SUITE ---
    {
        "name": "wc-tool-registry",
        "category": "Meta & Discovery",
        "description": "Interactive registry index providing instant capability discovery and zero-overhead invocation recipes.",
        "usage": "wc-tool-registry [category|tool_name] [--json]",
        "examples": [
            "wc-tool-registry",
            "wc-tool-registry --json"
        ]
    },
    {
        "name": "wc-search",
        "category": "Inspection & Search",
        "description": "Context-aware lightning-fast symbol, regex, and text finder that automatically ignores build/cache noise directories.",
        "usage": "wc-search <query> [path] [-e ext] [-C lines] [--json]",
        "examples": [
            "wc-search 'wallpaperTransparency' . -e kt,xml",
            "wc-search 'class .*ViewModel' . -r -e kt"
        ]
    },
    {
        "name": "wc-deps",
        "category": "Dependencies & Packages",
        "description": "Multi-ecosystem dependency manifest analyzer for Android Gradle, Node NPM, Python, and Rust Cargo.",
        "usage": "wc-deps [directory] [--json]",
        "examples": [
            "wc-deps .",
            "wc-deps ~/repo/Piuu-Unified-Launcher-Android --json"
        ]
    },
    {
        "name": "wc-git-sync",
        "category": "Git & CI/CD",
        "description": "Multi-branch synchronizer (e.g. main <-> master unified path) and fast working tree status inspector.",
        "usage": "wc-git-sync <status|sync> [dir] [src] [target]",
        "examples": [
            "wc-git-sync status .",
            "wc-git-sync sync . main master"
        ]
    },
    {
        "name": "wc-termux-env",
        "category": "Android & Termux System",
        "description": "Inspects Android/Termux hardware telemetry (RAM, CPU load), verified toolchains (clang, python, git), and fixes shebangs.",
        "usage": "wc-termux-env <status|toolchains|fix-shebangs> [dir]",
        "examples": [
            "wc-termux-env status",
            "wc-termux-env toolchains"
        ]
    },
    {
        "name": "wc-scan",
        "category": "Inspection & Architecture",
        "description": "Recursively scans workspace directory tree, builds resilient JSON maps, and computes aggregate file/dir metrics.",
        "usage": "wc-scan <directory> [output_json]",
        "examples": [
            "wc-scan .",
            "wc-scan ~/repo/Piuu-Unified-Launcher-Android metadata.json"
        ]
    },
    {
        "name": "wc-analyze",
        "category": "Code Quality & Complexity",
        "description": "Calculates cyclomatic complexity, lines of code (LOC), functions, and structural metrics for codebase files.",
        "usage": "wc-analyze <complexity|metrics|summary> [directory]",
        "examples": [
            "wc-analyze summary .",
            "wc-analyze metrics ./lib"
        ]
    },
    {
        "name": "wc-manage",
        "category": "Workspace Maintenance",
        "description": "Safely sanitizes build artifacts, temporary logs, and orphan caches with protected root bounds and dry-run preview.",
        "usage": "wc-manage sanitize <directory> <pattern1> [pattern2...] [--dry-run]",
        "examples": [
            "wc-manage sanitize . '*.tmp' '*.bak' --dry-run"
        ]
    },
    {
        "name": "wc-monitor",
        "category": "Health & Anomaly Detection",
        "description": "Continuously audits workspace health against complexity limits, large file bounds, and forbidden patterns.",
        "usage": "wc-monitor <root_path> [config_path]",
        "examples": [
            "wc-monitor .",
            "wc-monitor ~/repo/Piuu-Unified-Launcher-Android config/workspace-health.json"
        ]
    },
    {
        "name": "wc-cloud-backup",
        "category": "Disaster Recovery & Backup",
        "description": "Autonomous incremental compressed snapshot creator, SHA-256 integrity ledger & Google Drive disaster recovery sync manager.",
        "usage": "wc-cloud-backup <backup|list|status> [-t target] [-d dest] [--dry-run] [-f]",
        "examples": [
            "wc-cloud-backup backup -t agy",
            "wc-cloud-backup list",
            "wc-cloud-backup status"
        ]
    },
    {
        "name": "wc-skill-pack",
        "category": "Workflow & Swarm Orchestration",
        "description": "Automated SKILL.md linter, YAML frontmatter validator, AST toolchain dependency validator and .skill bundle packager.",
        "usage": "wc-skill-pack <lint|pack|unpack> <target> [-o output] [-d dest]",
        "examples": [
            "wc-skill-pack lint ~/skills-workspace/user-skills/piuu-c-native-core/SKILL.md",
            "wc-skill-pack pack ~/skills-workspace/user-skills/workspace-context-helper",
            "wc-skill-pack unpack package.skill -d /tmp/extracted_skill"
        ]
    },
    {
        "name": "wc-elf-align",
        "category": "Android & Termux System",
        "description": "Android 15 & 16 (API 36) 16KB memory page-alignment ELF binary analyzer, segment inspector and linker flag auditor.",
        "usage": "wc-elf-align <inspect|flags> [target]",
        "examples": [
            "wc-elf-align inspect libpiuu_core.so",
            "wc-elf-align inspect /path/to/apk/lib/arm64-v8a",
            "wc-elf-align flags"
        ]
    },
    {
        "name": "wc-adb-bridge",
        "category": "Android & Termux System",
        "description": "Termux & Linux wireless ADB connection manager, port discovery, remote shell execution and framebuffer screencap tool.",
        "usage": "wc-adb-bridge <devices|pair|connect|shell|screencap|telemetry> [args]",
        "examples": [
            "wc-adb-bridge devices",
            "wc-adb-bridge pair 192.168.1.100:37891 123456",
            "wc-adb-bridge screencap phone_screen.png",
            "wc-adb-bridge telemetry"
        ]
    },
    {
        "name": "wc-kernel-builder",
        "category": "Android & Termux System",
        "description": "Android GKI Linux Kernel compilation manager, defconfig auditor, AnyKernel3 zip flasher compiler & Image header verifier.",
        "usage": "wc-kernel-builder <check-env|audit-config|verify-image|anykernel-pack> [args]",
        "examples": [
            "wc-kernel-builder check-env",
            "wc-kernel-builder audit-config arch/arm64/configs/gki_defconfig",
            "wc-kernel-builder verify-image out/arch/arm64/boot/Image",
            "wc-kernel-builder anykernel-pack Image -o Kernel-Flashable.zip"
        ]
    },
    {
        "name": "wc-hermes-adapter",
        "category": "Workflow & Swarm Orchestration",
        "description": "Multi-agent protocol translator bridging Hermes JSON sessions, Antigravity AGY JSONL logs & Gemini CLI transcripts.",
        "usage": "wc-hermes-adapter <to-hermes|to-agy|inspect> <input_file>",
        "examples": [
            "wc-hermes-adapter to-hermes transcript.jsonl > hermes_session.json",
            "wc-hermes-adapter to-agy hermes_session.json > transcript.jsonl",
            "wc-hermes-adapter inspect transcript.jsonl"
        ]
    },
    {
        "name": "wc-electron-runner",
        "category": "Code Quality & Complexity",
        "description": "Headless Electron IPC bridge mock validator, preload context test harness and extension studio bundle simulator.",
        "usage": "wc-electron-runner <audit-security|audit-ipc|simulate-bundle> [target]",
        "examples": [
            "wc-electron-runner audit-security main.js",
            "wc-electron-runner audit-ipc main.js -p preload.js",
            "wc-electron-runner simulate-bundle my_extension.piuu"
        ]
    },
    {
        "name": "wc-agy-session",
        "category": "JSON & Data Processing",
        "description": "Antigravity AGY session transcript analyzer, token density counter, tool call profiler and Markdown timeline exporter.",
        "usage": "wc-agy-session <stats|timeline> <transcript.jsonl> [-o output.md]",
        "examples": [
            "wc-agy-session stats ~/.gemini/antigravity-cli/brain/*/logs/transcript.jsonl",
            "wc-agy-session timeline transcript.jsonl -o session_summary.md"
        ]
    }
]

def get_registry_catalog(filter_query=None):
    if not filter_query or filter_query == "--json":
        return TOOLS_CATALOG

    query = filter_query.lower()
    return [
        t for t in TOOLS_CATALOG
        if query in t["name"].lower() or query in t["category"].lower() or query in t["description"].lower()
    ]
