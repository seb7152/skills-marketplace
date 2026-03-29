# Context Building: How the Agent Learns and Stores

The vault is designed to help agents remember you, your work, and your context. This document explains how the agent should read, learn, and update the vault across sessions.

## Session Startup: Reading Context

At the beginning of each session, the agent MUST read these files in order:

### 1. Personal Profile (`10_context/profil.md`)
**Purpose:** Who are you? What's your background, skills, interests?

**Read because:** Helps the agent understand how to tailor advice, what language to use, what your baseline skills are.

**Example structure:**
```yaml
---
type: personal-profile
project: personal
date: "2026-03-29"
title: "Seb's Profile"
---

## Background
- 10+ years in consulting
- Founder of SIA Partners
- Building AI automation workflows

## Current Skills
- Python scripting
- Obsidian vault organization
- API design and integration

## Interests & Focus
- Knowledge management
- Agent workflows
- Building tools for teams

## Timezone & Availability
- CEST (UTC+2)
- Usually available: 9am-6pm weekdays
```

### 2. Aspirations (`10_context/aspirations.md`)
**Purpose:** What are your goals? What are you working toward?

**Read because:** Helps the agent prioritize tasks, suggest improvements aligned with your direction, avoid wasting time on dead ends.

**Example structure:**
```yaml
---
type: aspirations
project: personal
date: "2026-03-29"
title: "Goals & Direction"
---

## 2026 Goals
- Migrate all meetings to Obsidian vault ✓ (done)
- Build complete API for vault queries
- Create skill framework for agents

## Current Focus (Q2 2026)
- Deploy API to production (Hostinger)
- Document vault workflows
- Enable agents to enrich context automatically

## Long-term (2-5 years)
- Build a platform for knowledge agents
- Help teams use AI to augment knowledge work
```

### 3. System Context (`_system/MEMORY.md`)
**Purpose:** What does the agent need to know about your domain? Acronyms, projects, people, decisions?

**Read because:** Ensures the agent doesn't make suggestions that violate past decisions or ignore domain constraints.

**Example structure:**
```yaml
---
type: system-context
project: professional
date: "2026-03-29"
---

## Key People
- Alice (CTO, MEN project)
- Bob (Product Lead, The-Link)
- Carol (Finance, budget owner)

## Project Acronyms
- COTECH: Collaborative Workspace Technology initiative
- PASCAL: Ministry move to Gentilly project
- Smart Workplace: Next-gen workspace platform

## Active Projects
- MEN: Ministry network modernization
- The-Link: Internal collaboration tool
- ENGIE-Lease-Management: Real estate optimization

## Past Decisions
- 2026-03-15: Decided to use Obsidian for all meeting notes (not Notion)
- 2026-02-01: API must support both professional (20_Projects) and personal (10_context) contexts
- 2025-12-10: All meetings require summaries in English + French

## Constraints
- API token must rotate monthly
- Meeting summaries max 3 lines, plain text only
- Personal files must use "personal" project tag
```

### 4. Workflow Rules (`_system/agent_rules.md`)
**Purpose:** How should the agent behave? What are the operational constraints?

**Read because:** Prevents the agent from making unsafe decisions or breaking conventions.

## Learning & Updating Context

During a session, the agent will discover new information:
- Something you mention about your goals
- A decision you make
- A pattern in your work
- New terminology or people

### Creating New Personal Files

When the agent learns something important, it should create a new file in `10_context/perso/`:

**File types:**
- `personal-note` — General learning or observation
- `personal-todo` — Action items for you
- `personal-favorite` — Resources, links, references
- `reflection` — Deeper thinking, learnings, patterns
- `project-idea` — Side projects or ideas

**Example: Agent learns you're interested in OAuth**
```bash
POST /api/file/10_context/perso/notes/oauth-learning.md

{
  "content": "---\ntype: personal-note\nproject: personal\ndate: \"2026-03-29\"\ntitle: \"Learning: OAuth 2.0 Implementation\"\nstatus: active\n---\n\n## Context\nDuring our discussion about API security, Seb mentioned wanting to implement OAuth for the Obsidian API.\n\n## Key Points\n- Investigating OAuth 2.0 flows\n- Evaluating libraries for Node.js\n- Planning integration with existing Bearer token auth\n\n## Next Steps\n- Research authorization_code vs client_credentials flows\n- Test with ChatGPT integration\n"
}
```

