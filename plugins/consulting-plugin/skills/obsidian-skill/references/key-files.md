---
created: 2026-03-29
updated: 2026-03-29
---
# Key System Files

The vault contains several system files that provide context and documentation. Know what each one is for and when to consult it.

## Files in `_system/` Folder

### `agent.md`
**Purpose:** Entry point and workflow guide.

**Read when:**
- Starting a new task with the vault
- Unsure whether to use professional or personal workflow
- Need a quick reference for what the vault is

**Contents:** Links to other reference files based on workflow type. Very concise.

### `API.md`
**Purpose:** Complete REST API documentation with examples for all endpoints.

**Read when:**
- Working with the API directly (curl, Python requests, etc.)
- Need detailed information about query parameters, filters, response formats
- Building a script that queries or updates the vault
- Debugging API issues

**Key sections:**
- All endpoints (GET /api/files, POST /api/file, PATCH /api/file, GET /api/search, etc.)
- Authentication and error handling
- Request/response examples for every operation
- Batch operation patterns

### `MEMORY.md`
**Purpose:** Context about the vault's domain: people, acronyms, projects, historical decisions.

**Read BEFORE:**
- Generating summaries for meetings
- Creating new decisions or action items
- Analyzing project context
- Writing content that should reference internal knowledge

**Contents:**
- Who's who (people, roles, teams)
- Project acronyms and what they mean (PASCAL, Smart Workplace, COTECH, etc.)
- Current projects and their status
- Historical decisions and constraints
- Terminology and conventions

**Why it matters:** Content generated without reading MEMORY.md often misses context, makes redundant suggestions, or violates past decisions.

### `agent_rules.md`
**Purpose:** Rules and constraints for how agents should interact with the vault.

**Read when:**
- Building automated workflows (batch summaries, bulk updates)
- Unsure about conventions (date formats, status values, naming)
- Managing file organization or archival
- Following project governance

**Key sections:**
- How to structure different file types
- Status progression (draft → review → completed → archived)
- When to create vs. update files
- How to handle duplicates or conflicts
- Authorization and sensitive data

### `openapi.yaml`
**Purpose:** Machine-readable API specification (OpenAPI 3.0).

**Read when:**
- Feeding the API to ChatGPT for code generation
- Setting up a client library
- Documenting the API for other users
- Understanding the complete API contract

**Format:** YAML that defines:
- All endpoints with operationIds
- Request/response schemas
- Authentication requirements
- Error codes

**Usage:** Can be imported into ChatGPT's Code Interpreter or Swagger UI for visual documentation.

---

## Workflow-Specific Reference Files

### For Professional Work
**Primary:** `references/workflow-professional.md`

Covers:
- Folder structure for 20_Projects
- File types (meeting-summary, decision, coding-notes, etc.)
- API patterns for querying and updating projects
- Python patterns for batch operations
- When to consult MEMORY.md

### For Personal Storage
**Primary:** `references/workflow-personal.md`

Covers:
- Folder structure for 10_context/perso and inbox
- File types for personal content
- Creating and organizing personal notes
- When to update profil.md or aspirations.md
- Quick capture patterns

### For File Format Details
**Primary:** `references/file-format.md`

Covers:
- YAML frontmatter template and syntax
- Standard properties (type, project, date, title, summary, status)
- Custom properties (adding your own fields)
- API response format
- Special cases (minimal frontmatter, quick capture)

---

## Quick Lookup Table

| Need | File to Read |
|------|--------------|
| "What's the workflow?" | `agent.md` |
| "How do I use the API?" | `_system/API.md` |
| "What does COTECH mean?" | `_system/MEMORY.md` |
| "What's the date format?" | `references/file-format.md` |
| "Am I following the rules?" | `_system/agent_rules.md` |
| "Professional or personal?" | `references/workflow-professional.md` or `workflow-personal.md` |
| "How do I query files?" | `references/workflow-professional.md` + `_system/API.md` |
| "Where do I put personal notes?" | `references/workflow-personal.md` |
| "What custom fields can I add?" | `references/file-format.md` |

---

## Reading Order for Different Tasks

### Agent: Session Startup
1. `10_context/profil.md` — Who is the user?
2. `10_context/aspirations.md` — What are their goals?
3. `_system/MEMORY.md` — What's the domain context?
4. `_system/agent_rules.md` — What are the constraints?
5. `agent.md` — Then understand the workflow

### Human: New to the vault?
1. `agent.md` — Understand the structure
2. Either `references/workflow-professional.md` or `workflow-personal.md` — Get oriented
3. `references/file-format.md` — Learn YAML format
4. `references/context-building.md` — How agents learn and store context

### Querying the vault?
1. `_system/API.md` — Find the right endpoint
2. `_system/MEMORY.md` — Understand context for your query
3. `references/workflow-professional.md` or `workflow-personal.md` — See example patterns

### Generating content (summaries, decisions)?
1. `_system/MEMORY.md` — Read context first
2. `_system/agent_rules.md` — Understand constraints
3. `references/file-format.md` — Get frontmatter right
4. `_system/API.md` — See examples of similar files

### Organizing personal files?
1. `references/workflow-personal.md` — Folder structure
2. `references/file-format.md` — Frontmatter for personal files
3. `00_inbox/` → `10_context/perso/` — Move items when organized

### Debugging or troubleshooting?
1. `_system/API.md` — Check endpoint parameters and response format
2. `_system/agent_rules.md` — Verify you're following conventions
3. `_system/MEMORY.md` — Check for context you might be missing

## Quick Lookup Table (Updated)

| Need | File to Read |
|------|--------------|
| "What's the workflow?" | `agent.md` |
| "How do I use the API?" | `_system/API.md` |
| "What does COTECH mean?" | `_system/MEMORY.md` |
| "What's the date format?" | `references/file-format.md` |
| "Am I following the rules?" | `_system/agent_rules.md` |
| "Professional or personal?" | `references/workflow-professional.md` or `workflow-personal.md` |
| "How do I query files?" | `references/workflow-professional.md` + `_system/API.md` |
| "Where do I put personal notes?" | `references/workflow-personal.md` |
| "What custom fields can I add?" | `references/file-format.md` |
| "How should I learn and remember?" | `references/context-building.md` |
| "What should I read at session start?" | `references/context-building.md` |
