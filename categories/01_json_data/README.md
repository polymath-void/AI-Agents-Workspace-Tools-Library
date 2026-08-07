# 📊 Category 01: JSON & Data Processing Suite

Dedicated tools for JSON data manipulation, prompt syntax repair, hierarchical flattening, token minification, schema generation, and tabular format conversion.

---

## 🛠️ Tools Directory & Use-Case Mapping

| Tool Name | Core Use Case | When Agents Should Use This Tool |
| :--- | :--- | :--- |
| [`wc-json-prompt`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-prompt) | Prompt JSON Extractor & Repair | When user prompts contain unquoted keys, single quotes, or unformatted JSON mixed with natural language. |
| [`wc-json-query`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-query) | Precision JSONPath Query | When you only need a specific nested value (e.g. `build.targetSdk`) without loading the whole file into context. |
| [`wc-json-patch`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-patch) | In-Place Atomic Key Modification | When mutating nested JSON configs (`targetSdk = 35`) safely with rollback support. |
| [`wc-json-validate`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-validate) | Schema & Type Validation | When verifying manifest files or extension configs conform to required fields and types. |
| [`wc-json-format`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-format) | Prettifier & Token Minifier | When formatting JSON for human inspection (`-c` colorized) or compressing it for token savings (`-m`). |
| [`wc-json-schema`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-schema) | Auto JSON Schema Generator | When generating standard JSON Schema Draft 7 specifications from arbitrary sample JSON files. |
| [`wc-json-flatten`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-flatten) | Hierarchical Flattener / Unflattener | When converting deeply nested JSON trees to dot notation (`a.b.c: 1`) or un-flattening back. |
| [`wc-json-ndjson`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-ndjson) | JSON Lines / NDJSON Streamer | When streaming large log lines, filtering line-by-line, or converting JSON arrays $\leftrightarrow$ NDJSON. |
| [`wc-json-csv`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-csv) | Tabular Data Converter | When converting tabular datasets between CSV / TSV and structured JSON array records. |
| [`wc-json-stats`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-stats) | Structural & Token Profiler | When inspecting JSON payload nesting depth, total key count, type distribution, and token estimates. |
| [`wc-json-filter`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-filter) | Predicate Array Query Engine | When filtering collections of objects (`age > 25`, `role == 'admin'`, `tags contains 'android'`). |
| [`wc-json-mask`](file:///data/data/com.termux/files/home/AI-Agents-Workspace-Tools-Library/bin/wc-json-mask) | Privacy & Secret Sanitizer | When redacting API keys, authorization tokens, passwords, and emails from JSON payloads. |

---

## ⚡ Agent Invocation Examples

```bash
# 1. Extract and auto-repair broken JSON from conversational chat
wc-json-prompt extract "update: {targetSdk: 35, 'active': True, }"

# 2. Query targetSdk token without loading entire file
wc-json-query "android.defaultConfig.targetSdk" build.json --raw

# 3. Mask sensitive keys in config
wc-json-mask server_config.json -i

# 4. Generate JSON schema
wc-json-schema sample_manifest.json -t "ExtensionManifest"
```
