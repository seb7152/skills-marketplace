---
created: 2026-03-29
updated: 2026-03-29
---
# Professional Workflow: 20_Projects

Use this guide when working with professional projects (MEN, The-Link, ENGIE-Lease-Management, etc.).

## Folder Structure

```
20_Projects/
├── MEN/                    # Project name
│   ├── Réunions/          # Meeting notes by date
│   ├── Decisions/         # Project decisions
│   ├── Coding-Notes/      # Technical notes
│   └── ...other types
├── The-Link/
└── ENGIE-Lease-Management/
```

## File Format for Professional Files

```yaml
---
type: meeting-summary         # or: decision, coding-notes, action-items, etc.
project: MEN                  # Project folder name
date: "2026-02-06"           # ISO 8601
title: "COTECH Réunion"       # Human-readable title
summary: "2-3 line summary"   # Plain text, no markdown
status: draft|review|completed|archived
---
## Meeting Content

Notes here...
```

**Standard properties:**
- `type`: File classification (meeting-summary, decision, coding-notes, action-items)
- `project`: Project name (must match folder in 20_Projects/)
- `date`: When created/last updated
- `title`: Display name for the meeting/decision
- `summary`: Concise summary (auto-generated via API or manual)
- `status`: Workflow state (draft → review → completed → archived)

## Common API Operations

### List all meetings in a project
```bash
GET /api/files?type=meeting-summary&project=MEN
```

### Read a specific meeting
```bash
GET /api/file/20_Projects/MEN/Réunions/2026-02-06.md
```

Response includes `frontmatter` (metadata) + `body` (content) separately.

### Update meeting metadata (summary, status)
```bash
PATCH /api/file/20_Projects/MEN/Réunions/2026-02-06.md

{
  "summary": "Key decisions made about workspace design",
  "status": "completed"
}
```

**Why PATCH?** It updates only the frontmatter, preserving the file body. Safe for batch operations.

### Create a new decision file
```bash
POST /api/file/20_Projects/MEN/Decisions/2026-03-29-workspace-upgrade.md

{
  "content": "---\ntype: decision\nproject: MEN\ndate: \"2026-03-29\"\ntitle: \"Upgrade to Smart Workplace\"\nsummary: \"Decision to migrate to Smart Workplace platform\"\nstatus: draft\n---\n## Context\n...\n## Decision\n...\n## Rationale\n..."
}
```

### Search across project
```bash
GET /api/search?q=Smart%20Workplace
```

## Python Patterns

### Batch generate summaries
```python
import requests

BASE_URL = "https://obsidian-api.srv1119889.hstgr.cloud"
TOKEN = "your-token"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Get all MEN meetings without summaries
files = requests.get(
    f"{BASE_URL}/api/files?type=meeting-summary&project=MEN",
    headers=headers
).json()["files"]

# Generate summaries (using OpenAI or similar)
for file in files:
    if not file["frontmatter"].get("summary"):
        # Call LLM API, get summary
        summary = generate_summary(file["body"])

        # Update file
        requests.patch(
            f"{BASE_URL}/api/file/{file['path']}",
            json={"summary": summary},
            headers=headers
        )
```

### Batch update status
```python
import requests

BASE_URL = "https://obsidian-api.srv1119889.hstgr.cloud"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Mark all 2026 meetings as reviewed
files = requests.get(
    f"{BASE_URL}/api/files?type=meeting-summary&project=MEN",
    headers=headers
).json()["files"]

for file in files:
    if "2026-" in file["path"]:
        requests.patch(
            f"{BASE_URL}/api/file/{file['path']}",
            json={"status": "completed", "reviewed_by": "agent"},
            headers=headers
        )
```

## Context: Use MEMORY.md

Before generating summaries or decisions, consult `_system/MEMORY.md`. It contains:
- **Acronyms:** What COTECH, Smart Workplace, PASCAL mean in your context
- **People:** Names and roles of key stakeholders
- **Projects:** Project goals and constraints
- **Historical context:** Important decisions from past meetings

This context helps generate better summaries and avoid repeating past decisions.

## Workflow Rules

See `_system/agent_rules.md` for the complete workflow. Key points:
- Always check if a meeting/decision already exists before creating
- Use consistent date format (ISO 8601: YYYY-MM-DD)
- Keep summaries to 2-3 lines, plain text only
- Status progression: draft → review → completed (or archived if superseded)
