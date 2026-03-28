# Todoist Configuration & Setup

## MCP Connection Check

### Verifying Todoist MCP

On skill initialization, verify:

```javascript
// Pseudo-code
async function checkTodoistMCP() {
  // Check if Todoist MCP is in active MCPs list
  const todoistAvailable = checkMCPConnected("Todoist");
  
  if (!todoistAvailable) {
    return {
      status: "unavailable",
      message: "Todoist MCP not connected",
      action: "Suggest enabling https://ai.todoist.net/mcp in MCP settings"
    };
  }
  
  // Test connection by fetching projects
  try {
    const projects = await callTodoistMCP("get_all_projects", {});
    return {
      status: "connected",
      projects: projects,
      projectCount: projects.length
    };
  } catch (error) {
    return {
      status: "error",
      message: "Failed to connect to Todoist MCP",
      error: error.message,
      action: "Re-authenticate OAuth or check MCP configuration"
    };
  }
}
```

---

## Project Mapping Configuration

### Default Mappings

Map clients/contexts to Todoist projects by name:

```yaml
# Example configuration for Seb
todoist_mappings:
  # Client → Project name
  ENGIE: "ENGIE Smart Parking"       # Smart Parking project
  Praemia: "Praemia REIM"             # Real Estate project
  Accor: "Accor L1 Support"           # Outsourcing support
  TotalEnergies: "TotalEnergies"     # Energy project
  Sanofi: "Sanofi"                   # Pharma project
  
  # Domain → Section or default project
  RFP: "ENGIE Smart Parking"  # RFP responses go to main client
  "Smart Building": "Smart Building Dev"
  "Figma Plugin": "Dev Projects"
  "Startup DB": "Startup DB"
  
  # Fallback
  default: "Meeting Actions"
  
# Automatically assign these labels to all meeting-sourced tasks
auto_labels:
  - "meeting-notes"
  - "{client_name}"      # e.g., "ENGIE", "Praemia"
  - "{domain}"           # e.g., "RFP", "Smart Building"

# Priority rules
priority_rules:
  # deadline within X days → priority level
  deadline_in_1_day: 1      # Urgent
  deadline_in_3_days: 2     # High
  deadline_in_7_days: 3     # Normal
  else: 4                   # Low
```

### Runtime Project Selection

When generating meeting notes, if Todoist is enabled:

1. **Detect meeting context** from transcript:
   - Client name (ENGIE, Praemia, etc.)
   - Project/domain (RFP, Smart Building, etc.)
   
2. **Suggest project** using mapping:
   ```
   "These actions seem related to ENGIE Smart Parking project.
    Send to that project? [Yes] [Pick different] [Inbox]"
   ```

3. **Display available projects** if user chooses "Pick different":
   ```
   Available projects:
   - ENGIE Smart Parking (8 tasks)
   - Praemia REIM (5 tasks)
   - Accor L1 Support (12 tasks)
   - Meeting Actions (47 tasks)
   - [Create new project]
   ```

4. **Batch selection** for multiple actions:
   ```
   Actions for Todoist:
   □ Analyse RFP IZIX → ENGIE Smart Parking
   □ Préparer synthèse → ENGIE Smart Parking
   □ Validation budget → [Ask user]
   □ Planifier réunion → ENGIE Smart Parking
   
   [Send all] [Customize] [Cancel]
   ```

---

## Tool Calls to Todoist MCP

### Official Todoist AI MCP Tools

The official Todoist MCP (`https://ai.todoist.net/mcp`) exposes:

**Available tools** (from Doist/todoist-ai documentation):
- `addTasks` – Create one or more tasks
- `findTasksByDate` – Find tasks due on specific date
- `quickAdd` – Quick-add syntax (natural language)
- `close` – Mark task complete
- `updateTask` – Update task properties
- `deleteTask` – Remove task
- `getProjects` – List all projects
- `getSections` – List sections in project
- `getLabels` – List available labels
- Plus more...

### Task Creation Call Format

When sending action to Todoist:

```javascript
{
  // Todoist MCP call (exact format to verify with MCP)
  tool: "Todoist:addTasks" || "quickAdd", // TBD - verify with actual MCP
  
  input: {
    // If using structured tool:
    tasks: [
      {
        content: "[Seb] Analyser réponses RFP IZIX",
        description: "Source: Réunion ENGIE RFP - 25 mars 2024\nContexte: Point 2 - Évaluation fournisseurs\n\nOriginal transcript:\n\"Seb, tu dois analyser les réponses RFP IZIX et comparer avec Witco\"",
        due_date: "2024-03-31",
        priority: 2,  // 1=highest, 4=lowest
        project_id: "12345",  // From getProjects() call
        labels: ["meeting-notes", "ENGIE", "RFP"],
        description_url: "https://granola.ai/meeting/..."  // Optional link to meeting
      }
    ]
    
    // Or if using quickAdd (natural language):
    // "Analyser réponses RFP IZIX - Seb #ENGIE !2 due:2024-03-31"
  }
}
```

---

## Fallback (MCP Unavailable)

If Todoist MCP is not connected, generate a **manual import text** for user to copy-paste:

```markdown
## Tasks to add to Todoist (Copy & Paste)

Analyser réponses RFP IZIX - Seb #ENGIE !2 due:2024-03-31
Préparer synthèse comparative - Seb #ENGIE !3 due:2024-04-02
Planifier réunion de restitution - Seb !2 due:2024-03-28

**Syntax:**
- `#project` = project name
- `!priority` = priority (1=highest)
- `due:date` = due date (YYYY-MM-DD)
- `@person` = assignee
```

And display a button/link:
> "Todoist MCP not connected. 
>  [Set up Todoist MCP] | [Copy manual tasks above] | [Skip]"

---

## Implementation Checklist

- [ ] Verify Todoist MCP URL is `https://ai.todoist.net/mcp`
- [ ] Confirm exact tool names via MCP introspection
- [ ] Implement `getProjects()` call on skill load
- [ ] Cache projects list for session
- [ ] Build project selector UI component
- [ ] Map user's Todoist projects to config
- [ ] Implement task creation call (structured or quickAdd)
- [ ] Test with real Todoist account
- [ ] Fallback text generation if MCP unavailable
- [ ] Add "Refresh projects" button for long sessions
