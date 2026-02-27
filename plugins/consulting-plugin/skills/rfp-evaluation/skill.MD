---
name: rfp-evaluation
description: Évalue systématiquement les réponses des fournisseurs à un appel d'offres (RFP/AO), catégorie par catégorie, avec scores motivés, commentaires comparatifs et questions soutenance. **À utiliser dès qu'un utilisateur mentionne une évaluation d'offres, une analyse comparative de fournisseurs, une notation de propositions, un RFP ou un appel d'offres — même sans explicitement demander ce skill.** Déclencheurs proactifs : "évalue les offres", "lance l'évaluation du RFP", "analyse les réponses fournisseurs", "note les offres", "commence l'évaluation", "démarre l'analyse comparative".
compatibility: Requires MCP "rfp-analyzer" (for requirements & evaluation persistence); Python openpyxl (for Excel export); local access to RFP documents (PDF, Word, Excel).
---

# RFP Evaluation Skill

Évalue de façon systématique et comparative les réponses fournisseurs à un appel d'offres — catégorie par catégorie, tous fournisseurs en parallèle, avec validation utilisateur entre chaque étape. Le MCP rfp-analyzer stocke les exigences, les fournisseurs et les scores.

## Prérequis

- **MCP rfp-analyzer** : configuré et accessible
- **CDC + grille d'exigences** : disponibles localement (PDF, Word, Excel) ou via MCP
- **Réponses fournisseurs** : accessibles localement
- **Python openpyxl** : pour génération Excel

## Workflow en 5 phases

```
Phase 0 : Executive Summary obligatoire → Lire CDC, lister exigences MCP, validation ⏸
Phase 1-4 : Boucle d'évaluation par catégorie → Évaluation croisée, scores, questions → checkpoint ⏸
Phase 5 : Synthèse globale → Classement pondéré → output Excel ou MCP
```

**Voir `docs/WORKFLOW.md` pour le détail complet de chaque phase.**

## Phase 0 — Executive Summary obligatoire

1. Lire CDC intégralement → enjeux, contraintes, critères implicites
2. Via MCP : lister catégories + exigences
3. Rédiger Executive Summary → voir `references/executive_summary_guide.md`
4. ⏸ Présenter à l'utilisateur pour validation

**Si l'utilisateur saute :** lancer directement Phase 1-4 avec rappel des catégories principales.

## Phase 1-4 — Boucle d'évaluation par catégorie

Pour chaque catégorie (ordre hiérarchique MCP) :

1. Annoncer la catégorie : `"Je commence [Nom] ([n] exigences, poids [x%])"`
2. Pour chaque exigence : lire réponses MCP → comparer tous fournisseurs sur base de leurs réponses et des documents fournis → attribuer score 0-5 + commentaire + status
3. Sauvegarder dans MCP via `POST /responses`
4. ⏸ Présenter récap tabulaire (scores × fournisseurs) et attendre validation
   - Utilisateur peut : ✅ Valider → suivant | ✏️ Ajuster note | 🔍 Revoir exigence

**OBLIGATOIRE : Voir `reference/scoring_guide.md` pour les règles de scoring et statuts.**
**Voir `docs/WORKFLOW.md` pour détails scores, statuts, et interactions checkpoints.**

## Phase 5 — Synthèse & Output

1. Générer rapport : classement pondéré global, radar par catégorie, questions soutenance
2. Demander format sortie :
   - **A** : Excel par fournisseur (une feuille par fournisseur)
   - **B** : Excel consolidé (tous fournisseurs en colonnes)
   - **C** : MCP uniquement (garder données dans rfp-analyzer)
3. Si Excel → exporter JSON du MCP → `scripts/generate_evaluation_grid.py`

## Interaction MCP rfp-analyzer

### Endpoints clés

