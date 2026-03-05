# Workflow détaillé — RFP Evaluation

Ce document décrit le processus d'évaluation phase par phase, avec les points de décision, les pièges à éviter et les interactions attendues avec l'utilisateur.

---

## Vue d'ensemble du flux

```
┌─────────────────────────────────────────────────────────────┐
│  INITIALISATION                                             │
│  Vérif prérequis → Identification fournisseurs → Go/No Go  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  PHASE 0 — EXECUTIVE SUMMARY                                │
│  Lecture CDC → Lecture grille MCP → Rédaction ES            │
│  → Validation utilisateur ✅                                │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  BOUCLE PAR CATÉGORIE                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Pour chaque exigence de la catégorie :             │   │
│  │  Lecture → Évaluation tous fournisseurs → Deep dive │   │
│  │  → Score + Commentaire + Status + Question MCP      │   │
│  └──────────────────────────────────────────┬──────────┘   │
│                                             │               │
│  Récap catégorie → Checkpoint utilisateur ✅ │               │
│  → Ajustements si demandés → Catégorie suivante            │
└──────────────────────────────┬──────────────────────────────┘
                               │ (toutes catégories traitées)
┌──────────────────────────────▼──────────────────────────────┐
│  PHASE 5 — SYNTHÈSE & OUTPUT                                │
│  Scores globaux → Classement → Rapport → Format output      │
└─────────────────────────────────────────────────────────────┘
```

---

## Initialisation

### Checklist d'ouverture

Avant de commencer, poser les questions suivantes à l'utilisateur si l'information n'est pas disponible :

**Sur le projet :**
- "Quel est le nom ou référence de cet appel d'offres ?"
- "Est-il déjà dans RFP-analyzer ?"
- "Combien de fournisseurs sont en compétition ?"
- "Quels sont leurs noms ?" (pour les retrouver dans rfp-analyzer)

**Sur les documents :**
- "Où se trouvent les documents du CDC et de la grille d'exigences ?"
- "Les réponses fournisseurs sont-elles dans un dossier structuré ou à fournir au fil de l'eau ?"
- "Les exigences sont-elles déjà chargées dans rfp-analyzer, ou dois-je lancer rfp-import-extractor d'abord ?"

**Vérification MCP :**
- Tester la connexion au MCP rfp-analyzer
- Vérifier que les catégories et exigences sont bien présentes
- Vérifier que les fournisseurs sont bien référencés

### Si les exigences ne sont pas dans rfp-analyzer

```
"Je ne trouve pas les exigences dans rfp-analyzer pour ce projet.
Il faut d'abord importer la grille d'exigences.
Voulez-vous que je déclenche le skill rfp-import-extractor sur votre fichier
[chemin/fichier] ?"
```

→ Attendre la fin de l'import avant de continuer.

---

## Phase 0 — Executive Summary

### Ordre de lecture recommandé

1. **D'abord le CDC** (vue d'ensemble, contexte, contraintes)
2. **Ensuite la grille MCP** (structure, exigences, poids)
3. **Croiser** pour identifier les points structurants

### Biais à éviter

- Ne pas lire les offres fournisseurs avant de finir l'Executive Summary (risque de biais)
- Ne pas se laisser influencer par le poids d'un fournisseur connu
- Garder un regard critique sur les exigences mal formulées dans le CDC

### Indicateurs d'un ES de qualité

✅ L'utilisateur peut corriger des incompréhensions avant l'évaluation
✅ Les exigences éliminatoires sont toutes listées
✅ Les 3-5 points qui feront vraiment la différence sont identifiés
✅ Les zones ambiguës sont signalées avec une recommandation d'évaluation

---

## Boucle d'évaluation par catégorie

### Ordre de traitement des catégories

Respecter l'ordre hiérarchique défini dans rfp-analyzer :
1. Catégories de niveau 1 dans l'ordre de leur `order` (ou code)
2. Traiter les sous-catégories d'une catégorie parent avant de passer au parent suivant

Si aucun ordre n'est défini : traiter par ordre alphabétique de code.

### Gestion des fournisseurs avec documents manquants

Si un fournisseur n'a pas encore fourni sa réponse pour une exigence :

**Option A — Le document entier est manquant :**
```
Statut à sauvegarder dans MCP :
  ai_score: null (ne pas mettre 0)
  ai_comment: "Document non encore reçu — évaluation en attente"
  status: "pending"
```
Ne pas pénaliser avec un score 0 : le document peut arriver plus tard.

**Option B — Le document est présent mais l'exigence n'est pas traitée :**
→ Faire un deep dive avant de conclure à l'absence de réponse (score 0).

### Règles du deep dive (Phase 3)

