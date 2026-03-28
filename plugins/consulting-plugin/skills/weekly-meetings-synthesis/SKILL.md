---
name: weekly-meetings-synthesis
description: >
  Génère automatiquement une synthèse hebdomadaire structurée des réunions du projet MEN (ministère de l'Éducation nationale / projet PASCAL) à partir de Granola, et produit un document Word professionnel nommé AAMMJJ - Synthese de la semaine.docx.

  Utiliser ce skill dès qu'on demande une synthèse, un récapitulatif, un bilan ou un résumé des réunions de la semaine, qu'il soit question de "meetings de la semaine", "réunions MEN", "synthèse hebdo", "bilan de la semaine", ou "récap des réunions". Déclencher également si l'utilisateur demande "ce qu'il s'est passé cette semaine" ou "un point sur les réunions".
---

# Synthèse hebdomadaire des réunions MEN

Ce skill récupère les réunions de la semaine dans les dossiers Granola liés au projet MEN, extrait les points clés de chaque réunion, et génère un document Word structuré et professionnel.

---

## Vue d'ensemble du workflow

1. Lister les dossiers Granola et identifier ceux dont le nom commence par "MEN"
2. Récupérer les réunions de la semaine en cours dans chacun de ces dossiers
3. Récupérer le contenu détaillé de chaque réunion (par lots de 10 max)
4. Générer le document Word avec le script fourni

---

## Étape 1 — Identifier les dossiers MEN dans Granola

Utiliser l'outil `list_meeting_folders` pour lister tous les dossiers. Retenir tous ceux dont le titre commence par "MEN" (ex : "MEN", "MEN - Gouvernance", "MEN - Smartworkplace").

Si aucun dossier MEN n'apparaît, demander à l'utilisateur de vérifier que ses dossiers Granola sont bien dans l'espace courant (ils peuvent être dans un autre espace Granola).

---

## Étape 2 — Lister les réunions de la semaine

Pour chaque dossier MEN identifié, appeler `list_meetings` avec :
- `time_range: "this_week"`
- `folder_id`: l'ID du dossier

Consolider toutes les réunions dans une liste unique. Si la liste est vide, essayer `last_week` et en informer l'utilisateur.

---

## Étape 3 — Récupérer le contenu détaillé

Appeler `get_meetings` avec les IDs des réunions (10 max par appel). Si plus de 10 réunions, faire plusieurs appels successifs.

Pour chaque réunion, extraire :
- **Titre** et **date**
- **Objectif** : inférer depuis la summary ou les notes si non explicite
- **Éléments clés** : faits importants, décisions, points de vigilance, informations techniques (5-8 points)
- **Actions** : tâches identifiées avec leur responsable (depuis la summary ou les notes privées)

---

## Étape 4 — Générer le document Word

### Nom du fichier
Format : `AAMMJJ - Synthese de la semaine.docx`
Exemple pour le 26 mars 2026 : `260326 - Synthese de la semaine.docx`

### Utiliser docx-js via Node.js

Vérifier que docx est installé :
```bash
npm list --prefix /sessions/friendly-zen-sagan/.npm-global docx 2>/dev/null | grep docx
```

Si non installé :
```bash
npm install docx --prefix /sessions/friendly-zen-sagan/.npm-global
```

Générer un script JavaScript dans `/sessions/friendly-zen-sagan/` et l'exécuter avec `node`. Le module docx se trouve dans `/sessions/friendly-zen-sagan/.npm-global/lib/node_modules/docx`.

### Structure du document

Le document doit contenir pour chaque réunion :

1. **En-tête de section** (fond bleu foncé, texte blanc) : numéro et titre de la réunion
2. **Date** et **Objectif** en texte labelisé
3. **Éléments clés** : section avec titre coloré + liste à tirets
4. **Actions** : tableau à 2 colonnes (Action | Responsable) avec en-tête coloré

Inclure un **pied de page** avec pagination (Page X / Y) et un **en-tête** avec le titre du projet.

### Constantes de couleurs recommandées
```javascript
const BLUE_DARK = "1F3864";   // En-têtes de section
const BLUE_MED  = "2E75B6";   // Titres de sous-sections, tableau actions
const BLUE_LIGHT = "D6E4F0";  // Fond cellules si besoin
const WHITE = "FFFFFF";
```

### Règles critiques docx-js

- **Jamais `\n`** dans les TextRun : utiliser des Paragraph séparés
- **Jamais de bullets unicode** : utiliser `LevelFormat.BULLET` avec `numbering`
- **PageBreak toujours dans un Paragraph**
- **Tables : dual width** — `columnWidths` sur la table ET `width` sur chaque cellule
- **`ShadingType.CLEAR`** (jamais SOLID) pour les fonds colorés
- **`WidthType.DXA`** toujours (jamais PERCENTAGE)

### Où sauvegarder
Sauvegarder le fichier final dans le dossier workspace de l'utilisateur :
```
/sessions/friendly-zen-sagan/mnt/MEN - PASCAL/AAMMJJ - Synthese de la semaine.docx
```

---

## Étape 5 — Présenter le résultat

Fournir un lien `computer://` vers le fichier généré, avec un bref résumé :
- Nombre de réunions couvertes
- Dossiers Granola utilisés
- Nom du fichier généré

---

## Gestion des cas particuliers

**Réunions sans notes substantielles** : inclure quand même la réunion avec les informations disponibles (titre, date, participants si disponibles).

**Réunions hors scope MEN** (ex : réunions commerciales, carrière) : ne pas les inclure, même si elles apparaissent dans la liste temporelle.

**Semaine sans réunions** : informer l'utilisateur et proposer de générer la synthèse de la semaine précédente.

**Plus de 10 réunions** : faire plusieurs appels `get_meetings` successifs par lots de 10.
