---
name: rfp-evaluation
description: Évalue les réponses des fournisseurs à un appel d'offres (RFP/AO), exigence par exigence et catégorie par catégorie, en s'appuyant sur le serveur MCP rfp-analyzer et les documents locaux (PDF, Word, Excel). Produit des scores motivés, des commentaires comparatifs et identifie les points à éclaircir en soutenance. Déclencheurs : "évalue les offres", "lance l'évaluation du RFP", "analyse les réponses fournisseurs", "note les offres", "commence l'évaluation", "démarre l'analyse comparative", "évalue les propositions", "analyse les soumissions fournisseurs".
---

# RFP Evaluation

Évalue de façon systématique et comparative les réponses fournisseurs à un appel d'offres, exigence par exigence, avec notation motivée et checkpoint utilisateur entre chaque catégorie.

## Vue d'ensemble

Ce skill orchestre une évaluation structurée en plusieurs phases :

```
Phase 0 : Prise de connaissance des documents + Executive Summary
      ↓
Phase 1 : Lecture des exigences catégorie par catégorie
      ↓
Phase 2 : Évaluation croisée des réponses de tous les fournisseurs
      ↓
Phase 3 : Deep dive documents si réponse floue ou référence externe
      ↓
Phase 4 : Notation + commentaire comparatif + sauvegarde MCP
      ↓
⏸ Checkpoint utilisateur → validation avant catégorie suivante
      ↓
Phase 5 : Synthèse finale + génération de l'output
```

Le **MCP rfp-analyzer** est le système de référence : il stocke catégories, exigences et réponses fournisseurs. Les documents (CDC, réponses) restent en local et sont lus directement.

---

## Prérequis

Avant de lancer l'évaluation, vérifier avec l'utilisateur :

- [ ] Le serveur MCP `rfp-analyzer` est configuré et accessible
- [ ] Le CDC (cahier des charges) et la grille d'exigences pondérée sont disponibles localement
- [ ] Les réponses fournisseurs sont disponibles (dossier local ou fournis au fil de l'eau)
- [ ] Les fournisseurs à évaluer sont identifiés (noms, nombre)

**Si les exigences ne sont pas encore dans rfp-analyzer :**
Proposer de déclencher le skill **rfp-import-extractor** en premier pour importer catégories et exigences depuis le fichier Excel/Word de la grille. Ne pas commencer l'évaluation sans que les exigences soient dans le MCP.

**Si un dossier de réponses est fourni :**
Demander à l'utilisateur de confirmer la structure : un sous-dossier par fournisseur ? Les noms des fournisseurs correspondent-ils à ceux dans rfp-analyzer ?

---

## Phase 0 : Prise de connaissance & Executive Summary

### Objectif
Maîtriser le CDC et la grille d'exigences avant d'évaluer quoi que ce soit. Produire un Executive Summary qui servira de référentiel tout au long de l'évaluation.

### Étapes

**0.1 — Lire le CDC (cahier des charges)**

Lire l'intégralité du CDC. Identifier et noter :
- Le contexte du projet et les enjeux métier
- Les contraintes techniques et réglementaires majeures
- Les livrables attendus et le calendrier
- Les critères implicites de succès (ce qui est valorisé mais pas forcément exigé)

**0.2 — Lire la grille d'exigences**

Récupérer via le MCP rfp-analyzer la liste des catégories et exigences :
- Utiliser l'outil MCP pour lister les catégories (avec leur hiérarchie)
- Utiliser l'outil MCP pour lister les exigences de chaque catégorie (avec poids et flag `is_mandatory`)

Pour chaque catégorie, identifier :
- Les exigences à fort poids (weight > 0.7) → commentaires approfondis requis
- Les exigences obligatoires (`is_mandatory: true`) → point éliminatoire si score < 3
- La cohérence entre catégories (exigences interdépendantes)

**0.3 — Formaliser l'Executive Summary**

Rédiger un Executive Summary structuré selon le guide `references/executive_summary_guide.md`. Il doit couvrir :
1. Contexte et enjeux du projet (3-5 phrases)
2. Architecture de la grille (nb catégories, nb exigences, répartition des poids)
3. Points clés et structurants : les exigences/catégories qui feront la différence
4. Exigences éliminatoires listées explicitement
5. Zones de vigilance identifiées (ambiguïtés du CDC, exigences difficiles à évaluer)

**0.4 — Validation par l'utilisateur**

Présenter l'Executive Summary et demander :
> "Voici ma prise de connaissance du dossier. Est-ce que cet Executive Summary capture bien les enjeux clés ? Y a-t-il des points que je devrais prioriser ou des biais à corriger avant de commencer l'évaluation ?"

Ne pas passer à la phase suivante sans validation.

---

## Phase 1 à 4 : Boucle d'évaluation par catégorie

Traiter les catégories dans l'ordre (par niveau hiérarchique, en respectant l'ordre défini dans rfp-analyzer).

