# MCP Integration Guide - RFP Analyzer Import

Guide complet pour importer des données dans RFP Analyzer via le serveur MCP.

---

## 📋 Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Prérequis](#prérequis)
3. [Méthodes d'import](#méthodes-dimport)
4. [Workflow recommandé](#workflow-recommandé)
5. [Tools MCP disponibles](#tools-mcp-disponibles)
6. [Endpoint HTTP direct (curl)](#endpoint-http-direct-curl)
7. [Gestion des erreurs](#gestion-des-erreurs)
8. [Exemples complets](#exemples-complets)

---

## Vue d'ensemble

Le serveur MCP RFP Analyzer offre **deux méthodes** pour importer des données:

| Méthode | Cas d'usage | Avantages |
|---------|-------------|-----------|
| **MCP Tools** | Import interactif, petits volumes | - Feedback immédiat<br>- Validation en temps réel<br>- Contrôle utilisateur |
| **HTTP Endpoint (curl)** | Gros volumes, automation | - Fichier hors contexte LLM<br>- Performance optimale<br>- Automatisation scripts |

**⚠️ IMPORTANT - Validation obligatoire**

Quelle que soit la méthode choisie, **la validation JSON avec `scripts/validate_json.py` est OBLIGATOIRE avant tout import**. Les imports sans validation préalable seront rejetés par le serveur.

---

## Prérequis

### 1. Authentification

Vous devez disposer d'un **Personal Access Token (PAT)** RFP Analyzer:

1. Connectez-vous à RFP Analyzer
2. Allez dans **Settings → API Tokens**
3. Cliquez sur **Generate New Token**
4. Copiez le token (format: `rfpa_...`)

### 2. Configuration MCP

Le MCP RFP Analyzer doit être configuré dans votre environnement Claude:

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "rfp-analyzer": {
      "url": "https://your-app.vercel.app/api/mcp",
      "headers": {
        "Authorization": "Bearer rfpa_your_token_here"
      }
    }
  }
}
```

**Claude Code (CLI)**:

```bash
claude mcp add --transport http rfp-analyzer https://your-app.vercel.app/api/mcp \
  --header "Authorization: Bearer rfpa_your_token_here" \
  --scope user
```

### 3. ID du RFP

Vous devez connaître l'**ID du RFP** dans lequel importer les données:

```bash
# Lister les RFPs disponibles via MCP
# Utilisez le tool MCP: get_rfps
```

Ou demandez à l'utilisateur: "Quel est l'ID du RFP dans RFP Analyzer?"

---

## Méthodes d'import

### Méthode 1: MCP Tools (Recommandé pour interaction)

#### Avantages
- ✅ Feedback immédiat et détaillé
- ✅ Validation en temps réel
- ✅ Gestion interactive des erreurs
- ✅ Parfait pour itération avec l'utilisateur

#### Limites
- ⚠️ Fichier entier dans le contexte LLM (coût tokens)
- ⚠️ Limite de taille (quelques centaines d'items max)

#### Tools disponibles

| Tool MCP | Type de données | Mode |
|----------|----------------|------|
| `import_structure` | Catégories (structure hiérarchique) | append / replace |
| `import_requirements` | Exigences (requirements) | append / replace |
| `import_supplier_responses` | Réponses fournisseurs | append (upsert par requirement) |

### Méthode 2: HTTP Endpoint (Recommandé pour gros volumes)

#### Avantages
- ✅ **Fichier hors contexte** - pas de coût tokens
- ✅ Performance optimale pour gros volumes
- ✅ Automatisation via scripts
- ✅ Support curl natif

#### Workflow

1. **Générer un token d'import** (valide 5min):
   ```
   Utilisez le tool MCP: get_import_command
   ```

2. **Exécuter la commande curl** retournée par le tool

3. **Vérifier le résultat**

---

## Workflow recommandé

Suivez cette séquence pour un import réussi:

```
1. Extraire les données du fichier source (Excel/Word)
   ↓
2. ✅ VALIDER le JSON avec scripts/validate_json.py
   ↓ (SI ERREURS → FIX → RE-VALIDER)
   ↓
3. Demander à l'utilisateur: Import direct ou JSON pour révision?
   ↓
   ├─→ [JSON pour révision] → Sauvegarder et terminer
   │
   └─→ [Import direct]
       ↓
4. Demander: "Quel est l'ID du RFP dans RFP Analyzer?"
   ↓
5. Choisir la méthode:
   ├─→ Petit volume (<100 items) → MCP Tools
   └─→ Gros volume (>100 items) → HTTP curl
   ↓
6. Exécuter l'import
   ↓
7. Vérifier les résultats (created, skipped, errors)
   ↓
8. Gérer les erreurs si nécessaire
```

### Questions à poser à l'utilisateur

**Phase 1 - Intention:**

> "Voulez-vous que je :
> - a) Génère un fichier JSON pour révision manuelle
> - b) Importe directement dans RFP Analyzer via MCP
> - c) Les deux (JSON + import automatique)"

**Phase 2 - RFP cible (si import):**

> "Quel est l'ID du RFP dans RFP Analyzer où importer ces données?"

Si l'utilisateur ne connaît pas l'ID:
```
Proposez d'utiliser le tool get_rfps pour lister les RFPs disponibles
```

**Phase 3 - Mode d'import (catégories/requirements):**

> "Mode d'import :
> - `append` : Ajouter aux données existantes (par défaut)
> - `replace` : Remplacer toutes les données existantes
>
> Quel mode préférez-vous?"

**Phase 4 - Fournisseur (si réponses):**

> "Quel fournisseur voulez-vous importer?
> - Entrez l'ID du fournisseur (si connu)
> - Ou entrez le nom (je le créerai si nécessaire)"

Si l'utilisateur ne connaît pas l'ID:
```
Utilisez le tool list_suppliers pour obtenir la liste
```

---

## Tools MCP disponibles

### 1. `import_structure`

Importe la structure hiérarchique de catégories.

**Paramètres:**

```typescript
{
  rfp_id: string;        // ID du RFP (UUID)
  file_content: string;  // JSON stringifié des catégories
  mode: "append" | "replace";  // Par défaut: "append"
}
```

**Format JSON attendu:**

```json
[
  {
    "id": "cat-1",
    "code": "DOM1",
    "title": "Sécurité",
    "level": 1,
    "parent_id": null,
    "short_name": "SEC",
    "order": 1
  },
  {
    "id": "cat-2",
    "code": "DOM1.1",
    "title": "Authentification",
    "level": 2,
    "parent_id": "cat-1",
    "order": 1
  }
]
```

**Réponse:**

```json
{
  "created": 12,
  "skipped": 0,
  "errors": []
}
```

**Gestion d'erreurs:**

- Si `parent_id` référence une catégorie inexistante → erreur
- Si `code` en double → skip (en mode append) ou erreur (en mode replace)

### 2. `import_requirements`

Importe les exigences (requirements).

**Paramètres:**

```typescript
{
  rfp_id: string;
  file_content: string;  // JSON stringifié des requirements
  mode: "append" | "replace";
}
```

**Format JSON attendu:**

```json
[
  {
    "code": "REQ-001",
    "title": "Authentification multi-facteurs",
    "description": "Le système doit supporter l'authentification à deux facteurs",
    "weight": 0.8,
    "category_name": "DOM1.1",
    "is_mandatory": true,
    "is_optional": false,
    "tags": ["sécurité", "auth"],
    "page_number": 12
  }
]
```

**⚠️ Champs requis:** `code`, `title`, `description`, `weight`, `category_name`

**Validation pré-import:**

- `category_name` doit correspondre au `code` d'une catégorie existante
- `weight` entre 0 et 1
- `code` unique

**Réponse:**

```json
{
  "created": 45,
  "skipped": 2,
  "errors": [
    {
      "code": "REQ-042",
      "error": "Category 'DOM99' not found"
    }
  ]
}
```

### 3. `import_supplier_responses`

Importe les réponses d'un fournisseur.

**Paramètres:**

```typescript
{
  rfp_id: string;
  file_content: string;  // JSON stringifié des réponses
  supplier_id?: string;   // ID du fournisseur (optionnel)
  supplier_name?: string; // Nom (créé si absent, optionnel)
  version_id?: string;    // Version d'évaluation (optionnel)
}
```

**Format JSON attendu:**

```json
[
  {
    "requirement_id_external": "REQ-001",
    "response_text": "Notre solution supporte MFA via TOTP et biométrie",
    "ai_score": 4.5,
    "ai_comment": "Réponse complète et détaillée",
    "manual_score": 5,
    "manual_comment": "Excellent, validé en démo",
    "question": "Quel est le coût de l'option biométrie?",
    "status": "pass"
  }
]
```

**⚠️ Champ requis:** `requirement_id_external`

**Notes importantes:**

- **Scores absents → 0**: Si `ai_score` ou `manual_score` est `null`/absent, mapper à `0`
- **Status valides**: `pending`, `pass`, `partial`, `fail`
- **Upsert**: Si une réponse existe déjà pour ce requirement, elle est mise à jour

**Réponse:**

```json
{
  "created": 38,
  "updated": 12,
  "skipped": 0,
  "errors": []
}
```

---

## Endpoint HTTP direct (curl)

Pour les **gros volumes** ou l'**automatisation**, utilisez l'endpoint HTTP `/api/mcp/import-file`.

### Étape 1: Générer un token d'import

Utilisez le tool MCP `get_import_command`:

**Paramètres:**

```typescript
{
  rfp_id: string;
  type: "structure" | "requirements" | "supplier_responses";
  mode?: "append" | "replace";  // Par défaut: "append"
  supplier_id?: string;  // Requis si type=supplier_responses
  supplier_name?: string; // Alternative à supplier_id
  file_path: string;  // Chemin du fichier JSON
}
```

**Exemple d'appel:**

```
Tool: get_import_command
Params:
{
  "rfp_id": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "type": "requirements",
  "mode": "append",
  "file_path": "requirements.json"
}
```

**Réponse:**

```json
{
  "command": "curl -X POST 'https://your-app.vercel.app/api/mcp/import-file?rfp_id=4fef2cbb-30df-45af-a1ce-f9fa11ec2d54&type=requirements&mode=append' \\\n  -H 'Authorization: Bearer eyJhbGc...' \\\n  --data-binary @requirements.json",
  "token_expires_in": "5 minutes",
  "file_path": "requirements.json"
}
```

### Étape 2: Exécuter la commande curl

Le tool `get_import_command` retourne une commande curl prête à l'emploi.

**Copiez et exécutez la commande:**

```bash
curl -X POST 'https://your-app.vercel.app/api/mcp/import-file?rfp_id=xxx&type=requirements&mode=append' \
  -H 'Authorization: Bearer eyJhbGc...' \
  --data-binary @requirements.json
```

**Réponse:**

```json
{
  "created": 108,
  "skipped": 0,
  "errors": []
}
```

### Paramètres de requête

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `rfp_id` | UUID | ✅ | ID du RFP cible |
| `type` | enum | ✅ | `structure` \| `requirements` \| `supplier_responses` |
| `mode` | enum | - | `append` (défaut) \| `replace` |
| `supplier_id` | UUID | - | ID du fournisseur (requis si type=supplier_responses) |
| `supplier_name` | string | - | Nom du fournisseur (alternative à supplier_id) |
| `version_id` | UUID | - | Version d'évaluation (optionnel) |

### Authentification

L'endpoint `/api/mcp/import-file` utilise un **token d'import éphémère** (validité: 5 minutes) généré par `get_import_command`.

**❌ Les PATs réguliers ne sont PAS acceptés** sur cet endpoint pour des raisons de sécurité.

---

## Gestion des erreurs

### Erreurs courantes

#### 1. Validation JSON échoue

**Erreur:**
```
Validation failed: Unknown field 'weight' in category
```

**Solution:**
- Les catégories n'ont PAS de champ `weight`
- Supprimez tout champ `weight`, `ponderation` du JSON catégories
- Relancez `scripts/validate_json.py`

#### 2. Catégorie non trouvée

**Erreur:**
```json
{
  "errors": [
    {
      "code": "REQ-042",
      "error": "Category 'DOM99' not found"
    }
  ]
}
```

**Solution:**
- Vérifiez que `category_name` dans requirements correspond au `code` d'une catégorie existante
- Importez d'abord les catégories (`import_structure`)
- Puis importez les requirements (`import_requirements`)

#### 3. Requirement non trouvé (réponses)

**Erreur:**
```json
{
  "errors": [
    {
      "requirement_id_external": "REQ-999",
      "error": "Requirement not found"
    }
  ]
}
```

**Solution:**
- `requirement_id_external` doit correspondre au `code` d'un requirement existant
- Importez d'abord les requirements
- Puis importez les réponses fournisseurs

#### 4. Token expiré

**Erreur:**
```json
{
  "error": "Unauthorized: valid import token required"
}
```

**Solution:**
- Le token d'import a expiré (validité: 5 minutes)
- Régénérez un nouveau token avec `get_import_command`
- Relancez la commande curl avec le nouveau token

### Stratégie de retry

En cas d'erreurs partielles:

1. **Analyser les erreurs** retournées dans le champ `errors[]`
2. **Fixer les données** problématiques dans le JSON source
3. **Re-valider** avec `scripts/validate_json.py`
4. **Réimporter** seulement les items qui ont échoué (extraire du JSON original)

---

## Exemples complets

### Exemple 1: Import structure + requirements

**Contexte:** L'utilisateur a extrait catégories et requirements d'un fichier Excel.

**Workflow:**

```bash
# 1. Valider les catégories
python scripts/validate_json.py categories.json categories

# 2. Valider les requirements (avec catégories)
python scripts/validate_json.py requirements.json requirements categories.json

# 3. Demander l'ID du RFP
# Utilisez: get_rfps

# 4. Importer la structure
# Tool MCP: import_structure
{
  "rfp_id": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "file_content": "<contenu de categories.json>",
  "mode": "append"
}

# 5. Importer les requirements
# Tool MCP: import_requirements
{
  "rfp_id": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "file_content": "<contenu de requirements.json>",
  "mode": "append"
}
```

### Exemple 2: Import gros volume via curl

**Contexte:** 500 requirements à importer.

**Workflow:**

```bash
# 1. Valider le JSON
python scripts/validate_json.py requirements.json requirements categories.json

# 2. Générer la commande curl
# Tool MCP: get_import_command
{
  "rfp_id": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "type": "requirements",
  "mode": "append",
  "file_path": "requirements.json"
}

# 3. Exécuter la commande retournée
curl -X POST 'https://app.vercel.app/api/mcp/import-file?rfp_id=xxx&type=requirements&mode=append' \
  -H 'Authorization: Bearer eyJhbGc...' \
  --data-binary @requirements.json

# Résultat:
{
  "created": 500,
  "skipped": 0,
  "errors": []
}
```

### Exemple 3: Import réponses fournisseur

**Contexte:** Réponses du fournisseur "Acme Corp" extraites.

**Workflow:**

```bash
# 1. Valider le JSON
python scripts/validate_json.py responses_acme.json responses

# 2. Obtenir l'ID du fournisseur (ou utiliser le nom)
# Tool MCP: list_suppliers
{
  "rfp_id": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54"
}

# 3. Importer les réponses
# Tool MCP: import_supplier_responses
{
  "rfp_id": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "file_content": "<contenu de responses_acme.json>",
  "supplier_name": "Acme Corp"
}

# Si le fournisseur n'existe pas, il sera créé automatiquement
```

---

## Bonnes pratiques

### ✅ À FAIRE

1. **Toujours valider avant import**
   ```bash
   python scripts/validate_json.py data.json <type> [categories.json]
   ```

2. **Demander confirmation à l'utilisateur**
   ```
   "Je vais importer 108 requirements dans le RFP 'Plateforme CRM 2025'.
    Mode: append (ajout aux données existantes).
    Confirmez-vous?"
   ```

3. **Ordre d'import correct**
   ```
   1. Structure (catégories)
   2. Requirements
   3. Réponses fournisseurs
   ```

4. **Utiliser curl pour gros volumes**
   ```
   > 100 items → get_import_command + curl
   < 100 items → MCP tools
   ```

5. **Gérer les erreurs partielles**
   ```json
   {
     "created": 95,
     "skipped": 2,
     "errors": [
       { "code": "REQ-042", "error": "Category not found" }
     ]
   }
   ```
   → Fixer les 2 items en erreur et réimporter seulement ceux-là

### ❌ À ÉVITER

1. ❌ **Ne jamais importer sans validation**
   - Le serveur rejettera les données invalides
   - Perte de temps et frustration utilisateur

2. ❌ **Ne pas importer les pondérations de catégories**
   - Le schéma catégories n'a PAS de champ `weight`
   - Sera rejeté en validation STRICT

3. ❌ **Ne pas laisser scores `null`**
   - Toujours mapper `null` → `0`
   - Ne jamais omettre le champ

4. ❌ **Ne pas utiliser mode `replace` sans confirmation**
   - `replace` efface TOUTES les données existantes
   - Demander confirmation explicite

5. ❌ **Ne pas ignorer les erreurs**
   - Toujours lire le champ `errors[]`
   - Corriger et réimporter les items en échec

---

## Résumé: Checklist d'import

- [ ] 1. Fichier extrait et JSON généré
- [ ] 2. ✅ **Validation JSON avec `scripts/validate_json.py`**
- [ ] 3. Demander à l'utilisateur: Import direct ou JSON?
- [ ] 4. Obtenir l'ID du RFP (via `get_rfps` si nécessaire)
- [ ] 5. Choisir la méthode (MCP tools vs curl)
- [ ] 6. Demander confirmation du mode (`append` vs `replace`)
- [ ] 7. Exécuter l'import
- [ ] 8. Vérifier les résultats (`created`, `skipped`, `errors`)
- [ ] 9. Gérer les erreurs si présentes
- [ ] 10. Confirmer succès à l'utilisateur

---

**Documentation mise à jour:** 2026-03-06
**Version MCP Server:** 2.0.0
