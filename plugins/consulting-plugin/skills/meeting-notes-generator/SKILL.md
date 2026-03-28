---
name: meeting-notes-generator
description: Generate professional meeting notes and reports from Granola meeting transcripts. Use this skill whenever a user needs to create structured notes from a meeting (formal minutes, email summaries, decision logs, action items lists). Supports multiple output formats including formal meeting notes, executive summaries, email syntheses, and action item tracking. Automatically fetches meeting transcripts via Granola MCP and applies customizable formatting templates.
compatibility: Granola MCP (meeting transcript retrieval)
---

# Meeting Notes Generator

Génère des comptes rendus professionnels à partir des transcripts Granola, avec support de multiples formats de sortie.

## Vue d'ensemble

Ce skill automatise la création de comptes rendus structurés en :
1. **Récupérant le transcript** via l'API Granola (par ID ou recherche par nom)
2. **Analysant le contenu** pour extraire contexte, décisions, actions, participants
3. **Générant la sortie** dans le format choisi (formel, synthèse mail, décisions, etc.)

## Règles impératives

### Aucun emoji dans les outputs
**INTERDIT** : N'utiliser aucun emoji dans les comptes rendus générés, quelle que soit la demande. Les outputs sont des documents professionnels. Cette règle s'applique à tous les formats (formel, synthèse mail, CR tabulaire, etc.).

### Questionnement utilisateur obligatoire si format non précisé
Si l'utilisateur ne précise pas le format souhaité dans sa demande, **poser la question AVANT de générer le compte rendu**. Ne pas choisir un format par défaut silencieusement.

Question type à poser :
```
Quel format souhaitez-vous ?
1. Synthèse mail – résumé concis pour email, ton direct et actionnable
2. Compte rendu formel – document officiel complet, archivable
3. CR tabulaire (style ministère) – document Word structuré en tableaux : constats/points d'attention, arbitrages et décisions, plan d'actions
```

Exception : si le contexte de la demande rend le format évident (ex. "génère-moi une synthèse mail"), passer directement à la génération.

## Flux de travail

### Étape 1 : Identifier la réunion et le format
Demander à l'utilisateur :
- Le **nom exact** de la réunion ou la **date/période**
- Le **format souhaité** pour le compte rendu — **si non précisé, poser la question avec les 3 options ci-dessus**

Utiliser Granola pour chercher et identifier la réunion correcte.

### Étape 2 : Récupérer le transcript
- Utiliser `Granola:get_meeting_transcript` pour obtenir le contenu complet
- Extraire les éléments clés : participants, durée, sujets principaux

### Étape 3 : Générer le compte rendu
- Lire le **format de référence** correspondant depuis `/references/`
- Appliquer les instructions et le template du format choisi
- Générer un fichier structuré prêt à l'emploi

### Étape 3.5 : Vérifier la disponibilité Todoist (optionnel)
Si l'utilisateur veut exporter les actions vers Todoist :
- Vérifier que le MCP Todoist est connecté
- Récupérer la liste des projets actifs dans Todoist
- Cacher en session pour réutilisation
- Proposer les mappages client → projet

### Étape 4 : Parser les actions
- Extraire de la transcription : tous les items de type "À faire", "On doit", "Je vais", etc.
- Identifier le **responsable** (nom ou rôle) et si applicable la **deadline**
- Structurer en tableau : `Action | Responsable | Deadline | Status`

### Étape 5 : Identifier tes actions
- Chercher dans la liste : ton nom, tes rôles, ou patterns comme "tu dois", "c'est à toi"
- Mettre en évidence les actions qui te concernent directement
- Afficher un **tableau récapitulatif** dans le chat avec filtrage

### Étape 6 : Proposer l'intégration Todoist
- Pour chaque action qui te concerne, proposer un bouton "Ajouter à Todoist"
- Envoyer via `Todoist:add_task` (ou équivalent MCP) avec :
  - Titre = libellé de l'action
  - Description = contexte (réunion, deadline, responsable si autre)
  - Due date = si deadline identifiée
  - Projet = suggestion basée sur le contexte (client, projet)

### Étape 7 : Livrer le résultat
- Exporter le compte rendu en format demandé (Markdown, Word, ou directement dans le chat)
- Proposer des ajustements ou variantes si nécessaire

## Formats disponibles

> **Comment ajouter un format** : Créer un fichier `format-nom.md` dans `/references/` avec instructions et template. Chaque format décrit :
> - Les sections à inclure
> - Le tone et le style
> - Les champs obligatoires/optionnels
> - Un exemple structuré

Voir les détails dans le répertoire `/references/` :

- **`format-formel.md`** – Compte rendu officiel complet, apte à la signature et archivage
- **`format-synthese-mail.md`** – Synthèse concise pour email, ton direct et actionnable
- **`format-cr-pascal.md`** – CR tabulaire style ministère, génère un fichier Word avec en-tête officiel, tableau participants, constats/points d'attention, plan d'action, arbitrages et décisions, plan d'actions et prochaines échéances
- **`format-decisions.md`** *(à ajouter)* – Focus sur les décisions prises et leurs propriétaires
- **`format-actions.md`** *(à ajouter)* – Liste d'actions structurée avec responsables et deadlines

## Extraction et gestion des actions

