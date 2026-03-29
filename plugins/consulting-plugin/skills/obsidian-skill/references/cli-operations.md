# CLI Operations: Alternative to REST API

While the REST API is the primary way to interact with the vault, you can also use the Obsidian CLI for direct file operations when the API is unavailable or for batch operations.

## When to Use CLI vs API

| Task | CLI | API |
|------|-----|-----|
| List files | ✓ Fast | ✓ Better filtering |
| Search content | ✓ Fast | ✓ Built-in |
| Read single file | ✓ Good | ✓ With parsing |
| Bulk operations | ✓ Via scripts | ✓ Batch updates |
| Create/update files | ✓ Direct | ✓ Structured |
| Check file exists | ✓ Quick | ✓ Reliable |

**Prefer API** for structured operations (querying by type/project, batch updates).
**Use CLI** for quick checks or when you need raw access.

## Prerequisites

- Obsidian app running (CLI auto-launches if not)
- Bash/shell environment
- CLI enabled in Obsidian

## Common CLI Commands

### List all files
```bash
obsidian files
```

Filter results:
```bash
obsidian files | grep "2026-02"           # Files from 2026 February
obsidian files | grep "Réunions"          # All meetings
obsidian files | grep "MEN" | grep "2026" # MEN meetings in 2026
```

### Search for content, tags, or patterns
```bash
obsidian search query="POL GPON"
obsidian search query="#MEN_workspace"
obsidian search query="Smart Workplace"
```

Search with context (surrounding lines):
```bash
obsidian search:context query="COTECH" path="20_Projects/MEN/Réunions"
```

### List all tags in vault
```bash
obsidian tags
```

Extract unique project tags:
```bash
obsidian tags | grep "#MEN" | cut -d' ' -f1 | sort -u
```

### Read file content
```bash
obsidian read path="20_Projects/MEN/Réunions/2026-02-06.md"
```

Read and extract just the body (skip frontmatter):
```bash
obsidian read path="20_Projects/MEN/Réunions/2026-02-06.md" | tail -n +10
```

### Create a new file
```bash
obsidian create path="20_Projects/MEN/Réunions/2026-03-29-cotech.md" \
  content="---
type: meeting-summary
project: MEN
date: \"2026-03-29\"
title: \"COTECH Réunion\"
---

## Topics Discussed
- Smart Workplace migration
- Budget allocation"
```

Parent directories are auto-created.

### Append to a file
```bash
obsidian append path="20_Projects/MEN/Réunions/2026-03-29-cotech.md" \
  content="

## Decisions
- Approved migration to Smart Workplace"
```

### Delete a file
```bash
obsidian delete path="20_Projects/MEN/Réunions/old-meeting.md"
```

### Move or rename a file
```bash
obsidian move path="20_Projects/MEN/old-name.md" \
  to="20_Projects/MEN/new-name.md"
```

### Check if file exists
```bash
obsidian files | grep "2026-02-06.md"
```

If no output, file doesn't exist.

## Common Patterns

### Get all porteur names from a directory
```bash
obsidian files | grep "20_Projects/MEN/Porteurs" | sed 's/.*\///' | sed 's/\.md$//'
```

### Find all files tagged with #MEN_*
```bash
obsidian search query="#MEN_" | grep -oE '#MEN_[a-zA-Z0-9_]+' | sort -u
```

### Check if a theme folder exists
```bash
obsidian files | grep "20_Projects/MEN/Thématiques/Projet.*Pascal"
```

### Get list of meetings from a specific month
```bash
obsidian files | grep "20_Projects/MEN/Réunions/2026-03"
```

### Extract all decision files
```bash
obsidian files | grep "Decisions" | head -20
```

## Parsing Output

### Extract file names from listing
```bash
obsidian files | grep "MEN" | sed 's/.*\///'  # Just filenames
```

### Get paths and filter by date
```bash
obsidian files | grep "2026-02-"  # All files from Feb 2026
```

### Count files by project
```bash
obsidian files | grep "20_Projects" | grep -oE 'MEN|The-Link|ENGIE' | sort | uniq -c
```

### Parse tags and their occurrences
```bash
obsidian tags | sort -k2 -rn | head -20  # Top 20 most used tags
```

## Key Notes

### Paths are relative to vault root
```bash
# ✓ Correct
obsidian read path="20_Projects/MEN/Réunions/2026-02-06.md"

# ✗ Wrong (absolute path)
obsidian read path="/Users/seb/Documents/myVault/20_Projects/..."
```

### Parent directories auto-created
```bash
# This works even if 20_Projects/MEN/NewFolder doesn't exist yet
obsidian create path="20_Projects/MEN/NewFolder/new-file.md" content="..."
```

### Wiki-links must be included in content
If you want to reference other files, include `[[...]]` syntax in the content:

```bash
obsidian create path="20_Projects/MEN/file.md" \
  content="See also: [[other-file.md]]"
```

### Frontmatter must be valid YAML
When creating files with `obsidian create`, ensure YAML is properly formatted:

```bash
# ✓ Valid
content="---
type: meeting-summary
project: MEN
date: \"2026-02-06\"
---"

# ✗ Invalid (missing quotes around date)
content="---
type: meeting-summary
date: 2026-02-06
---"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Obsidian is not running" | CLI auto-launches; ensure Obsidian app is installed |
| "Permission denied" | Check vault path and read/write permissions |
| "File not found" | Verify path is correct and relative to vault root; use `obsidian files` to check |
| "Invalid YAML" | Ensure frontmatter uses proper YAML syntax (quotes around dates) |
| "Path not found" | Parent directories must exist; use `obsidian files` to verify structure |

## CLI vs API Comparison

When should you use CLI over API?

**Use CLI when:**
- You need a quick directory listing
- You're checking file existence
- You want raw file content without parsing
- You're in a context where the API isn't available
- You're doing a one-off operation

**Use API when:**
- You need structured filtering (by type, project)
- You're doing batch operations
- You want frontmatter parsed automatically
- You need to update only metadata (PATCH)
- You're building a script or automation

**Example: Mixed approach**
```bash
# Use CLI to find all 2026 meetings
files=$(obsidian files | grep "Réunions/2026-02")

# Use API to read and update each
for file in $files; do
  curl -H "Authorization: Bearer TOKEN" \
    "https://obsidian-api.srv1119889.hstgr.cloud/api/file/$file" \
    | jq '.frontmatter' > /tmp/meta.json

  # Modify metadata
  # ...

  curl -X PATCH \
    -H "Authorization: Bearer TOKEN" \
    -H "Content-Type: application/json" \
    -d @/tmp/meta.json \
    "https://obsidian-api.srv1119889.hstgr.cloud/api/file/$file"
done
```
