# Action Extraction & Todoist Integration

## Detecting Action Patterns

### Linguistic Markers

**Direct assignments:**
- "[Name] will [action]" / "[Name] doit [action]"
- "[Name] needs to [action]" / "[Name] besoin de [action]"
- "I will [action]" / "Je vais [action]"
- "You need to [action]" / "Tu dois [action]"

**Imperative forms:**
- "[Action], ok?" / "[Action], d'accord ?"
- "Make sure to [action]" / "Assure-toi de [action]"
- "Please [action]" / "S'il te plaît [action]"

**Implicit patterns:**
- "Action: [description]"
- "To-do: [description]"
- "Follow-up: [description]"
- Statements ending with deadline → likely action

### Confidence Scoring

```
High confidence (0.9+):
- Explicit name assignment + imperative
- "Seb will review the RFP by Friday" → 0.95

Medium confidence (0.7-0.89):
- Role-based assignment (if user's role matches)
- Imperative without explicit name (context-dependent)
- "We need to validate this" (if you're the validator)

Low confidence (0.5-0.69):
- Pronoun-based ("you should check")
- Ambiguous phrasing
- Implicit responsibility

Skip (< 0.5):
- Generic statements ("we should improve X")
- FYI items without action verb
- Decisions that aren't tasks
```

### User Relevance Detection

An action is relevant if:
1. **Name match** : "Seb", "Sébastien", known aliases → 100% relevant
2. **Role match** : User's title/expertise (e.g., "consultant", "lead") + action domain
3. **Pronoun match** : "tu dois", "c'est à toi", "you're responsible"
4. **Domain overlap** : Action is in user's known area (Smart Building, RFP, dev) → mark as "likely for you"
5. **Explicit flag** : User clicks checkbox to claim action

---

## Extraction Algorithm (Pseudocode)

```python
def extract_actions(transcript: str, user_name: str, user_roles: List[str]) -> List[Action]:
    """
    Parse transcript and extract actionable items.
    """
    actions = []
    sentences = tokenize_sentences(transcript)
    
    for i, sentence in enumerate(sentences):
        if has_action_verb(sentence):  # "do", "check", "review", "prepare", etc.
            action = {
                "description": extract_main_clause(sentence),
                "owner": extract_owner(sentence, sentences[i-2:i+3]),  # Look at context
                "deadline": extract_deadline(sentence, sentences[i:i+3]),
                "context": extract_section_header(sentences, i),  # Which agenda item?
                "confidence": calculate_confidence(sentence),
            }
            
            # Determine if relevant to user
            action["relevant_to_user"] = is_relevant(
                action, 
                user_name=user_name, 
                user_roles=user_roles
            )
            
            # Dedup: check if similar action already extracted
            if not is_duplicate(action, actions):
                actions.append(action)
    
    return sorted(actions, key=lambda x: x["confidence"], reverse=True)

def is_relevant(action: Action, user_name: str, user_roles: List[str]) -> bool:
    """Check if action concerns the user."""
    
    # Direct name match
    if user_name.lower() in action["description"].lower():
        return True
    if user_name.lower() in (action["owner"] or "").lower():
        return True
    
    # Role match
    for role in user_roles:
        if role.lower() in action["description"].lower():
            # And action verb aligns with that role
            if action_aligns_with_role(action["description"], role):
                return True
    
    # Pronoun match (you, tu, c'est à toi)
    if any(pronoun in action["description"].lower() for pronoun in ["you", "tu", "c'est à toi"]):
        return True
    
    return False
```

---

## Output Format

```json
{
  "actions": [
    {
      "id": 1,
      "description": "Analyser les réponses RFP IZIX et comparer avec Witco",
      "owner": "Seb",
      "owner_confidence": 0.95,
      "deadline": "2024-03-31",
      "deadline_confidence": 0.9,
      "context": "Point 2 : Évaluation fournisseurs",
      "relevant_to_user": true,
      "confidence": 0.93,
      "extracted_at": "2024-03-25T14:32:00Z",
      "transcript_quote": "Seb, tu dois analyser les réponses RFP avant vendredi..."
    },
    {
      "id": 2,
      "description": "Valider le budget prévisionnel avec finance",
      "owner": "Alice",
      "owner_confidence": 0.92,
      "deadline": "2024-03-28",
      "deadline_confidence": 0.88,
      "context": "Point 3 : Budget 2024",
      "relevant_to_user": false,
      "confidence": 0.89,
      "extracted_at": "2024-03-25T14:32:00Z",
      "transcript_quote": "Alice, tu dois valider avec finance d'ici mercredi..."
    }
  ],
  "summary": {
    "total_actions": 7,
    "actions_for_user": 3,
    "high_confidence": 5,
    "without_deadline": 2
  }
}
```

---

## Todoist MCP Integration

### Checking Todoist MCP Availability

Before attempting to send actions to Todoist:

1. **Verify MCP is connected** : Check if Todoist MCP is available in the active MCP list
   - Primary URL (official Todoist): `https://ai.todoist.net/mcp`
   - Alternative: User may have a custom Todoist MCP server configured
   
2. **Fetch available projects** : Call Todoist MCP to retrieve the user's active projects
   - This confirms the connection works
   - Returns project list with IDs and names
   - Should be cached for the session

3. **If MCP unavailable** :
   - Display message: "Todoist MCP not connected. Please add it in your MCP settings."
   - Provide fallback: Generate a copyable task summary formatted for manual import
   - Link to Todoist setup guide

### Getting Active Projects from Todoist

**On skill initialization or when user enables Todoist export:**

