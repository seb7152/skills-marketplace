---
created: 2026-03-29
updated: 2026-03-29
---
# File Format: YAML Frontmatter & Structure

Every markdown file in the vault starts with YAML metadata, followed by body content.

## Template

```yaml
---
type: file-type            # Required. Classification of the file.
project: project-name      # Required. Project name (MEN, The-Link, personal, etc.)
date: "YYYY-MM-DD"        # Required. ISO 8601 date.
title: "Display Title"     # Required. Human-readable title.
summary: "Brief summary"   # Optional. 1-3 line plain text summary.
status: draft              # Optional. Workflow state.
---

## Body Content

This is the actual markdown content below the frontmatter.
```

## Standard Properties

### `type` (Required)

File classification. Choose from:

**Professional files:**
- `meeting-summary` — Meeting notes with decisions and action items
- `decision` — Project decisions and rationale
- `coding-notes` — Technical notes, code snippets, architecture
- `action-items` — Tasks and assignments
- `project-plan` — Project scope, timeline, deliverables
- `resource` — Documentation, guidelines, templates

**Personal files:**
- `personal-note` — General notes
- `personal-todo` — Tasks and action items
- `personal-favorite` — Links, resources, references
- `reflection` — Thoughts, learnings, reflections
- `inbox-item` — Quick capture, unorganized

### `project` (Required)

Which project or context this file belongs to. Examples:
- Professional: `MEN`, `The-Link`, `ENGIE-Lease-Management`
- Personal: `personal`, `coding/Food-thought`, other in 20_Projects/Coding

Used for filtering. Always set correctly.

### `date` (Required)

ISO 8601 format: `YYYY-MM-DD`. When the file was created or last updated.

```yaml
date: "2026-03-29"
date: "2026-02-06"
```

### `title` (Required)

Human-readable display name. Examples:
- `"COTECH Réunion"`
- `"Migrate to Smart Workplace"`
- `"Learning: OAuth Flows"`

### `summary` (Optional)

Brief summary (1-3 lines, plain text, no markdown). Used to quickly understand file content without reading the body.

**Good summary:**
```yaml
summary: "Decided to migrate to Smart Workplace platform by Q2 2026. Budget approved: €50K."
```

**Bad summary:**
```yaml
summary: "# Discuss smart workplace\n\n- **Pros:** Better features\n- **Cons:** Cost"
```

For auto-generated summaries (via API), keep to 2-3 lines, plain text only.

### `status` (Optional, default: `draft`)

Workflow state. Standard values:
- `draft` — In progress, not yet shared
- `review` — Ready for feedback
- `completed` — Done, can be archived
- `archived` — Old, kept for reference

Example progression:
```yaml
status: draft          # Initial creation
status: review         # Ready for team review
status: completed      # Approved and implemented
status: archived       # Superseded or no longer relevant
```

## Custom Properties

You can add any custom properties you need. They'll be preserved when using PATCH to update files.

**Examples:**

```yaml
---
type: meeting-summary
project: MEN
date: "2026-03-29"
title: "COTECH Réunion"
summary: "Smart Workplace migration approved."
status: completed
assigned_to: alice           # Custom: who owns follow-up
attendees: alice, bob, carol  # Custom: participants
duration_minutes: 90         # Custom: meeting length
next_meeting: "2026-04-12"   # Custom: when next scheduled
---
```

Use PATCH to update just the custom fields:

```bash
PATCH /api/file/20_Projects/MEN/Réunions/2026-03-29.md

{
  "assigned_to": "bob",
  "next_meeting": "2026-04-12"
}
```

## Special Cases

### No summary yet (auto-generated later)

When creating a file, summary is optional. API can generate it:

```yaml
---
type: meeting-summary
project: MEN
date: "2026-03-29"
title: "COTECH Réunion"
status: draft
---
```

Then use the generate_meeting_summaries.py script to batch-fill summaries.

### Personal notes (minimal frontmatter)

Personal files can be more minimal:

```yaml
---
type: personal-note
project: personal
date: "2026-03-29"
title: "Learning OAuth"
---
```

`summary` and `status` are optional for personal notes.

### Inbox items (quick capture)

Inbox items can be very minimal while you triage:

```yaml
---
type: inbox-item
project: personal
date: "2026-03-29"
title: "Ideas from standup"
status: draft
---

- Implement OAuth
- Set up MCP
- Document API
```

Later, move sections into properly-typed files.

## API Response Format

When you GET a file via the API, you receive this structure:

```json
{
  "path": "20_Projects/MEN/Réunions/2026-03-29.md",
  "frontmatter": {
    "type": "meeting-summary",
    "project": "MEN",
    "date": "2026-03-29",
    "title": "COTECH Réunion",
    "summary": "Smart Workplace migration approved.",
    "status": "completed",
    "custom_field": "custom_value"
  },
  "body": "## Discussion\n\nWe talked about...",
  "content": "---\ntype: meeting-summary\n...\n---\n## Discussion\n\n..."
}
```

- **`frontmatter`** — Parsed YAML metadata as a JSON object (use for filtering, updating)
- **`body`** — Markdown content without the frontmatter
- **`content`** — Complete file including frontmatter (for display)

## Formatting Rules

- **Always use double quotes** in YAML values: `date: "2026-03-29"` not `date: 2026-03-29`
- **Dates must be ISO 8601** (YYYY-MM-DD): `"2026-03-29"` ✓, `"3/29/26"` ✗
- **Summaries are plain text** — no markdown formatting
- **No special characters in field names** — stick to alphanumeric and hyphens
- **Indentation matters** — YAML uses 2-space indentation

## Migration Notes

When moving files between projects:
- Update the `project` field in frontmatter
- Update the file path if necessary (e.g., move from `20_Projects/MEN/` to `20_Projects/The-Link/`)
- Keep all other properties intact

```bash
PATCH /api/file/20_Projects/The-Link/Decisions/migrate-to-smart-workplace.md

{
  "project": "The-Link"
}
```