### Updating Shared Context (`_system/MEMORY.md`)

When the agent discovers new domain knowledge, it should update MEMORY.md:

**Examples:**
- New person mentioned → Add to "Key People"
- New project acronym → Add to "Project Acronyms"
- Important decision made → Add to "Past Decisions"
- New constraint discovered → Add to "Constraints"

```bash
PATCH /api/file/_system/MEMORY.md

{
  "updated": "2026-03-29"
}
```

Then append to the body:

```
## New Entry (Added 2026-03-29)

**Person:** David (DevOps, manages Hostinger infrastructure)
**Context:** Mentioned during deployment planning; handles server configuration and API deployment.

**Project:** OAuth Integration (starting Q2 2026)
**Status:** Planning phase
**Constraint:** Must maintain backward compatibility with existing Bearer token auth
```

### Using Inbox for Quick Capture

If unsure where something belongs, use `00_inbox/`:

```bash
POST /api/file/00_inbox/session-2026-03-29.md

{
  "content": "---\ntype: inbox-item\nproject: personal\ndate: \"2026-03-29\"\ntitle: \"Session Notes - March 29\"\nstatus: draft\n---\n\n## Topics Discussed\n- OAuth implementation strategy\n- API deployment on Hostinger\n- Agent context management\n\n## Decisions Made\n- Will use Authorization Code flow for OAuth\n- Deploy to production by end of Q2\n\n## Learnings\n- Agent should read profil.md at session start\n- Need to track personal learning separately from work\n\n## TODO for Next Session\n- Organize inbox items into proper files\n- Update MEMORY.md with new decisions\n"
}
```

Then in the next session, organize these into proper files or archive.

## Context Consistency

**Golden rule:** All context added to the vault should be:

1. **Structured** — Follows YAML frontmatter format
2. **Findable** — Tagged with correct type/project
3. **Dated** — Includes when it was added or updated
4. **Traceable** — You can understand why something was added
5. **Actionable** — Supports decision-making or learning

**Bad example (unstructured):**
```
some random notes about oauth that dont follow any format
```

**Good example (structured):**
```yaml
---
type: personal-note
project: personal
date: "2026-03-29"
title: "OAuth Implementation Strategy"
status: active
---

## Decision
Will implement OAuth 2.0 using Authorization Code flow.

## Rationale
- Most secure for user-facing applications
- Well-supported by ChatGPT integration
- Backward compatible with existing Bearer token auth

## Implementation Plan
1. Research Node.js OAuth libraries
2. Design token refresh mechanism
3. Update API spec (openapi.yaml)
4. Test with ChatGPT

## Resources
- https://tools.ietf.org/html/rfc6749
- Node.js libraries: passport.js, oidc-provider
```

## What NOT to Store

Don't store in the vault:
- **Secrets:** API keys, passwords, tokens (use environment variables instead)
- **Sensitive data:** Financial info, personal identifying details
- **Temporary notes:** Use inbox, then delete when organized or archived
- **Duplicate information:** Link to existing files instead of copying

## Example Session Flow

### Session Start
1. Agent reads `10_context/profil.md` → Understands your background
2. Agent reads `10_context/aspirations.md` → Knows your 2026 goals
3. Agent reads `_system/MEMORY.md` → Learns about projects, people, acronyms
4. Agent reads `_system/agent_rules.md` → Understands constraints

### During Session
- You mention something important → Agent creates file in `10_context/perso/`
- You make a decision → Agent updates `_system/MEMORY.md`
- You discover something → Agent adds to relevant personal note
- Unclear where to put something → Agent adds to `00_inbox/`

### Session End
- Agent suggests organizing inbox items for next session
- Vault is consistent and all new info is accessible

### Next Session
- Agent reads updated MEMORY.md with yesterday's decisions
- Agent reads new personal notes from yesterday
- Agent has continuity across sessions

## Tips for Agents

1. **Always start by reading context** — Don't make assumptions about who the user is or what they want
2. **Ask before creating new files** — If unsure, ask: "Should I create a file about X?"
3. **Keep profil.md and aspirations.md fresh** — Update when goals change
4. **Use MEMORY.md for shared learning** — Future agents will benefit
5. **Structure is power** — Every new file should follow the format, or it becomes noise
6. **Archive don't delete** — Change status to "archived" instead of removing files
7. **Link to existing files** — Reference things like "see `10_context/perso/oauth-learning.md`"
