# WORKFLOW.md — Phases détaillées et interactions utilisateur

Document de référence pour les phases 1-4 du processus d'évaluation RFP.

## Phase 1-4 — Boucle d'évaluation par catégorie

### Exemple de flux

**Annonce de catégorie :**
```
"Je commence la catégorie : Description fonctionnelle des besoins
 • 37 exigences
 • Poids global : 45%
 • Fournisseurs : Izix, Sharvy, Cardiweb, Commuty
 
 Je vais évaluer chaque exigence en comparant les 4 réponses."
```

### Pour chaque exigence

**Étapes :**

1. **Lire l'exigence** depuis MCP
   ```
   Exigence : E - 001 "Déploiement multisite"
   Code : DOM2.1.1
   Poids : 0.0225
   Description : "La solution doit gérer des contextes multisites..."
   ```

2. **Consulter les réponses MCP** (ou documents locaux si manquantes)
   ```
   GET /rfps/{id}/responses?requirement_id=192f26e3...
   
   Retour : réponses des 4 fournisseurs pour cette exigence
   ```

3. **Analyser en comparaison croisée**
   - Comparer **simultanément** les 4 réponses
   - Identifier différences clés, points forts/faibles
   - Consulter documents externes si réponse vague (voir "Deep dive")

4. **Attribuer le score** (0-5)
   - **5** : Répond complètement, démontre expertise, références solides
   - **4** : Répond très bien, quelques clarifications mineures
   - **3** : Répond de manière satisfaisante, clarifications attendues
   - **2** : Répond partiellement, clarifications majeures
   - **1** : Répond très partiellement
   - **0** : Ne répond pas ou document manquant
   - Voir `references/scoring_guide.md` pour grille détaillée

5. **Sauvegarder la réponse évaluée** dans MCP
   ```
   POST /rfps/{id}/responses
   {
     "supplier_id": "eac4f281...",
     "requirement_id": "192f26e3...",
     "response_text": "Notre solution supporte 50 sites...",
     "ai_score": 4.5,
     "ai_comment": "Réponse très complète couvrant multisite, architecture...",
     "status": "pass",
     "question": "Pouvez-vous préciser la latence de réplication ?"
   }
   ```

### Champs obligatoires à chaque évaluation

| Champ | Type | Exemple | Notes |
|-------|------|---------|-------|
| `ai_score` | 0-5 | 4.5 | Inclut 0.5 (ex: 3.5 = entre 3 et 4) |
| `ai_comment` | string | "Réponse très complète couvrant..." | 100-300 caractères pour critères critiques |
| `status` | enum | "pass" \| "partial" \| "fail" \| "pending" | Voir règles ci-dessous |
| `question` | string (optionnel) | "Préciser latence ?" | Pour soutenance si besoin clarification |

### Règles de `status`

- **"pass"** : Score ≥ 3.5, exigence satisfaite
- **"partial"** : Score 2-3.5, clarifications attendues à soutenance
- **"fail"** : Score < 2, exigence non satisfaite ou manquante
- **"pending"** : Document manquant, ne pas mettre score 0

**Important :** Ne pas mettre score 0 si document manquant → `status: "pending"` au lieu.

### Deep dive — Consulter documents locaux

Si réponse fournisseur est vague ou référence externe (ex: "voir annexe 12") :

1. **Localiser le document** (PDF, Word, Excel)
2. **Consulter directement** la section/annexe
3. **Compléter évaluation** avec informations trouvées
4. **Documenter dans `ai_comment`** : "Réponse + consultation PDF page 45 annexe technique"

### Checkpoint — Fin de catégorie

Après avoir évalué toutes les exigences de la catégorie :

#### 1. Présenter le récap tabulaire

