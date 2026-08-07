# `wc-agy-session`

## Overview
`wc-agy-session` is an Antigravity AGY session transcript analyzer and token metrics inspector. It parses `transcript.jsonl` and `transcript_full.jsonl` files, counts message types and tokens, profiles tool calls and subagents spawned, and exports human-readable Markdown timeline summaries.

## Category & Classification
- **Category**: `01_json_data` (JSON & Data Processing)
- **Runtime**: Pure Python 3 & JSONL Parser
- **Dependencies**: None (Standard Library)

## CLI Usage
```bash
wc-agy-session <stats|timeline> <transcript.jsonl> [-o output.md]
```

### Subcommands
- `stats <transcript.jsonl>`: Calculates total steps, token approximations, tool calls, and subagent spawns.
- `timeline <transcript.jsonl> [-o output.md]`: Exports structured Markdown timeline report of conversation history.

## Associated Skills
- `antigravity-guide`
- `antigravity-support`
- `workspace-context-helper`

## Example Agent Invocation
```bash
wc-agy-session stats ~/.gemini/antigravity-cli/brain/*/logs/transcript.jsonl
```
