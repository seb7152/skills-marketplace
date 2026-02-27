# MCP-API-reference.md — Endpoints rfp-analyzer détaillés

Documentation de référence pour l'intégration avec le MCP rfp-analyzer.

## Endpoints principaux

### 1. Gestion des RFPs

#### `GET /rfps` — Lister toutes les RFPs

```bash
GET /rfps?limit=50&offset=0

Réponse 200 :
{
  "items": [
    {
      "id": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
      "title": "[ENGIE] Smart Parking",
      "status": "in_progress",
      "createdAt": "2025-12-22T08:32:27.659745+00:00"
    }
  ],
  "_meta": { "total": 4, "limit": 50, "offset": 0, "hasMore": false }
}
```

#### `POST /rfps` — Créer une RFP

```bash
POST /rfps
{
  "title": "[CLIENT] Nom du projet",
  "description": "Description optionnelle",
  "status": "in_progress"
}

Réponse 201 :
{
  "id": "new-uuid-here",
  "title": "[CLIENT] Nom du projet",
  "status": "in_progress",
  "createdAt": "2026-02-27T10:30:00Z"
}
```

#### `GET /rfps/{rfp_id}` — Détails RFP

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54

Réponse 200 :
{
  "id": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "title": "[ENGIE] Smart Parking",
  "description": null,
  "status": "in_progress",
  "organizationId": "b4e485c1-b045-463e-a95e-718d8cdacc62",
  "createdAt": "2025-12-22T08:32:27.659745+00:00"
}
```

#### `PATCH /rfps/{rfp_id}` — Mettre à jour RFP

```bash
PATCH /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54
{
  "title": "Nouveau titre",
  "status": "completed"
}

Réponse 200 : RFP mise à jour
```

### 2. Structure — Catégories et Exigences

#### `GET /rfps/{rfp_id}/structure` — Vue légère (catégories sans exigences)

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/structure?include_stats=true&include_suppliers=true

Réponse 200 :
{
  "id": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "title": "[ENGIE] Smart Parking",
  "categories": [
    {
      "id": "fbfb7293-3fa1-4aa2-86b0-1510c7806cc8",
      "code": "DOM2",
      "title": "Description fonctionnelle des besoins",
      "level": 1,
      "weight": 0.45,
      "aggregateWeight": 0.45,
      "requirementCount": 37,
      "mandatoryCount": 0,
      "children": [
        {
          "id": "83aefc09-e6d5-454d-8ae5-ec069d712cd5",
          "code": "DOM2.1",
          "title": "Grands principes de la solution",
          "level": 2,
          "requirementCount": 8
        }
      ]
    }
  ],
  "suppliers": [
    { "id": "eac4f281-ad1c-4cd1-bea0-ef66ce4b5b4f", "externalId": "IZIX", "name": "Izix" }
  ],
  "stats": {
    "totalCategories": 49,
    "totalRequirements": 82,
    "totalSuppliers": 4,
    "totalResponses": 656
  }
}
```

#### `GET /rfps/{rfp_id}/requirements-tree` — Arbre complet avec exigences

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/requirements-tree?flatten=false

Réponse 200 :
{
  "rfpId": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "rfpTitle": "[ENGIE] Smart Parking",
  "categories": [
    {
      "id": "fbfb7293-3fa1-4aa2-86b0-1510c7806cc8",
      "code": "DOM2",
      "title": "Description fonctionnelle",
      "level": 1,
      "weight": 0.45,
      "children": [
        {
          "id": "83aefc09-e6d5-454d-8ae5-ec069d712cd5",
          "code": "DOM2.1",
          "title": "Grands principes",
          "requirements": [
            {
              "id": "192f26e3-16ed-4674-8c90-3df4e7bca0fc",
              "externalId": "E - 001",
              "title": "Déploiement multisite",
              "description": "La solution doit gérer des contextes multisites...",
              "weight": 0.0225,
              "isMandatory": false
            }
          ]
        }
      ]
    }
  ]
}
```

**Avec `flatten=true` :** retourne liste plate avec `categoryPath` au lieu d'arborescence.

#### `GET /rfps/{rfp_id}/requirements` — Liste paginée

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/requirements?limit=50&offset=0

Réponse 200 :
{
  "items": [
    {
      "id": "192f26e3-16ed-4674-8c90-3df4e7bca0fc",
      "externalId": "E - 001",
      "title": "Déploiement multisite",
      "weight": 0.0225,
      "isMandatory": false,
      "categoryPath": "Description fonctionnelle > Grands principes > Multisite"
    }
  ],
  "_meta": { "total": 82, "limit": 50, "offset": 0, "hasMore": true, "nextOffset": 50 }
}
```

### 3. Fournisseurs

#### `GET /rfps/{rfp_id}/suppliers` — Lister fournisseurs

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/suppliers?limit=50

