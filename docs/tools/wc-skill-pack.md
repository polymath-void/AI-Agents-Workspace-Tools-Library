# `wc-skill-pack`

## Overview
`wc-skill-pack` is an automated validation, linting, packaging, and unpacking utility for AI Agent Skills. It parses YAML frontmatter without external yaml dependencies, enforces naming standards, audits referenced CLI tools against the tools registry, and builds tamper-proof `.skill` packages with SHA-256 sidecar manifests.

## Category & Classification
- **Category**: `02_workflow_swarm` (Workflow & Swarm Orchestration)
- **Runtime**: Pure Python 3
- **Dependencies**: None (Standard Library)

## CLI Usage
```bash
wc-skill-pack <lint|pack|unpack> <target> [-o output] [-d dest]
```

### Subcommands
- `lint <file_or_dir>`: Checks YAML frontmatter attributes (`name`, `description`), markdown structure, backtick formatting, and referenced tools.
- `pack <skill_dir> [-o output.skill]`: Compresses skill folder into `.skill` package with embedded SHA-256 manifest.
- `unpack <bundle.skill> -d <dest_dir>`: Unpacks `.skill` package and verifies extracted files.

## Associated Skills
- `ai-agent-skill-crafting`
- `skill-creator`
- `workspace-context-helper`

## Example Agent Invocation
```bash
wc-skill-pack lint ~/skills-workspace/user-skills/piuu-c-native-core/SKILL.md
```