**Déclencher le deep dive si :**
- La réponse dans le MCP est vide ET le document fournisseur est disponible localement
- La réponse contient une référence externe ("cf. annexe 3", "voir notre documentation")
- La réponse est générique et ne contient aucun élément vérifiable
- Il y a une incohérence avec d'autres réponses du même fournisseur
- L'exigence est obligatoire ET le score pressenti est ≤ 2

**Méthode de deep dive :**
1. Identifier les mots-clés de l'exigence (3-5 termes pertinents)
2. Chercher ces termes dans les documents du fournisseur (PDF, Word, Excel)
3. Lire les sections identifiées en contexte
4. Décider : est-ce que le document apporte des éléments supplémentaires ?

**Dans le commentaire, toujours mentionner :**
> "Suite à lecture du [nom document], section [X] : [élément trouvé/non trouvé]."

---

## Checkpoint catégorie — Guide de présentation

### Format du récapitulatif

```markdown
## 📊 Catégorie : [Nom] — Récapitulatif

**[N] exigences évaluées** | Poids total : [x%] de la grille globale

### Tableau des scores

| Code   | Titre              | Poids | Oblig. | Fourn. A | Fourn. B | Fourn. C |
|--------|--------------------|-------|--------|----------|----------|----------|
| EX-001 | [Titre court]      | 0.8   |   🔴   |   4 ✅   |   2 ❌   |   3 ✅   |
| EX-002 | [Titre court]      | 0.6   |        |   3 ✅   |   3 ✅   |   5 ✅   |
| EX-003 | [Titre court]      | 0.4   |        |   2 ⚠️   |   4 ✅   |   2 ⚠️   |

Légende : ✅ pass | ⚠️ partial | ❌ fail

### Scores pondérés de la catégorie

| Fournisseur | Score brut moyen | Score pondéré | Rang catégorie |
|-------------|------------------|---------------|----------------|
| Fournisseur A |      3.0       |      3.2      |      2ème      |
| Fournisseur B |      3.0       |      2.6      |      3ème      |
| Fournisseur C |      3.3       |      3.5      |      1er       |

### Points d'alerte
- 🔴 Fournisseur B : score 2 sur EX-001 (obligatoire) → statut FAIL éliminatoire
- ⚠️ Fournisseurs A et C : EX-003 à améliorer (poids 0.4, non bloquant)

### Questions soutenance identifiées : [N]
- EX-001 / Fournisseur B : [texte question]
- ...
```

### Questions à l'utilisateur au checkpoint

```
"Le récapitulatif de la catégorie [Nom] est prêt.
Souhaitez-vous :
1. ✅ Valider et passer à la catégorie suivante [Nom catégorie suivante]
2. ✏️ Ajuster certaines notes ou commentaires
3. 🔍 Revoir une exigence spécifique en détail
```

---

## Calcul des scores pondérés

### Formule

Pour chaque fournisseur dans une catégorie :

```
Score_pondéré_catégorie = Σ(score_i × weight_i) / Σ(weight_i)
```

Pour le score global :

```
Score_pondéré_global = Σ(score_pondéré_catégorie_k × poids_catégorie_k) / Σ(poids_catégorie_k)
```

Le poids d'une catégorie est calculé comme la somme des poids de ses exigences (ou utiliser le poids de la catégorie si défini dans rfp-analyzer).

### Gestion des scores null (documents manquants)

- Exclure du calcul les exigences avec status `pending`
- Mentionner explicitement dans le récap : "Score calculé sur [n] exigences évaluées / [total]"

### Traitement des fail éliminatoires

Un fournisseur avec `fail` sur une exigence `is_mandatory` :
- Conserver son score pondéré calculé
- Ajouter un marqueur **🔴 ALERTE ÉLIMINATOIRE** dans tous les tableaux
- Recommander en synthèse finale une décision go/no-go

---

## Phase 5 — Synthèse finale

### Rapport de synthèse (structure recommandée)

```markdown
# Synthèse évaluation RFP — [Nom projet] — [Date]

## 1. Classement général

| Rang | Fournisseur | Score global pondéré | Alertes éliminatoires |
|------|-------------|---------------------|----------------------|
|  1   | Fournisseur C |       3.8         |         —            |
|  2   | Fournisseur A |       3.4         |         —            |
|  3   | Fournisseur B |       2.9         | 🔴 EX-001, EX-015   |

## 2. Analyse comparative par catégorie

[Tableau ou radar textuel comparant les scores par catégorie]

## 3. Points forts et faiblesses par fournisseur

### Fournisseur A
- ✅ Points forts : [top 3]
- ⚠️ Points de vigilance : [top 3]
- 🔴 Points éliminatoires : aucun

### Fournisseur B
...

## 4. Risques et recommandations

### Risques identifiés
- [Fournisseur + exigence + nature du risque]

### Questions soutenance prioritaires
[Top 5 questions classées par criticité]

### Recommandation
[Recommandation argumentée : fournisseur(s) à sélectionner, conditions, vigilances]
```