| Endpoint | Usage |
|----------|-------|
| `GET /rfps` | Lister RFPs |
| `GET /rfps/{id}/structure` | Charger catégories + stats |
| `GET /rfps/{id}/requirements-tree` | Hiérarchie exigences |
| `GET /rfps/{id}/suppliers` | Lister fournisseurs |
| `GET /rfps/{id}/responses` | Lister réponses (filtres: supplier_id, requirement_id, status) |
| `POST /rfps/{id}/responses` | Créer/mettre à jour réponse évaluée |
| `GET /rfps/{id}/scoring-matrix` | Matrice scores × fournisseurs |
| `GET /rfps/{id}/defense-synthesis` | Synthèse AI forces/faiblesses |
| `GET /rfps/{id}/soutenance-brief` | Brief Markdown soutenance |

**Documentation complète : voir `docs/MCP-API-reference.md`**

### Validation MCP au démarrage

```
✓ Vérification connexion au MCP rfp-analyzer...
✓ [n] catégories trouvées
✓ [n] exigences trouvées
✓ [n] fournisseurs trouvés
→ Prêt pour l'évaluation
```

Séquence : `GET /rfps/{id}` → `GET /structure` → `GET /suppliers` → `GET /requirements-tree`

## Champs de réponse MCP

Lors de `POST /rfps/{id}/responses` :

- **`ai_score`** (0-5, y compris 0.5) : Note 0-5
- **`ai_comment`** : Commentaire évaluateur (100-300 caractères pour critères critiques)
- **`status`** : "pass" | "partial" | "fail" | "pending" (voir `references/scoring_guide.md`)
- **`question`** : Question soutenance (vide si aucune)

## Ressources & Guides

- **`docs/WORKFLOW.md`** — Phases 1-4 détaillées, checkpoints, interaction utilisateur
- **`docs/MCP-API-reference.md`** — Endpoints MCP complets avec exemples reqts/réponses
- **`docs/INTEGRATION-GUIDE.md`** — Cas particuliers (réevaluation, ajout fournisseur, gestion erreurs)
- **`references/scoring_guide.md`** — Grille notation, règles status, exemples par niveau
- **`references/executive_summary_guide.md`** — Structure ES, sections attendues, template
- **`references/evaluation_workflow.md`** — Workflow détaillé, calcul scores pondérés, scénarios courants
- **`scripts/generate_evaluation_grid.py`** — Génération Excel (Formats A/B avec validation deps)

## Cas particuliers

### Réevaluation ou ajout fournisseur en cours
1. Récupérer scores existants : `GET /rfps/{id}/responses?supplier_id=...`
2. Présenter grille actuelle + contexte nouveau
3. Procéder aux ajustements via `POST /responses`
4. Re-calculer synthèse : `GET /scoring-matrix`

### Sauter l'Executive Summary
- Optionnel. Si utilisateur : "va direct aux évaluations"
- Lancer Phase 1 immédiatement avec rappel catégories principales

### Ajustements lors d'un checkpoint
- Format attendu : `"Ajuster EX-042 de 3 à 4"` ou `"Revoir la catégorie Sécurité en détail"`
- Mettre à jour score via `POST /responses`, re-calculer récap

## Exemple réel — ENGIE Smart Parking

**Contexte :** 82 exigences, 4 fournisseurs (Izix, Sharvy, Cardiweb, Commuty), 6 catégories hiérarchiques.

**Phase 0 :** ES sur enjeux (multisite, Living@ intégration, OKTA SSO, données RGPD)

**Phase 1-4 :** Boucle catégories
- DOM2 "Description fonctionnelle" (37 ex, poids 45%)
- DOM3 "Description technique" (21 ex, poids 35%)
- DOM5/6 "Dispositif/Maintenance" (14 ex, poids 10%)
- Interrupteurs : checkpoints après chaque catégorie

**Phase 5 :** Synthèse
- Scores globaux pondérés : Izix 3.8, Cardiweb 3.5, Sharvy 3.2, Commuty 2.7
- Excel Format A (une feuille par fournisseur) ou Format B (consolidé)