```
╔═══════════════════════════════════════════════════════════════════╗
║ Catégorie : Description fonctionnelle (37 exigences, poids 45%)   ║
╠═══════════════════════════════════════════════════════════════════╣
║ Exigence             │ Izix │ Sharvy │ Cardiweb │ Commuty │ Moy  ║
╠═══════════════════════════════════════════════════════════════════╣
║ E-001 Multisite      │ 4.5  │  3.0   │   3.8    │  2.9   │ 3.55 ║
║ E-002 Langues        │ 5.0  │  4.0   │   4.5    │  3.5   │ 4.25 ║
║ E-003 Solution adapt │ 4.0  │  2.5   │   3.5    │  2.0   │ 3.00 ║
║ ...                  │ ...  │  ...   │   ...    │  ...   │ ...  ║
╠═══════════════════════════════════════════════════════════════════╣
║ Moyenne catégorie    │ 4.2  │  3.1   │   3.8    │  2.9   │      ║
║ Pondération          │ 45%  │ 45%    │   45%    │ 45%    │      ║
╚═══════════════════════════════════════════════════════════════════╝

⚠️ Alertes :
  • Commuty < 3 sur 3 exigences (E-003, E-005, E-007)
  • Sharvy : E-010 "granularité" à clarifier en soutenance

📋 Questions prioritaires pour soutenance :
  • Izix : Coûts d'intégration Interparking ?
  • Cardiweb : Support multi-tenant à préciser
```

#### 2. Proposer trois options à l'utilisateur

**Format attendu pour les actions :**

```
✅ Valider → Passer à la catégorie suivante

✏️  Ajuster une note
   Format : "Ajuster EX-042 de 3 à 4" ou "Modifier EX-010 Sharvy : 2.5 → 3"
   Action : Re-sauvegarder dans MCP, re-calculer moyenne catégorie

🔍 Revoir une exigence en détail
   Format : "Revoir E-005" ou "Deep dive catégorie Sécurité"
   Action : Revenir à l'exigence spécifique, afficher réponses, consulting docs
```

#### 3. Attendre validation avant suivant

Ne pas passer à la catégorie suivante avant validation de l'utilisateur.

### Exemple complet — Une exigence

**Exigence :** E-006 "API et connectivité"
```
Poids : 0.0113
Description : "Afin de pouvoir assurer une intégration forte de la solution 
avec Living@, la solution devra disposer d'API permettant les échanges de 
données entre les systèmes. Le soumissionnaire précisera les fonctionnalités 
exposées via ses API."
```

**Réponses fournisseurs :**

| Fournisseur | Réponse | Notes |
|-------------|---------|-------|
| **Izix** | "API REST documentée (OpenAPI 3.0), endpoints pour réservation, état places, notifications. Webhook pour intégration asynchrone. Exemples Python/JS." | Complète, documentée, références |
| **Sharvy** | "API fournie. Détails en annexe technique." | Vague, à consulter annexe |
| **Cardiweb** | "API REST, endpoints standard CRUD pour réservations et utilisateurs. Doc PDF interne." | Basique, pas de webhook |
| **Commuty** | "Pas d'API exposée. Intégration via ETL uniquement." | Pas de réponse adéquate |

**Scores attribués :**

```
Izix     : 4.5  (Réponse très complète, API moderne, exemples code)
Sharvy   : 2.5  (Réponse vague, mais API existe — à consulter annexe)
Cardiweb : 3.0  (API basique, pas de webhook, CRUD standard)
Commuty  : 1.0  (Pas d'API, ETL seul = très limitant pour Living@)

Statuts  : Izix/Cardiweb/Sharvy = "pass", Commuty = "partial"

Questions soutenance :
  • Sharvy : Préciser endpoints disponibles via API ?
  • Commuty : Comment gérer webhook Living@ sans API ?
```

**Sauvegarde MCP :**
```json
[
  {
    "supplier_id": "eac4f281-ad1c-4cd1-bea0-ef66ce4b5b4f",  // Izix
    "requirement_id": "80847b92-2026-41f0-b371-8726e9771976",
    "response_text": "API REST documentée (OpenAPI 3.0)...",
    "ai_score": 4.5,
    "ai_comment": "Réponse très complète, API moderne avec OpenAPI 3.0, webhook asynchrone, exemples code Python/JS. Très bon pour intégration Living@.",
    "status": "pass",
    "question": ""
  },
  {
    "supplier_id": "b6b686f3-0936-49dd-8811-1b3e396ab67d",  // Sharvy
    "requirement_id": "80847b92-2026-41f0-b371-8726e9771976",
    "response_text": "API fournie. Détails en annexe technique.",
    "ai_score": 2.5,
    "ai_comment": "Réponse très vague. API existe mais détails non fournis directement. À consulter annexe technique pour clarifications endpoints.",
    "status": "partial",
    "question": "Quels endpoints API sont disponibles pour intégration Living@ ?"
  },
  // ... Cardiweb et Commuty ...
]
```