Réponse 200 :
{
  "items": [
    {
      "id": "eac4f281-ad1c-4cd1-bea0-ef66ce4b5b4f",
      "externalId": "IZIX",
      "name": "Izix",
      "contactName": null,
      "contactEmail": null,
      "contactPhone": null
    },
    {
      "id": "b6b686f3-0936-49dd-8811-1b3e396ab67d",
      "externalId": "SHAR",
      "name": "Sharvy",
      "contactName": "John Doe",
      "contactEmail": "john@sharvy.com",
      "contactPhone": "+33 1 23 45 67 89"
    }
  ],
  "_meta": { "total": 4, "limit": 50, "offset": 0 }
}
```

#### `POST /rfps/{rfp_id}/suppliers` — Ajouter fournisseur

```bash
POST /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/suppliers
{
  "name": "Nouveau Fournisseur",
  "supplier_id_external": "NEW-01",
  "contact_name": "Jean Dupont",
  "contact_email": "jean@new.fr",
  "contact_phone": "+33 1 23 45 67 89"
}

Réponse 201 :
{
  "id": "new-supplier-uuid",
  "externalId": "NEW-01",
  "name": "Nouveau Fournisseur",
  "contactName": "Jean Dupont",
  "contactEmail": "jean@new.fr"
}
```

### 4. Évaluation — Réponses et Scores

#### `GET /rfps/{rfp_id}/responses` — Lister réponses

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/responses?limit=50&offset=0&status=pass

Paramètres optionnels :
  supplier_id=...         Filter by supplier UUID
  requirement_id=...      Filter by requirement UUID
  category_id=...         Filter by category (recursive subtree)
  status=pass|partial|fail|pending
  min_score=2&max_score=4
  has_comment=true
  version_id=...

Réponse 200 :
{
  "items": [
    {
      "id": "response-uuid",
      "requirementId": "192f26e3-16ed-4674-8c90-3df4e7bca0fc",
      "requirement_id_external": "E - 001",
      "supplierId": "eac4f281-ad1c-4cd1-bea0-ef66ce4b5b4f",
      "supplier_name": "Izix",
      "response_text": "Notre solution supporte 50 sites...",
      "ai_score": 4.5,
      "manual_score": null,
      "ai_comment": "Réponse très complète couvrant multisite, architecture...",
      "manual_comment": null,
      "status": "pass",
      "question": "Pouvez-vous préciser la latence ?",
      "is_checked": false,
      "updatedAt": "2026-02-27T10:30:00.000Z"
    }
  ],
  "_meta": { "total": 8, "limit": 50, "offset": 0 }
}
```

#### `POST /rfps/{rfp_id}/responses` — Créer ou mettre à jour réponse

```bash
POST /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/responses
{
  "supplier_id": "eac4f281-ad1c-4cd1-bea0-ef66ce4b5b4f",
  "requirement_id": "192f26e3-16ed-4674-8c90-3df4e7bca0fc",
  "response_text": "Notre solution supporte 50 sites en architecture multi-cloud...",
  "ai_score": 4.5,
  "manual_score": null,
  "ai_comment": "Réponse très complète couvrant multisite, architecture, références",
  "manual_comment": null,
  "status": "pass",
  "question": "Pouvez-vous préciser la latence de réplication entre les sites ?",
  "is_checked": false,
  "version_id": null
}

Réponse 201 ou 200 :
{
  "id": "response-uuid",
  "created": true,
  "updated": false,
  "updatedAt": "2026-02-27T10:45:30.000Z"
}
```

#### `GET /rfps/{rfp_id}/scoring-matrix` — Matrice scores × fournisseurs

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/scoring-matrix?category_id=fbfb7293...

Réponse 200 :
{
  "rfpId": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "rfpTitle": "[ENGIE] Smart Parking",
  "categoryMatrices": [
    {
      "category": {
        "id": "fbfb7293-3fa1-4aa2-86b0-1510c7806cc8",
        "code": "DOM2",
        "title": "Description fonctionnelle des besoins",
        "weight": 0.45
      },
      "suppliers": {
        "IZIX": 4.2,
        "SHAR": 3.1,
        "CARDI": 3.8,
        "COMU": 2.9
      }
    },
    {
      "category": {
        "id": "7c791cdc-367b-46f0-a4bc-2d52b8b27d70",
        "code": "DOM3",
        "title": "Description technique de la solution",
        "weight": 0.35
      },
      "suppliers": {
        "IZIX": 3.9,
        "SHAR": 2.8,
        "CARDI": 3.3,
        "COMU": 2.4
      }
    }
  ],
  "globalScores": {
    "IZIX": 3.82,
    "SHAR": 3.15,
    "CARDI": 3.48,
    "COMU": 2.68
  }
}
```

### 5. Synthèse

#### `GET /rfps/{rfp_id}/defense-synthesis` — Synthèse forces/faiblesses

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/defense-synthesis?supplier_id=eac4f281...

Réponse 200 :
{
  "rfpId": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "suppliers": [
    {
      "supplierId": "eac4f281-ad1c-4cd1-bea0-ef66ce4b5b4f",
      "supplierName": "Izix",
      "categories": [
        {
          "categoryId": "fbfb7293-3fa1-4aa2-86b0-1510c7806cc8",
          "categoryTitle": "Description fonctionnelle",
          "forces": [
            "Architecture multisite robuste avec 50+ références",
            "API documentée et testée en intégration"
          ],
          "faiblesses": [
            "Coûts d'intégration Interparking élevés"
          ],
          "pointsQuestion": [
            "Isolation des données en SaaS mutualisé ?"
          ]
        }
      ]
    }
  ]
}
```