### Décision sur le format output

Après la synthèse, toujours demander explicitement :
```
"Souhaitez-vous un export de la grille d'évaluation en Excel ?
Si oui, quel format préférez-vous :
  A — Une feuille par fournisseur + feuille de synthèse
  B — Une feuille unique avec tous les fournisseurs en colonnes
  C — Les données sont déjà dans rfp-analyzer, pas besoin d'export Excel"
```

Si Excel souhaité → utiliser `scripts/generate_evaluation_grid.py`

---

## Gestion des situations particulières

### Réponse contradictoire entre la réponse directe et les annexes

Si le texte de réponse dit "oui" mais qu'un document annexe contredit cette affirmation :
1. Score basé sur la réalité documentée (pénaliser si contradiction)
2. Mentionner explicitement la contradiction dans le commentaire
3. Ajouter une question soutenance obligatoire

### Exigence avec plusieurs sous-parties

Si une exigence contient clairement plusieurs sous-points (A, B, C) :
1. Évaluer chaque sous-point mentalement
2. Le score final est la moyenne pondérée (donner plus de poids aux sous-points critiques)
3. Le commentaire doit détailler le score pour chaque sous-point

### Fournisseur qui répond "non" clairement

Ne pas pénaliser une réponse honnête "non" de la même façon qu'une réponse vague :
- "Non, nous ne supportons pas X actuellement, mais le développement est prévu pour Q2 2025" → score 2 (partiel, engagement futur)
- "Non" sans explication → score 1 (hors sujet / refus non étayé)

### Deep dive négatif (document parcouru, rien trouvé)

```
"Suite à lecture complète du dossier technique ([nom document], [n] pages),
aucune mention de [thème exigence] n'a été identifiée. Le score reste à [n]."
```

---

## Checklist de fin d'évaluation

Avant de passer à la synthèse, vérifier :

- [ ] Toutes les catégories ont été évaluées
- [ ] Tous les scores ont été sauvegardés dans le MCP
- [ ] Les exigences obligatoires avec `fail` sont signalées
- [ ] Les questions soutenance sont enregistrées dans le champ `question` MCP
- [ ] Les documents manquants (status `pending`) sont identifiés et documentés
- [ ] L'utilisateur a validé chaque checkpoint catégorie

---

## Bonnes pratiques

1. **Toujours lire l'exigence entièrement** avant d'évaluer — ne jamais noter sur le titre seul
2. **Comparer systématiquement** — la note d'un fournisseur ne se comprend qu'en regard des autres
3. **Être précis dans les commentaires** — "réponse vague" ne suffit pas, dire ce qui manque exactement
4. **Proportionner l'effort** au poids — ne pas passer autant de temps sur une exigence à 0.2 qu'à 0.9
5. **Documenter les deep dives** — mentionner quel document et quelle section ont été consultés
6. **Ne pas deviner** — si une réponse est ambiguë, le dire dans le commentaire et poser une question soutenance
7. **Checkpoint catégorie systématique** — ne jamais passer à la catégorie suivante sans validation

---

## Scénarios courants

### Scénario 1 : Évaluation complète depuis zéro
L'utilisateur fournit un dossier avec CDC, grille et réponses fournisseurs.

1. Vérifier que les exigences sont dans rfp-analyzer (sinon → rfp-import-extractor)
2. Demander les noms des fournisseurs et la structure de leurs dossiers
3. Lancer Phase 0 → Executive Summary → validation
4. Boucle catégorie par catégorie avec checkpoints
5. Synthèse + output choisi par l'utilisateur

### Scénario 2 : Ajout d'un fournisseur en cours d'évaluation
L'évaluation est déjà commencée, un nouveau dossier arrive.

1. Confirmer : "Je vais évaluer [Fournisseur X] sur toutes les catégories déjà traitées, puis continuer en parallèle. Confirmez ?"
2. Reprendre depuis la première catégorie pour ce fournisseur
3. Mettre à jour la synthèse partielle

### Scénario 3 : Re-évaluation d'une catégorie
L'utilisateur souhaite revoir des notes après un échange avec un fournisseur.

1. Récupérer les évaluations existantes depuis le MCP
2. Présenter les scores actuels
3. Procéder aux ajustements demandés
4. Sauvegarder en MCP et mettre à jour la synthèse

### Scénario 4 : Exigences non encore dans rfp-analyzer
La grille existe en local (Excel ou Word) mais n'est pas importée.

1. Proposer de déclencher rfp-import-extractor
2. Attendre l'import complet
3. Vérifier via MCP que les exigences sont bien présentes
4. Lancer Phase 0