Pour **chaque catégorie**, exécuter la boucle complète avant de passer à la suivante.

### Étape 1 — Lecture de la catégorie

Annoncer la catégorie à l'utilisateur :
> "Je commence l'évaluation de la catégorie **[Nom catégorie]** ([n] exigences, poids total [x%])."

Pour chaque exigence de la catégorie :
- Lire le titre, la description complète et le poids
- Lire le contexte de la catégorie parente pour comprendre l'intention globale
- Identifier si l'exigence est obligatoire (`is_mandatory`)
- Mémoriser les liens avec d'autres exigences si pertinent

### Étape 2 — Évaluation croisée des réponses fournisseurs

Pour **chaque exigence** de la catégorie, évaluer tous les fournisseurs simultanément :

1. Récupérer via le MCP les réponses de chaque fournisseur pour cette exigence (`response_text`)
2. Si une réponse est absente ou vide dans le MCP → chercher dans les documents locaux du fournisseur
3. Lire toutes les réponses en parallèle pour avoir une vue comparative
4. Évaluer chaque réponse en la confrontant :
   - À l'exigence elle-même (correspond-elle précisément ?)
   - Au CDC (est-ce cohérent avec le contexte ?)
   - Aux autres réponses fournisseurs (est-ce mieux, moins bien, comparable ?)

### Étape 3 — Deep dive documents si nécessaire

Déclencher une analyse approfondie des documents locaux si :
- La réponse fait référence à un document annexe ("cf. notre SLA en annexe", "voir notre référence client X")
- La réponse est trop vague ou générique pour noter objectivement
- Il y a une incohérence entre la réponse et d'autres parties du dossier fournisseur

Dans ce cas :
- Parcourir les documents du fournisseur (PDF, Word, Excel annexes)
- Identifier les passages qui traitent de l'exigence
- Intégrer ces éléments dans l'évaluation (favorablement si pertinent, défavorablement si contradictoire)
- Mentionner explicitement dans le commentaire les sources consultées

### Étape 4 — Notation et sauvegarde MCP

Pour chaque réponse évaluée :

**Attribuer un score** (voir `references/scoring_guide.md` pour le détail) :
- `0` — Aucune réponse fournie
- `1` — Réponse hors sujet
- `2` — Réponse insuffisante ou partielle
- `3` — Réponse satisfaisante sur les attentes principales
- `4` — Bonne réponse, complète et convaincante
- `5` — Au-delà des attentes

**Rédiger le commentaire** (`ai_comment`) selon le niveau de criticité :
- **Exigences obligatoires ou weight > 0.7** → commentaire développé (4-6 phrases) : justification du score, éléments différenciants vs autres fournisseurs, lacunes précises, ce qui aurait mérité un score supérieur
- **Exigences weight 0.4-0.7** → commentaire standard (2-3 phrases) : justification et point principal manquant
- **Exigences weight < 0.4** → commentaire bref (1-2 phrases) : justification concise

**Déterminer le status** :
- Score 0 ou 1 → `fail`
- Score 2 → `partial`
- Score 3, 4 ou 5 → `pass`
- Exigence obligatoire avec score < 3 → `fail` (même si score = 2 donnerait normalement `partial`)