#### `GET /rfps/{rfp_id}/soutenance-brief` — Brief Markdown

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/soutenance-brief?supplier_id=eac4f281...

Réponse 200 :
{
  "rfpId": "4fef2cbb-30df-45af-a1ce-f9fa11ec2d54",
  "suppliers": [
    {
      "supplierId": "eac4f281-ad1c-4cd1-bea0-ef66ce4b5b4f",
      "supplierName": "Izix",
      "status": "completed",
      "report_markdown": "# Brief de soutenance — Izix\n\n## Points faibles ou partiels\n\n### Catégorie : Description fonctionnelle\n\n**EX-042** (Interfaçage Interparking) — Score 2 (Partiel)\n- Actuellement : Solution RPA temporaire\n- À la soutenance : Préciser si API Interparking disponible\n\n## Questions prioritaires\n\n1. **Isolation des données SaaS**\n   - Garantie d'isolation tenants en cas de charge client ?\n..."
    }
  ]
}
```

### 6. Import/Export Masse

#### `POST /rfps/{rfp_id}/import/categories` — Bulk import catégories

```bash
POST /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/import/categories
{
  "mode": "replace",  // ou "append"
  "categories": [
    {
      "id": "CAT-001",
      "code": "DOM2",
      "title": "Description fonctionnelle",
      "level": 1,
      "parent_id": null,
      "weight": 0.45,
      "short_name": "D2",
      "display_order": 2
    }
  ]
}

Réponse 201 :
{
  "imported": 1,
  "updated": 0,
  "errors": []
}
```

#### `POST /rfps/{rfp_id}/import/requirements` — Bulk import exigences

```bash
POST /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/import/requirements
{
  "mode": "append",
  "requirements": [
    {
      "code": "E - 001",
      "title": "Déploiement multisite",
      "description": "La solution doit gérer...",
      "weight": 0.0225,
      "category_name": "DOM2",
      "is_mandatory": false
    }
  ]
}

Réponse 201 :
{
  "imported": 1,
  "updated": 0,
  "errors": []
}
```

#### `POST /rfps/{rfp_id}/import/responses` — Bulk import réponses

```bash
POST /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/import/responses
{
  "supplier_name": "Izix",
  "mode": "upsert",
  "version_id": null,
  "responses": [
    {
      "requirement_id_external": "E - 001",
      "response_text": "Notre solution supporte 50 sites...",
      "ai_score": 4.5,
      "status": "pass",
      "ai_comment": "Réponse très complète"
    }
  ]
}

Réponse 201 :
{
  "imported": 1,
  "updated": 0,
  "errors": []
}
```

### 7. Versions

#### `GET /rfps/{rfp_id}/versions` — Lister versions d'évaluation

```bash
GET /rfps/4fef2cbb-30df-45af-a1ce-f9fa11ec2d54/versions

Réponse 200 :
{
  "versions": [
    {
      "id": "version-uuid-001",
      "number": 1,
      "name": "Version 1 — Première évaluation",
      "status": "completed",
      "active": false,
      "createdAt": "2026-01-15T...",
      "completedAt": "2026-02-20T..."
    },
    {
      "id": "version-uuid-002",
      "number": 2,
      "name": "Version 2 — Post-soutenance",
      "status": "in_progress",
      "active": true,
      "createdAt": "2026-02-20T..."
    }
  ]
}
```

## Validation au démarrage

**Séquence appelée automatiquement :**

1. `GET /rfps/{rfp_id}` → Valider RFP existe
2. `GET /rfps/{rfp_id}/structure` → Charger catégories + stats
3. `GET /rfps/{rfp_id}/suppliers` → Charger fournisseurs
4. `GET /rfps/{rfp_id}/requirements-tree?flatten=true` → Charger exigences

**Output attendu :**
```
✓ Vérification connexion au MCP rfp-analyzer...
✓ 49 catégories trouvées
✓ 82 exigences trouvées
✓ 4 fournisseurs trouvés
→ Prêt pour l'évaluation
```

---

**Documentation détaillée complète des workflows : voir `docs/WORKFLOW.md`**