```
Call: Todoist MCP "Get all projects" or similar
Returns: [
  { id: "12345", name: "ENGIE Smart Parking", color: "blue" },
  { id: "67890", name: "Meeting Actions", color: "gray" },
  { id: "11111", name: "Praemia REIM", color: "green" },
  ...
]
```

**Caching strategy** :
- Fetch projects once per session at skill trigger
- Store in skill context (or memory if available)
- Offer refresh button if user adds new projects

### Project Selection Strategy

Display project selection to user with:
1. **Suggested mapping** (if configured):
   - ENGIE → "ENGIE Smart Parking"
   - Praemia → "Praemia REIM"
   - Accor → "Accor L1 Support"
   - Default: "Meeting Actions"

2. **User override** :
   - Dropdown to select project explicitly
   - Or "Create new project" option

3. **Batch actions** :
   - "Send all to [Project name]?"
   - Option to map different actions to different projects

---

## Todoist Payload Mapping

For each action sent to Todoist via MCP:

```javascript
{
  // Task title: prepend owner if not user
  "content": "[Seb] Analyser réponses RFP IZIX",
  
  // Full context in description
  "description": [
    "**Source:** Réunion ENGIE RFP - 25 mars 2024",
    "**Context:** Point 2 - Évaluation fournisseurs",
    "**Original owner:** Seb",
    "",
    "Analyser les réponses RFP IZIX et comparer avec Witco",
    "",
    "Transcript quote: \"Seb, tu dois analyser les réponses...\"",
  ].join("\n"),
  
  // Due date
  "due_date": "2024-03-31",
  
  // Priority: infer from deadline urgency
  "priority": 3,  // 1=urgent (< 3 days), 2=high (< 7 days), 3=normal, 4=low
  
  // Labels for organization
  "labels": [
    "meeting-notes",      // Source
    "ENGIE",              // Client/project
    "RFP",                // Domain
    "Smart Building"      // Technical domain
  ],
  
  // Optional: project_id if configured
  // "project_id": "12345",
  
  // Optional: section_id if organizing by client/type
  // "section_id": "67890"
}
```

### Label Strategy

Auto-generate labels from:
- **Meeting context** : Client name (ENGIE, Praemia, etc.)
- **Domain** : RFP, Smart Building, Finance, etc.
- **Urgency** : urgent, high-priority (if deadline < 3 days)
- **Type** : meeting-notes, follow-up, decision-item

User can customize mapping in config.

---

## User Configuration

Store user preferences for action handling:

```yaml
# In ~/.seb-context/todoist-config.yml or similar
todoist:
  default_project: "Meeting Actions"  # or null for Inbox
  auto_labels:
    - "meeting-notes"
  map_clients_to_projects:
    ENGIE: "ENGIE Smart Parking"
    Praemia: "Praemia REIM"
    Accor: "Accor L1 Support"
  map_domains_to_sections:
    RFP: "RFP Evaluations"
    "Smart Building": "Smart Building Dev"
  priority_rules:
    deadline_within_days_3: 1  # Urgent
    deadline_within_days_7: 2  # High
    else: 3  # Normal
```

---

## Testing & Validation

### Test Cases

**Test 1: Direct assignment with deadline**
```
Input: "Seb, you need to review the ENGIE proposal by Friday the 28th."
Expected:
  - owner: "Seb", confidence: 0.95
  - deadline: "2024-03-28", confidence: 0.9
  - relevant_to_user: true
  - confidence: 0.93
```

**Test 2: Role-based implicit assignment**
```
Input: "The consultant should validate that the architecture is sound by end of sprint."
With user_roles: ["consultant"]
Expected:
  - owner: "Consultant (role)", confidence: 0.7
  - deadline: "2024-04-05" (inferred from sprint), confidence: 0.6
  - relevant_to_user: true (role match)
  - confidence: 0.7
```

**Test 3: FYI (not an action)**
```
Input: "Just FYI, we've approved the budget allocation. It should be in the system by next week."
Expected:
  - Not extracted (no action verb, only FYI statement)
```

---

## UI Presentation

### Tableau des actions dans le chat

```
🎯 **Actions extraites (5 trouvées)**

Pour toi : 3 | Autres : 2

| # | Action | Responsable | Deadline | Todoist |
|----|--------|-----------|----------|---------|
| ✅ | Analyser RFP IZIX vs Witco | Seb | 31/03 | [➕ Ajouter] |
| ✅ | Préparer synthèse comparative | Seb | 02/04 | [➕ Ajouter] |
| ✅ | Planifier réunion de restitution | Seb | 28/03 | [➕ Ajouter] |
| ❌ | Valider budget finance | Alice | 28/03 | — |
| ⚠️ | "Améliorer la doc" *(ambigü)* | ? | — | [?] |

**Confidence notes:**
- ⚠️ Action #5 : Faible confiance (0.55). C'est pour toi ?
  [✅ Oui] [❌ Non]
```

### Batch Actions to Todoist

```
[➕ Ajouter toutes mes actions à Todoist]  (3 actions)

ou

[➕ Ajouter sélectionnées] (after filtering)
```

### Success Feedback

```
✅ 3 actions ajoutées à Todoist !

1. "Analyser RFP IZIX vs Witco" → Projet: ENGIE Smart Parking | Deadline: 31/03
2. "Préparer synthèse comparative" → Projet: ENGIE Smart Parking | Deadline: 02/04
3. "Planifier réunion de restitution" → Projet: Meeting Actions | Deadline: 28/03

[Voir dans Todoist] [Undo]
```