**Identifier les questions de soutenance** (`question`) :
Renseigner le champ `question` si :
- La réponse est incomplète sur un point critique (weight > 0.6 ou is_mandatory)
- Une affirmation forte n'est pas étayée (référence client non vérifiable, engagement sans détail)
- Une divergence existe entre la réponse et les documents annexes
- Il manque une démonstration concrète (POC, cas d'usage, chiffres)

**Sauvegarder dans le MCP** pour chaque réponse évaluée :
```json
{
  "requirement_id_external": "[code exigence]",
  "ai_score": [score],
  "ai_comment": "[commentaire]",
  "status": "[pass|partial|fail]",
  "question": "[question soutenance si applicable]"
}
```

### Checkpoint catégorie

Après évaluation de toutes les exigences de la catégorie, présenter un récapitulatif :

```
📊 Catégorie : [Nom] — Évaluation terminée

| Exigence | Poids | Fournisseur A | Fournisseur B | Fournisseur C |
|----------|-------|---------------|---------------|---------------|
| EX-001   | 0.8   |    4 ✅       |    2 ⚠️       |    3 ✅       |
| EX-002   | 0.6   |    3 ✅       |    4 ✅       |    1 ❌       |
...

Scores pondérés catégorie : A=[x] B=[y] C=[z]
Questions soutenance identifiées : [n]
Points d'alerte : [exigences obligatoires avec fail]
```

Demander :
> "Le récap de cette catégorie vous convient-il ? Souhaitez-vous ajuster des notes ou commentaires avant que je passe à la catégorie suivante ?"

⏸ **Attendre la validation** avant de continuer.

---

## Phase 5 : Synthèse finale & Output

### Synthèse globale

Après l'évaluation de toutes les catégories, produire :

1. **Classement général** des fournisseurs (score total pondéré)
2. **Radar comparatif** par catégorie (en texte/tableau)
3. **Points forts et faiblesses** de chaque fournisseur
4. **Risques identifiés** (exigences obligatoires non satisfaites, zones de flou)
5. **Recommandations** (fournisseur(s) à retenir, points à clarifier absolument)

### Format de l'output

Demander à l'utilisateur le format souhaité :

> "L'évaluation est terminée. Comment souhaitez-vous l'output ?
> - **Option A** — Grille Excel par fournisseur (une feuille par fournisseur + synthèse)
> - **Option B** — Grille Excel consolidée (tous fournisseurs sur une seule feuille, colonnes par fournisseur)
> - **Option C** — Uniquement dans rfp-analyzer (données déjà sauvegardées dans le MCP)
> - **Option D** — Les deux : Excel + MCP"

**Si Excel demandé :**
Utiliser le script `scripts/generate_evaluation_grid.py` en lui fournissant les données exportées depuis le MCP.

Pour l'export depuis le MCP :
- Utiliser l'outil MCP pour exporter toutes les réponses évaluées (avec ai_score, ai_comment, status, question)
- Sauvegarder en JSON local avant de générer l'Excel

**Si rapport de synthèse demandé :**
Rédiger un rapport Markdown structuré avec les sections de synthèse ci-dessus.

---

## Gestion du mode "fil de l'eau"

Quand les documents fournisseurs arrivent progressivement :

1. **Commencer avec les fournisseurs disponibles** — ne pas bloquer sur un fournisseur manquant
2. **Marquer explicitement** dans le MCP les réponses manquantes (status: `pending`, commentaire: "Document non encore reçu")
3. **Reprendre l'évaluation** pour le fournisseur ajouté en indiquant : "J'évalue maintenant [Fournisseur X] qui vient d'être fourni — je reprends exigence par exigence dans l'ordre des catégories"
4. **Mettre à jour la synthèse** après chaque ajout de fournisseur

---

## Interaction avec le MCP rfp-analyzer

### Lecture

- Lister les catégories avec hiérarchie (niveau, parent)
- Lister les exigences par catégorie (avec `weight`, `is_mandatory`, `description`)
- Lister les fournisseurs disponibles dans le projet
- Lire les réponses fournisseurs par exigence (`response_text`)

### Écriture

- Mettre à jour les réponses avec les champs d'évaluation :
  - `ai_score` — score attribué (0 à 5, par pas de 0.5)
  - `ai_comment` — commentaire motivant le score
  - `status` — statut de conformité (pass / partial / fail / pending)
  - `question` — question à poser en soutenance (si applicable)

### En cas d'erreur MCP

Si l'outil MCP ne répond pas ou retourne une erreur :
1. Continuer l'évaluation localement (noter scores et commentaires dans un fichier temporaire)
2. Sauvegarder dans un fichier JSON local au format `responses_evaluation_[date].json`
3. Tenter la sauvegarde MCP ultérieurement ou via rfp-import-extractor

---

## Références

### Documents de référence

- **`references/evaluation_workflow.md`** — Workflow détaillé phase par phase avec exemples
- **`references/scoring_guide.md`** — Grille de notation 0-5 avec exemples et correspondances status
- **`references/executive_summary_guide.md`** — Structure et template de l'Executive Summary

### Scripts

- **`scripts/generate_evaluation_grid.py`** — Génère la grille Excel comparative depuis les données MCP

### Skills connexes

- **`rfp-import-extractor`** — À utiliser en amont pour importer les exigences et réponses dans rfp-analyzer
- **Anthropic Excel skill** — Référencer pour la manipulation avancée de fichiers Excel si nécessaire

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

1. Confirmer avec l'utilisateur : "Je vais évaluer [Fournisseur X] sur toutes les catégories déjà traitées, puis continuer en parallèle sur les suivantes. Confirmez ?"
2. Reprendre depuis la première catégorie pour ce fournisseur
3. Mettre à jour la synthèse partielle

### Scénario 3 : Re-évaluation d'une catégorie
L'utilisateur souhaite revoir des notes après un échange avec un fournisseur.

1. Récupérer les évaluations existantes depuis le MCP
2. Présenter les scores actuels
3. Procéder aux ajustements demandés
4. Sauvegarder en MCP et mettre à jour la synthèse

### Scénario 4 : Exigences non encore dans rfp-analyzer
La grille d'exigences existe en local (Excel ou Word) mais n'est pas importée.

1. Proposer de déclencher rfp-import-extractor
2. Attendre l'import complet
3. Vérifier via MCP que les exigences sont bien présentes
4. Lancer Phase 0