### Parser les actions du transcript

L'algorithme doit identifier les patterns d'action :

```
Patterns à chercher :
- "On doit [action]"
- "[Nom] doit [action]"
- "Je vais [action]"
- "Tu dois [action]"
- "À faire : [action]"
- "Action : [action]"
- Tone impératif suivi d'une deadline ou d'un nom
```

**Output du parsing :**
```
{
  "actions": [
    {
      "id": 1,
      "description": "Libellé clair de l'action",
      "owner": "Prénom Nom ou rôle",
      "deadline": "DD/MM/YYYY ou null",
      "context": "Sujet/point de réunion d'où vient l'action",
      "relevantToUser": true/false,
      "confidence": 0.95
    },
    ...
  ]
}
```

### Identifier tes actions

Chercher dans la liste les actions qui te concernent directement :

1. **Match par nom** : "Seb", "Sébastien", ton titre/rôle
2. **Match par pronom** : "tu dois", "c'est à toi"
3. **Contexte implicite** : Si un sujet est clairement ton domaine (Smart Building, RFP, dev), marquer comme relevant
4. **Manuellement** : Afficher un checkbox "C'est pour moi ?" pour chaque action

**Flag :** `relevantToUser: true` pour affichage prioritaire

### Afficher le tableau des actions

Dans le chat, présenter un tableau interactif :

```
| # | Action | Responsable | Deadline | Pour moi ? | Ajouter à Todoist |
|---|--------|-------------|----------|-----------|------------------|
| 1 | Analyser les réponses RFP IZIX | Seb | 31/03 | ✅ | [Ajouter] |
| 2 | Valider budget avec finance | Alice | 28/03 | ❌ | - |
| 3 | Préparer doc de synthèse | Seb | 02/04 | ✅ | [Ajouter] |
```

**Interactions possibles :**
- Cliquer "Ajouter à Todoist" → envoyer vers Todoist avec contexte
- Checkbox "Pour moi ?" → re-filtrer le tableau
- Bouton "Tous à Todoist" → batch add

### Intégration Todoist

Pour chaque action envoyée à Todoist :

**Données mappées :**
```javascript
{
  content: "[Seb] Analyser réponses RFP IZIX",  // Prepend nom si différent de toi
  description: "Source: Réunion [Titre] du [date]\nContexte: [Sujet]\nOrigine: [Responsable initial]",
  due_date: "2024-03-31",  // Format ISO
  priority: 3,  // 1=high, 2=medium, 3=normal, 4=low → inférer du deadline
  labels: ["meeting-notes", "ENGIE", "RFP"],  // Tags basés sur contexte/réunion
  project_id: "???"  // À configurer par l'utilisateur (optionnel)
}
```

**Configuration Todoist :**
- Demander à l'utilisateur quel **projet Todoist** utiliser (par défaut : "Inbox" ou un projet "Meeting Actions")
- Propose d'ajouter des **labels** automatiquement basés sur le client/projet de la réunion

### Workflow complet

```
User dit: "Génère un CR de la réunion ENGIE du 25/03"
  ↓
1. Récupère transcript Granola
2. Génère compte rendu (format choisi)
3. Parse actions → 5 actions trouvées
4. Identifie 3 actions pour Seb
5. Affiche tableau dans le chat
6. User clique "[Ajouter]" sur action #1
7. Send vers Todoist via MCP
8. Confirmation + suggestion des 2 autres actions
```

Conseils d'implémentation

- **Qualité du transcript** : Si le transcript est fragmenté ou incomplet, alerter et proposer un compte rendu partiel
- **Participants** : Granola les extraira automatiquement ; utiliser leurs vrais noms si présents
- **Actions** : Repérer les "to-do", "on doit", "je vais" et les isoler clairement
- **Décisions** : Identifier les consensus, les choix explicites, les directives
- **Tone** : Adapter au format (formel = neutre et complet ; mail = direct et scannable)
- **Confidence** : Si une action est ambiguë, noter la confiance et demander confirmation à l'user

## Configuration de Granola et Todoist

### Granola
Ce skill utilise les outils Granola suivants :
- `Granola:list_meetings` – Lister les réunions d'une période
- `Granola:get_meetings` – Récupérer détails (titre, participants, durée)
- `Granola:get_meeting_transcript` – Obtenir le contenu complet avec timestamps

Si l'utilisateur n'a pas de MCP Granola activé, expliquer comment le configurer ou proposer une solution manuelle (coller le transcript).

### Todoist
Pour l'intégration Todoist :
- `Todoist:add_task` – Créer une tâche avec titre, deadline, labels, projet
- Configuration optionnelle : projet par défaut, mapping client → projet

Voir `/references/action-extraction.md` pour détails complets sur le parsing, la détection de pertinence, et le payload Todoist.

## Fichiers de référence

- **`/references/format-formel.md`** – Template compte rendu officiel
- **`/references/format-synthese-mail.md`** – Template synthèse pour email
- **`/references/format-cr-pascal.md`** – Template CR tabulaire style ministère (génère un .docx)
- **`/references/action-extraction.md`** – Logique extraction actions, scoring confiance, intégration Todoist
- **`/references/todoist-setup.md`** – Vérification MCP Todoist, mappages client → projet, configuration
