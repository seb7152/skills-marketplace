---
name: granola-to-obsidian-men
description: Import Granola meeting notes into MEN Obsidian vault with automatic tagging, porteur linking, and index updates. Use this whenever the user wants to import meetings from Granola (by name, date range, or project folder) into the SIA/Projets/MEN Obsidian vault. The skill handles everything automatically after user confirmation - extracting meeting details, detecting porteurs and themes, creating properly formatted meeting notes with YAML frontmatter, and updating the MEN Index. This is the primary tool for feeding the MEN knowledge base with Granola data.
compatibility: Requires Granola API access (via MCP), Obsidian CLI, fuzzy string matching
---

## Overview

This skill automates the entire workflow of importing Granola meetings into the MEN Obsidian vault:

1. **Search Granola** - Find meetings by name, date range, or folder
2. **List & Confirm** - Show meetings in a table, user selects which to import
3. **Auto-create** - For each confirmed meeting:
   - Extract Granola data
   - Detect porteurs (fuzzy match against `SIA/Projets/MEN/Porteurs/`)
   - Deduce meeting type from context
   - Fetch existing #MEN_* tags from vault
   - Link relevant themes
   - Create markdown file in `SIA/Projets/MEN/Réunions/`
   - Update `MEN - Index.md`
4. **Summarize** - Report what was created

## Understanding User Intent

The user expresses their intent naturally:
- "Import MEN meetings from February 20-24"
- "Get the Smart Workplace meeting from Granola"
- "Grab all MEN meetings from last week"
- "Import meetings from the MEN folder"

The skill interprets date ranges, folder names, meeting titles, and "last week" / "this month" patterns to query Granola.

## Step 1: Search and List Meetings

Use the Granola API (via MCP) to fetch meetings matching the user's query:
- If user mentions dates: use `list_meetings` with time_range (custom, last_week, this_month, etc.)
- If user mentions a project/folder: query with filters for "MEN*" if not explicit
- If user names a specific meeting: search by title

Return a **numbered table** showing:
| # | Title | Date | Participants | Meeting Type |
|---|-------|------|--------------|--------------|

Example:
| 1 | Smart Workplace | 2026-02-06 | Sébastien, Jalal | point-apd |
| 2 | COTECH | 2026-02-06 | Sébastien | cotech |

Present this table to the user and ask: **"Import these meetings? Reply 'ok' or 'ok except 2,5'"**

## Step 2: User Confirmation

Wait for the user's response:
- "ok" → import all
- "ok except 1,3,5" → import all except those numbers
- "just 2,4" → import only those
- Or any other explicit instruction

Extract the list of meeting IDs to process.

## Step 3: Auto-Import Each Meeting

For each confirmed meeting ID:

### 3a. Fetch Full Meeting Details from Granola
Use `get_meetings` to retrieve:
- Full summary/description
- List of participants (by name when available)
- Date and time

### 3b. Detect Porteurs (Fuzzy Match)

**Why:** A meeting may mention porteurs of actions implicitly (e.g., "Julien will handle network arbitrage"). We match names against existing porteur files to create wiki-links.

**How:**
1. Use Obsidian CLI: `obsidian vault ls --path "SIA/Projets/MEN/Porteurs"` → list all porteur files
2. Extract all capitalized names/phrases from meeting summary that look like person names
3. For each candidate, fuzzy-match against porteur file names (e.g., "Julien" → "Julien Prévost.md")
4. Use 80%+ similarity threshold (e.g., Levenshtein distance or similar-text library)
5. Collect matched porteurs

**Example:**
- Meeting mentions "Julien confirmed..." → matches "Julien Prévost.md"
- Meeting mentions "Muriel to follow up" → matches "Muriel.md"
- Add to `themes:` as `[[Julien Prévost]]`, `[[Muriel]]`

### 3c. Deduce Meeting Type

Infer the `meeting_type` from context clues in the meeting summary:
- If mentions "arbitrage", "decision", "piloting" → `coproj`
- If mentions "technical", "infrastructure", "réseau", "architecture" → `cotech`
- If mentions "workshop", "atelier", "brainstorm" → `ateliers`
- If mentions "point", "status", "update" + domain-specific keywords → `point-apd` or `point-thematique`
- Default to most common type from context

### 3d. Fetch Existing #MEN_* Tags

Use Obsidian CLI: `obsidian vault search "#MEN_"` → list all existing MEN tags

