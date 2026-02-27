---
name: rfp-evaluation
description: Évalue les réponses des fournisseurs à un appel d'offres (RFP/AO), exigence par exigence et catégorie par catégorie, en s'appuyant sur le serveur MCP rfp-analyzer et les documents locaux (PDF, Word, Excel). Produit des scores motivés, des commentaires comparatifs et identifie les points à éclaircir en soutenance. À déclencher proactivement lorsqu'un utilisateur mentionne une évaluation d'offres, une analyse comparative de fournisseurs ou une notation de soumissions — même sans le mot "skill". Déclencheurs : "évalue les offres", "lance l'évaluation du RFP", "analyse les réponses fournisseurs", "note les offres", "commence l'évaluation", "démarre l'analyse comparative", "évalue les propositions".
---

# RFP Evaluation

Évalue de façon systématique les réponses fournisseurs à un AO — catégorie par catégorie, tous fournisseurs en parallèle, avec checkpoint utilisateur entre chaque catégorie. Le MCP rfp-analyzer stocke les exigences et persiste les scores ; les documents restent en local.

## Prérequis

- MCP `rfp-analyzer` configuré et accessible
- CDC + grille d'exigences disponibles localement
- Réponses fournisseurs disponibles (localement ou au fil de l'eau)
- Exigences déjà importées dans rfp-analyzer — sinon déclencher **rfp-import-extractor** en premier

## Workflow

```
Phase 0 : Lecture CDC + grille MCP → Executive Summary → validation ⏸
      ↓
Boucle par catégorie :
  Phase 1-4 : Lecture exigences → évaluation croisée → deep dive si besoin
              → score + commentaire + status + question → sauvegarde MCP
              → récap catégorie → checkpoint ⏸
      ↓
Phase 5 : Synthèse globale → classement pondéré → output
```

## Phase 0 — Executive Summary

1. Lire le CDC intégralement (enjeux, contraintes, critères implicites) — **avant** d'ouvrir les offres
2. Via MCP : lister catégories + exigences (poids, `is_mandatory`)
3. Rédiger l'Executive Summary → voir `references/executive_summary_guide.md`
4. ⏸ Présenter à l'utilisateur et attendre validation avant d'évaluer

## Phase 1-4 — Boucle d'évaluation par catégorie

Pour chaque catégorie dans l'ordre hiérarchique rfp-analyzer :

1. Annoncer : `"Je commence la catégorie [Nom] ([n] exigences, poids [x%])"`
2. Pour chaque exigence : lire réponses MCP → comparer tous fournisseurs simultanément → deep dive documents locaux si réponse vague ou référence externe
3. Attribuer score 0-5 + `ai_comment` + `status` + `question` soutenance → sauvegarder dans MCP → voir `references/scoring_guide.md`
4. ⏸ Présenter le récap tabulaire catégorie et attendre validation — voir `references/evaluation_workflow.md`

**Document manquant** → `status: "pending"`, ne pas mettre score 0.

## Phase 5 — Synthèse & Output

1. Produire : classement pondéré global, radar comparatif par catégorie, points forts/faiblesses par fournisseur, questions soutenance prioritaires
2. Demander le format : **A** Excel par fournisseur | **B** Excel consolidé | **C** MCP uniquement
3. Si Excel → `scripts/generate_evaluation_grid.py` (exporter les données MCP en JSON d'abord)

## Interaction MCP rfp-analyzer

**Lecture** : catégories (hiérarchie), exigences (weight, is_mandatory, description), fournisseurs, réponses (response_text)

**Écriture** par réponse évaluée : `ai_score` (0-5, pas de 0.5) · `ai_comment` · `status` (pass/partial/fail/pending) · `question`

**Erreur MCP** → continuer localement dans `responses_evaluation_[date].json`, importer ensuite via rfp-import-extractor

## Ressources

- `references/scoring_guide.md` — grille 0-5, règles status, profondeur des commentaires, exemples
- `references/executive_summary_guide.md` — structure et template de l'Executive Summary (Phase 0)
- `references/evaluation_workflow.md` — workflow détaillé, deep dive, checkpoints, calcul scores pondérés, scénarios
- `scripts/generate_evaluation_grid.py` — génération Excel (Format A par fournisseur, Format B consolidé)
