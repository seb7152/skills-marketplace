---
name: obsidian
description: Execute Obsidian vault operations via CLI (list files, search content, read/write/delete files). Use this skill whenever you need to query or modify the vault - list porteurs or themes, search for tags, read/update meeting notes, check file existence, or perform bulk operations. This skill executes CLI commands directly.
compatibility: Requires Obsidian 1.12.4+ with CLI enabled, bash/shell environment
---

## Overview

This skill executes Obsidian CLI commands to query and modify your vault. Use it directly for any vault operation:
- List directory contents (porteurs, themes, réunions)
- Search for tags or content patterns
- Read/write/delete files
- Check file existence
- Extract data for processing

The Obsidian CLI operates as a "remote control" for a running Obsidian app — Obsidian does not need to be in the foreground, but it must be running.

## How to Use This Skill

### When You Need To...

**List all files in vault:**
```bash
obsidian files
```
Returns full list of all files. Pipe to `grep` to filter.

**Search vault for text, tags, or names:**
```bash
obsidian search query="POL GPON"
obsidian search query="Julien Prévost"
obsidian search query="#MEN_coproj"
```
Returns files matching the query.

**Search with context (surrounding lines):**
```bash
obsidian search:context query="POL GPON" path="SIA/Projets/MEN/Réunions"
```
Returns matches with surrounding line context.

**List all tags in vault:**
```bash
obsidian tags
```
Returns list of all tags with occurrence counts.

**Read file content:**
```bash
obsidian read path="SIA/Projets/MEN/MEN - Index.md"
```
Returns full file content as plain text.

**Create a new file:**
```bash
obsidian create path="SIA/Projets/MEN/Réunions/2026-02-06 - COTECH.md" content="your content here"
```
Parent directories are auto-created. Content can include YAML frontmatter.

**Append content to a file:**
```bash
obsidian append path="SIA/Projets/MEN/Réunions/2026-02-06 - COTECH.md" content="additional content"
```

**Delete a file:**
```bash
obsidian delete path="SIA/Projets/MEN/Réunions/old-meeting.md"
```

**Move or rename a file:**
```bash
obsidian move path="SIA/Projets/MEN/Réunions/old.md" to="SIA/Projets/MEN/Réunions/new.md"
```

**Check if file exists:**
```bash
obsidian files | grep "2026-02-06 - COTECH.md"
```
If no output, file doesn't exist.

## Common Patterns

**Extract porteur names from directory:**
```bash
obsidian vault ls --path "SIA/Projets/MEN/Porteurs" | grep -oE '[^/]+\.md$' | sed 's/\.md$//'
```

**Get all #MEN_* tags (unique):**
```bash
obsidian vault search "#MEN_" | grep -oE '#MEN_\w+' | sort -u
```

**Check if theme/directory exists:**
```bash
obsidian vault ls --path "SIA/Projets/MEN/Thématiques" | grep "Projet Pascal"
```

**Update file by reading, modifying, then writing:**
1. Read: `obsidian file read "path/to/file.md"`
2. Modify content locally
3. Write back: `obsidian file write "path/to/file.md" --content "new content"`

## Output Parsing

**Extract file names from `vault ls`:**
Use `grep` or `sed` to parse the output — typically one file per line.

**Parse tags from search results:**
Use `grep -oE '#\w+'` to isolate hashtags.

**Check existence:**
Empty output from `vault ls` means file/directory doesn't exist.

## Key Notes

- **Paths are relative to vault root** — not the filesystem. Example: `SIA/Projets/MEN/Réunions/` not `/Users/.../OneDrive/.../Réunions/`
- **Commands are synchronous** — they block until completion
- **Parent directories auto-created** — no need to mkdir before `file write`
- **Wiki-links not auto-updated** — you must include `[[...]]` syntax in the content you write
- **Obsidian must be running** — the CLI will auto-launch if not, but needs the app installed

## Troubleshooting

- **"Obsidian is not running"** → CLI auto-launches; ensure Obsidian is installed
- **"Permission denied"** → Check vault path and read/write permissions
- **"File not found"** → Verify path is correct and relative to vault root; use `vault ls` to check existence first