Based on deduced meeting type, select the matching tag:
- `coproj` → `#MEN_coproj`
- `cotech` → `#MEN_cotech`
- etc.

Store this tag for the frontmatter.

### 3e. Detect Themes (Thématiques)

Search the meeting summary for keywords matching existing theme directories:
- Look in `SIA/Projets/MEN/Thématiques/` for files like:
  - `Projet Pascal.md`
  - `Smart Workplace.md`
  - `Architecture réseau.md`
  - `Gouvernance.md`

**Keyword matching:**
- If summary mentions "Pascal", "APD", "infrastructure" → link `[[Projet Pascal]]`
- If mentions "Smart Workplace", "réservation", "restauration" → link `[[Smart Workplace]]`
- If mentions "POL", "WiFi", "fibre", "réseau" → link `[[Architecture réseau]]`
- If mentions "pilotage", "gouvernance", "comité" → link `[[Gouvernance]]`

Add up to 3 primary themes.

### 3f. Create Meeting Note File

**File name:** `YYYY-MM-DD - [Type] Title.md`
- Location: `SIA/Projets/MEN/Réunions/`
- Example: `2026-02-06 - COTECH.md`

**YAML Frontmatter:**
```yaml
---
date: YYYY-MM-DD
participants:
  - Name 1
  - Name 2
status: completed
meeting_type: [deduced type]
tags:
  - MEN_[type]
themes:
  - "[[Theme 1]]"
  - "[[Theme 2]]"
---
```

**Content structure** (following MEN - Mode opératoire.md):
```markdown
## Compte-rendu

[2-3 sentence summary of meeting focus]

## Points clés

### [Key topic 1]
- Bullet point
- Bullet point

### [Key topic 2]
- Bullet point

## Actions immédiates

| Action | Porteur | Statut |
|--------|---------|--------|
| [Action] | [[Porteur Name]] | À faire |

## Participants

- Name 1
- Name 2
```

**Extracting from Granola summary:**
- Split summary by major themes/headings
- Condense into bullet points (remove fluff)
- Identify explicit actions (look for "to do", "must", "will", action phrases)
- Extract participants from the Granola meeting record

### 3g. Update MEN - Index.md

Edit `SIA/Projets/MEN/MEN - Index.md`:
1. Find the section "### Réunions par semaine"
2. Locate the correct week (or create a new week section if needed)
3. Add entry: `- [[YYYY-MM-DD - Title]] - Brief description`
4. Keep chronological order within the section

### 3h. Update Theme Pages (Optional Cross-Reference)

For each detected theme:
1. Open `SIA/Projets/MEN/Thématiques/[Theme].md`
2. Find "## Réunions associées" section
3. Find the appropriate week subsection or create it
4. Add: `- [[YYYY-MM-DD - Title]] - What this meeting covered about the theme`

## Step 4: Summarize Results

After all meetings are processed, print a summary:

```
✓ Successfully imported [N] meetings:

- 2026-02-06 - Smart Workplace.md (detected: Jalal, themes: [[Projet Pascal]], [[Smart Workplace]])
- 2026-02-06 - COTECH.md (detected: porteurs: [[Julien Prévost]], themes: [[Architecture réseau]])

Index updated: SIA/Projets/MEN/MEN - Index.md
Theme pages updated: 2 (Smart Workplace, Architecture réseau)
```

If any meetings had errors or partial matches, note them:
```
⚠ Partial imports:
- 2026-02-12 - Point d'arbitrage.md (no clear porteurs detected — you may want to add them manually)
```

## Deferring to Obsidian CLI Helper

For any complex Obsidian CLI operations not covered here, reference the `obsidian-cli-helpers` skill:
- Listing/searching vault contents
- Reading/writing files
- Advanced tag queries

Simply use the skill as: "See obsidian-cli-helpers skill for [command]"

## Edge Cases & Fallbacks

**No porteurs detected:** Still create the note, but mark the Actions section for manual review
**No themes detected:** Link to [[Projet Pascal]] by default (most common) and add a comment
**Ambiguous meeting type:** Use the most common type from similar recent meetings, or default to `point-apd`
**Date parsing fails:** Ask user to clarify the date range

## Mode Opératoire Reference

This skill implements the workflow described in `SIA/Projets/MEN/MEN - Mode opératoire.md`. All YAML frontmatter, file naming conventions, and structure rules follow that guide exactly.