## Gestion des ajustements au checkpoint

### Scénario : L'utilisateur veut ajuster un score

**Utilisateur :** `"Ajuster Sharvy de 2.5 à 3.5 pour E-006"`

**Actions :**
1. Récupérer la réponse existante via `GET /rfps/{id}/responses?supplier_id=sharvy&requirement_id=E-006`
2. Mettre à jour via `POST /rfps/{id}/responses` avec nouveau score
3. Recalculer la moyenne catégorie
4. Afficher nouveau récap tabulaire
5. Demander nouvelle validation

**Nouveau récap :**
```
Moyenne catégorie E-006 : (4.5 + 3.5 + 3.0 + 1.0) / 4 = 3.0  (au lieu de 2.75)
```

## Calcul des scores pondérés

### Par catégorie

```
score_catégorie = Σ(score_exigence_i × weight_i) / Σ(weight_i)

Exemple DOM2 "Description fonctionnelle" :
  E-001 (weight 0.0225) : Izix = 4.5 → 0.10125
  E-002 (weight 0.0225) : Izix = 5.0 → 0.1125
  ...
  Σ scores pondérés = X
  Σ poids = 0.45
  
  Score Izix DOM2 = X / 0.45 = 4.2
```

### Global (tous fournisseurs)

```
score_global = Σ(score_catégorie_k × poids_catégorie_k) / Σ(poids_catégorie_k)

Exemple global Izix (6 catégories) :
  DOM2 (45%) : 4.2
  DOM3 (35%) : 3.9
  DOM5 (5%) : 3.5
  DOM6 (10%) : 3.8
  ...
  
  Score global = (4.2×0.45 + 3.9×0.35 + 3.5×0.05 + 3.8×0.10) = 3.82
```

**Note :** Les scores "pending" (null) sont **exclus** du calcul.

## Scénarios courants

### Scénario 1 : Réevaluation après soutenance

**Contexte :** Après soutenance, utilisateur veut réviser quelques scores suite à clarifications.

**Actions :**
1. Identifier exigences à révaluer (ex: "E-042 et E-051")
2. Récupérer les réponses existantes : `GET /rfps/{id}/responses?requirement_id=E-042&requirement_id=E-051`
3. Présenter contexte soutenance + réponses existantes
4. Utilisateur donne nouveaux scores
5. `POST /responses` pour mettre à jour
6. Recalculer matrix scoring
7. Afficher nouveau classement global

### Scénario 2 : Ajout d'un fournisseur en cours

**Contexte :** Utilisateur ajoute un 5e fournisseur en cours d'évaluation (ex: catégorie 3 sur 6 complétée).

**Actions :**
1. `POST /rfps/{id}/suppliers` pour ajouter le fournisseur
2. Marquer les catégories 1-2 comme "pending" pour le nouveau fournisseur
3. Continuer catégorie 3 avec 5 fournisseurs au lieu de 4
4. Recalculer checkpoints avec nouveau nombre de colonnes

### Scénario 3 : Utilisateur saute Executive Summary

**Contexte :** Utilisateur : "Va direct aux évaluations, pas besoin de synthèse préalable"

**Actions :**
1. Confirmer : "OK, on lance Phase 1-4 directement"
2. Afficher récap rapide des catégories principales :
   ```
   Catégories principales :
   • DOM2 "Description fonctionnelle" (37 ex, 45%)
   • DOM3 "Description technique" (21 ex, 35%)
   • DOM5/6 "Dispositif & Maintenance" (24 ex, 20%)
   ```
3. Lancer Phase 1 sans ES

---

**Voir `references/scoring_guide.md` pour la grille de notation détaillée par niveau critique.**