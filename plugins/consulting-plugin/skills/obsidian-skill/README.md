---
created: 2026-03-29
updated: 2026-03-29
---
# Obsidian Vault Skill

This is a complete skill for working with the Obsidian vault system via REST API, Python scripts, or CLI.

## Structure

```
obsidian-skill/
├── SKILL.md                         # Main skill file - start here
├── references/
│   ├── workflow-professional.md     # Guide for 20_Projects
│   ├── workflow-personal.md         # Guide for 10_context/perso
│   ├── context-building.md          # How agent learns and stores context
│   ├── file-format.md               # YAML frontmatter spec
│   ├── key-files.md                 # What each system file does
│   ├── cli-operations.md            # Obsidian CLI alternative to API
│   └── README.md                    # This file
```

## Installation

Copy the entire `obsidian-skill/` folder to your `.claude/skills/` directory, or package as `.skill` file for distribution.

## Quick Start

1. Read `SKILL.md` - it will guide you to the right reference
2. Read `agent.md` in the vault root - determines professional vs personal workflow
3. Choose the appropriate reference guide:
   - Professional projects? → `references/workflow-professional.md`
   - Personal storage? → `references/workflow-personal.md`

## What This Skill Covers

- **REST API** — Querying, filtering, creating, updating files with structured filtering
- **Obsidian CLI** — Alternative direct file access via command line
- **YAML Frontmatter** — File format and metadata structure
- **Workflows** — Professional (20_Projects) and personal (10_context/perso)
- **Context Building** — How agents learn and remember user context across sessions
- **Python integration** — Batch operations, script patterns
- **Key system files** — What to read when, and why

## Key Files to Know

Inside the vault:
- `agent.md` - Entry point and workflow guide
- `_system/API.md` - Complete API documentation
- `_system/MEMORY.md` - Context and domain knowledge
- `_system/agent_rules.md` - Workflow rules and conventions
- `_system/openapi.yaml` - OpenAPI spec for code generation

## Authentication

All API endpoints require Bearer token authentication:

```bash
Authorization: Bearer YOUR_API_TOKEN
```

## Examples

### List professional meetings
```bash
curl -H "Authorization: Bearer TOKEN" \
  "https://obsidian-api.srv1119889.hstgr.cloud/api/files?type=meeting-summary&project=MEN"
```

### Create personal note
```bash
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "---\ntype: personal-note\nproject: personal\ndate: \"2026-03-29\"\ntitle: \"My Note\"\n---\nContent here"}' \
  "https://obsidian-api.srv1119889.hstgr.cloud/api/file/10_context/perso/my-note.md"
```

### Update only metadata
```bash
curl -X PATCH -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"summary": "Brief summary", "status": "completed"}' \
  "https://obsidian-api.srv1119889.hstgr.cloud/api/file/20_Projects/MEN/Réunions/2026-03-29.md"
```

See `references/workflow-professional.md` for more patterns and Python examples.
