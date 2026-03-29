---
created: 2026-03-29
updated: 2026-03-29
---
# Personal Workflow: 10_context & Inbox

Use this guide when storing personal notes, aspirations, favorites, or context about yourself that the agent should know.

## Folder Structure

```
10_context/
├── perso/                  # Personal notes, TODOs, favorites
│   ├── notes/
│   ├── todos/
│   ├── favorites/
│   └── ...
├── profil.md              # Personal profile (goals, skills, interests)
├── aspirations.md         # Long-term goals
└── ...

00_inbox/                  # Quick capture when unsure where to put something
├── item-1.md
├── item-2.md
└── ...
```

## When to Use Each Folder

- **`10_context/perso/`** — Personal notes you want to keep. Organized by type (notes, todos, favorites)
- **`profil.md`** — About you: skills, background, current role, interests
- **`aspirations.md`** — Goals for the future (career, learning, projects)
- **`00_inbox/`** — Quick capture when you're not sure where it belongs. You can organize it later

## File Format for Personal Files

```yaml
---
type: personal-note           # or: personal-todo, personal-favorite, reflection, etc.
project: personal             # Always "personal" for personal files
date: "2026-03-29"           # When created
title: "Note Title"
summary: "Brief description"  # Optional for personal files
status: draft|active|archived
---
Content here...
```

**When in doubt:** Use `00_inbox/` with a descriptive filename. The agent can organize it later.

## Creating Personal Content

### Quick personal note
```bash
POST /api/file/10_context/perso/notes/learning-MCP.md

{
  "content": "---\ntype: personal-note\nproject: personal\ndate: \"2026-03-29\"\ntitle: \"Learning: MCP Servers\"\nstatus: active\n---\n## What I learned\n\n- MCP enables LLMs to use external tools\n- Can build custom servers\n\n## Next steps\n- Read mcp-builder.md in skill-creator\n- Create my first MCP"
}
```

### Personal TODO
```bash
POST /api/file/10_context/perso/todos/learn-oauth.md

{
  "content": "---\ntype: personal-todo\nproject: personal\ndate: \"2026-03-29\"\ntitle: \"Implement OAuth for API\"\nstatus: active\n---\n- [ ] Research OAuth 2.0 flows\n- [ ] Evaluate libraries\n- [ ] Implement on API server\n- [ ] Test with ChatGPT"
}
```

### Favorite resource
```bash
POST /api/file/10_context/perso/favorites/obsidian-api-docs.md

{
  "content": "---\ntype: personal-favorite\nproject: personal\ndate: \"2026-03-29\"\ntitle: \"Obsidian Vault API\"\nstatus: active\n---\n**URL:** https://obsidian-api.srv1119889.hstgr.cloud/api\n**Token:** stored in env\n**Use case:** Query meetings, update frontmatter\n\n## Useful endpoints\n- GET /api/files - list with filtering\n- PATCH /api/file/:path - update metadata"
}
```

### Reflection or aspiration
```bash
POST /api/file/10_context/aspirations.md

Append to existing file or create section.
```

## Querying Personal Content

### List all personal notes
```bash
GET /api/files?project=personal&type=personal-note
```

### List all TODOs
```bash
GET /api/files?project=personal&type=personal-todo
```

### Search in personal context
```bash
GET /api/search?q=OAuth
```

### Read profil.md
```bash
GET /api/file/10_context/profil.md
```

## Using inbox for quick capture

When you're not sure where something belongs, put it in `00_inbox/`:

```bash
POST /api/file/00_inbox/capture-2026-03-29.md

{
  "content": "---\ntype: inbox-item\nproject: personal\ndate: \"2026-03-29\"\ntitle: \"Need to organize this later\"\nstatus: draft\n---\n- Client feedback about vault structure\n- Idea for OAuth implementation\n- Note about MCP servers\n\nOrganize into proper folders when ready."
}
```

Then, after organizing:
- Move summary into `10_context/perso/notes/`
- Move action items into `10_context/perso/todos/`
- Delete the inbox file

## Updating Personal Content

```bash
PATCH /api/file/10_context/perso/notes/learning-MCP.md

{
  "status": "archived"  # Mark as done
}
```

Or add to existing content:

```bash
PATCH /api/file/10_context/aspirations.md

{
  "summary": "Updated with 2026 Q2 goals"
}
```

## Types for Personal Files

- `personal-note` — General notes
- `personal-todo` — Tasks and action items
- `personal-favorite` — Links, resources, references
- `reflection` — Thoughts, learnings, reflections
- `inbox-item` — Quick capture, organize later
- `project-idea` — Side projects, ideas

## Tips

1. **Always tag personal files with `project: personal`** so they don't mix with professional projects
2. **Use 00_inbox for quick capture** — don't overthink organization in the moment
3. **Review profil.md before generating content about you** — helps tailor notes to your context
4. **Use aspirations.md as north star** — reference when prioritizing personal projects
5. **Keep personal notes separate from work** — they're for your own context, not shared
