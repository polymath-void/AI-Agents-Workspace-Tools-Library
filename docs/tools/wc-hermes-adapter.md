# `wc-hermes-adapter`

## Overview
`wc-hermes-adapter` is a cross-agent communication and session schema bridge. It translates Antigravity AGY conversation logs (`transcript.jsonl`) into Hermes agent JSON sessions, converts Hermes payloads back into AGY step records, and computes message density telemetry.

## Category & Classification
- **Category**: `02_workflow_swarm` (Workflow & Swarm Orchestration)
- **Runtime**: Pure Python 3
- **Dependencies**: None (Standard Library)

## CLI Usage
```bash
wc-hermes-adapter <to-hermes|to-agy|inspect> <input_file>
```

### Subcommands
- `to-hermes <transcript.jsonl>`: Converts AGY JSONL logs to normalized Hermes message protocol.
- `to-agy <hermes.json>`: Converts Hermes session format to AGY transcript records.
- `inspect <file>`: Analyzes turns, agent roles, and tool invocation counts.

## Associated Skills
- `workspace-context-helper`
- `ai-agent-skill-crafting`

## Example Agent Invocation
```bash
wc-hermes-adapter to-hermes ~/.gemini/antigravity-cli/brain/*/logs/transcript.jsonl > hermes_session.json
```
