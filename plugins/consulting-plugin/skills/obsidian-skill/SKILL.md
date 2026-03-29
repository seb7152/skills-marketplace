---
name: obsidian-vault
description: Work with the Obsidian vault system. Triggered on any mention of Obsidian, vault operations, file access, or project context retrieval. The vault supports both professional (20_Projects) and personal (10_context/perso) workflows. Always start by reading agent.md to determine workflow type, then consult the appropriate reference guide and API documentation. Covers REST API endpoints, CLI usage, YAML frontmatter format, and key system files.
created: 2026-03-29
updated: 2026-03-29
---

# Obsidian Vault Skill

This skill enables working with the Obsidian vault for both professional project management and personal knowledge capture. The vault is file-based with YAML frontmatter metadata, accessible via REST API or Python scripts.

## Quick Start: Which Path?

**Always start here:** Read `agent.md` in the vault root. It will guide you to:
- **Professional workflows** (MEN, The-Link, ENGIE-Lease-Management projects) → See `references/workflow-professional.md`
- **Personal storage** (notes, aspirations, context) → See `references/workflow-personal.md`

## Vault Structure at a Glance

```
20_Projects/           # Professional: organized by project → type → files
├── MEN/
│   ├── Réunions/
│   ├── Decisions/
│   └── ...
10_context/            # Personal: context and knowledge (agent-managed)
├── perso/             # Personal notes, TODOs, favorites
├── profil.md          # Personal profile (read before each session)
├── aspirations.md     # Goals and aspirations
└── ...
00_inbox/              # Quick capture inbox for unknowns
_system/               # System files: config, API docs, rules
├── agent.md           # START HERE - workflow guide
├── API.md             # Full REST API documentation
├── MEMORY.md          # Context: acronyms, people, projects (read & update)
├── agent_rules.md     # Workflow rules
└── openapi.yaml       # OpenAPI spec
```

## API Basics

All endpoints require Bearer token authentication (except `/health`).

| Endpoint | Purpose |
|----------|---------|
| `GET /api/files?type=X&project=Y` | List files with filtering |
| `GET /api/file/:path` | Read a specific file |
| `PATCH /api/file/:path` | Update frontmatter only |
| `POST /api/file/:path` | Create/overwrite file |
| `GET /api/search?q=query` | Search across vault |

## YAML Frontmatter Format

Every markdown file starts with metadata in YAML:

```yaml
---
type: meeting-summary    # File classification (see references/file-format.md)
project: MEN            # Project name or personal flag
date: "2026-02-06"      # ISO 8601 date
title: "Display Title"
summary: "Brief summary"
status: draft|review|completed|archived
---
File body here...
```

See `references/file-format.md` for all standard properties.

## Reference Files

Consult these based on your workflow:

1. **`agent.md`** (in vault root) — Entry point. Determines professional vs. personal workflow
2. **`references/workflow-professional.md`** — Working with 20_Projects, meetings, decisions, API patterns
3. **`references/workflow-personal.md`** — Storing personal notes in 10_context/perso, using inbox, profil.md
4. **`references/file-format.md`** — YAML frontmatter spec, standard properties, custom fields
5. **`references/key-files.md`** — System files to consult: _system/API.md, MEMORY.md, agent_rules.md
6. **`_system/API.md`** (in vault) — Complete REST API documentation with all endpoints and examples
7. **`_system/openapi.yaml`** (in vault) — OpenAPI spec for code generation

## Authentication

```bash
Authorization: Bearer YOUR_API_TOKEN
```

Set environment variables on server startup:
- `API_TOKEN` — Bearer token
- `VAULT_PATH` — Absolute path to vault
- `PORT` — Server port (default 3000)

## Common Workflows

### Professional: Query MEN meetings
```bash
curl -H "Authorization: Bearer TOKEN" \
  "https://obsidian-api.srv1119889.hstgr.cloud/api/files?type=meeting-summary&project=MEN"
```

### Personal: Create a personal note
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
  -d '{"summary": "New summary", "status": "completed"}' \
  "https://obsidian-api.srv1119889.hstgr.cloud/api/file/20_Projects/MEN/Réunions/2026-02-06.md"
```

## Agent Context Management

**Important:** At the start of each session, the agent MUST:

1. **Read personal context first:** `10_context/profil.md` and `10_context/aspirations.md` — these define who you are and what you're working toward
2. **Read workflow guide:** `agent.md` in vault root — determines professional vs personal context
3. **Read relevant system files:** `_system/MEMORY.md` (for domain context), `_system/agent_rules.md` (for constraints)

**The agent can and should:**
- Create new files in `10_context/perso/` when learning new things about you
- Update `_system/MEMORY.md` with new context, acronyms, or insights discovered
- Add structured notes when you mention something important
- Organize `00_inbox/` into proper files when patterns emerge
- Track decisions, learnings, and observations in the vault

**Structure matters:** All new files must follow YAML frontmatter format and be organized by type/project so the agent can retrieve them later.

## Alternative: CLI Operations

If the REST API is unavailable or you prefer direct file access, use the Obsidian CLI:

```bash
obsidian search query="Smart Workplace"
obsidian files | grep "2026-02"
obsidian read path="20_Projects/MEN/Réunions/2026-02-06.md"
obsidian create path="20_Projects/MEN/file.md" content="..."
```

See `references/cli-operations.md` for complete CLI reference, common patterns, and when to use CLI vs API.

## Next Steps

1. **First time?** Read `agent.md` in the vault to understand workflow
2. **Working professionally?** → `references/workflow-professional.md`
3. **Storing personal content?** → `references/workflow-personal.md`
4. **Agent context enrichment?** → `references/context-building.md` (how agent learns and stores context)
5. **Need detailed API docs?** → `_system/API.md` (full reference)
6. **Using CLI instead?** → `references/cli-operations.md` (Obsidian CLI commands)
7. **Lost?** → `references/key-files.md` (what each system file does)

## Python Integration

Use the `generate_meeting_summaries.py` script as a template for batch operations. Key patterns:

```python
import requests
BASE_URL = "https://obsidian-api.srv1119889.hstgr.cloud"
headers = {"Authorization": f"Bearer {TOKEN}"}

# List files
files = requests.get(f"{BASE_URL}/api/files?project=MEN", headers=headers).json()

# Update file
requests.patch(f"{BASE_URL}/api/file/{path}", json={"summary": "..."}, headers=headers)
```

---

**Remember:** Start with `agent.md`, then follow the appropriate reference guide for your workflow.
