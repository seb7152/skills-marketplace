# Format CR Tabulaire (Style Ministère / Projet PASCAL)

## Usage
Compte rendu structuré en tableaux pour les réunions de projet de type institutionnel/ministériel. Génère un fichier **Word (.docx)** avec mise en forme fidèle au standard visuel SIA Partners / Éducation nationale. Contenu dense, tabulaire, sans prose superflue.

Ce format est déclenché par : "CR tabulaire", "style ministère", "comme le PDF", "format PASCAL", ou toute demande de compte rendu formel avec sortie Word.

## Génération du fichier Word

**OBLIGATOIRE** : Ce format produit toujours un fichier `.docx`. Utiliser le skill `docx` (via `npm install -g docx` et JavaScript) pour générer le fichier. Ne jamais livrer uniquement du texte brut pour ce format.

Lire le SKILL.md du skill `docx` avant de générer le fichier.

Le fichier doit être sauvegardé dans `/sessions/.../mnt/outputs/CR_[Titre]_[DDMMYYYY].docx`.

## Structure du document Word

### Page de garde / En-tête (Page 1)

**Logo** (optionnel) : Si le contexte est ministériel, le logo peut être omis ou remplacé par un texte "Ministères Éducation Nationale / Enseignement Supérieur / Recherche" en petit dans le coin supérieur gauche.

**Tableau d'identification** (4 lignes, 2 colonnes) :
- Fond des cellules gauche : bleu foncé (`1F3864` ou `2E4057`) — texte blanc, gras
- Fond des cellules droite : blanc — texte noir

```
| Version :   | [DD/MM/YYYY]                                                               |
| Objet :     | [Titre complet de la réunion / du rapport]                                 |
| Rédacteur : | [Entité rédactrice, ex. DNE - DAC]                                        |
| Diffusion : | À l'ensemble des participants à la réunion du [DD/MM/YYYY] et aux parties prenantes concernées |
```

**Tableau des participants** (3 colonnes) :
- En-tête : fond bleu foncé, texte blanc, centré, gras
- Lignes groupe (ex. "DP/SAAM", "DNE") : fond bleu moyen (`4472C4` ou `3D5A80`), texte blanc, gras, fusionné sur les 3 colonnes
- Lignes participants : fond blanc, texte noir
- Colonne "Présence" : mettre "X" si présent, laisser vide si absent

Colonnes :
```
| Participants        | Contact (mail)                    | Présence |
|--------------------|-----------------------------------|----------|
| [Groupe 1]         | (cellule fusionnée)               | (fusion) |
| Prénom NOM         | prenom.nom@domaine.fr             | X        |
| ...                | ...                               |          |
| [Groupe 2]         | (cellule fusionnée)               | (fusion) |
| Prénom NOM         | prenom.nom@domaine.fr             | X        |
```

---

### Section 1 — Constats et points d'attention

**Titre de section** : "1. Constats et points d'attention" — style Heading (numéroté, en retrait)

**Tableau** (3 colonnes) :
- En-tête : fond bleu foncé, texte blanc, centré, gras : `Constat` | `Ce qui est établi` | `Réponse / plan d'action associé`
- Lignes : fond blanc (alternance légère gris clair optionnelle), texte noir
- Contenu dense : plusieurs paragraphes possibles dans une cellule

Extraction depuis le transcript :
- **Constat** : situation observée, problème identifié, enjeu soulevé (libellé court, ~1 ligne)
- **Ce qui est établi** : faits, état d'avancement, contexte factuel (~2-5 lignes)
- **Réponse / plan d'action** : décision ou action associée, responsabilités évoquées (~2-5 lignes, peut inclure des sous-bullets avec `-`)

---

### Section 2 — Plan d'action détaillé (si applicable)

Inclure cette section si la réunion a produit un plan d'action structuré en phases.

**Titre** : "[Intitulé du plan d'action]" — en gras, sans tableau encadrant le titre

**Tableau** (3 colonnes) :
- En-tête : fond bleu foncé, texte blanc, gras : `Action` | `Responsable(s)` | `Livrable / résultat`
- Lignes de phase : fond bleu moyen, texte blanc, gras, fusionné sur 3 colonnes — ex. "Phase 1 – Définition du cadre (19/02 → 23/02/2026) :"
- Lignes d'action : fond blanc, texte noir

Extraction depuis le transcript :
- **Action** : libellé précis de la tâche (~1-3 lignes)
- **Responsable(s)** : nom(s) complet(s), séparés par " + "
- **Livrable / résultat** : output attendu (document, validation, liste...)

---

### Section 3 — Arbitrages et décisions actées

**Titre de section** : "2. Arbitrages et décisions actées" (numéroté selon position dans le document)

**Tableau** (3 colonnes) :
- En-tête : fond bleu foncé, texte blanc, gras : `Sujet` | `Décision` | `Impacts / points de vigilance`
- Lignes : fond blanc, texte noir

Extraction depuis le transcript :
- **Sujet** : thème ou point arbitré (court, ~1 ligne)
- **Décision** : ce qui a été acté en séance (~2-5 lignes)
- **Impacts / points de vigilance** : conséquences, risques, dépendances (~2-5 lignes)

---

### Section 4 — Plan d'actions et prochaines échéances

**Titre de section** : "3. Plan d'actions et prochaines échéances" (numéroté)

**Tableau** (3 colonnes) :
- En-tête : fond bleu foncé, texte blanc, gras : `Échéance` | `Action` | `Responsable`
- Lignes : fond blanc, texte noir
- Tri chronologique par date d'échéance
- Dates en format DD/MM/YYYY ou "À planifier" si non déterminée

Extraction depuis le transcript :
- **Échéance** : date précise ou "À planifier"
- **Action** : libellé clair de la prochaine étape (~1-4 lignes)
- **Responsable** : nom(s) ou entité(s), avec sous-liste si plusieurs personnes

---

## Palette de couleurs (cohérence visuelle)

| Usage                        | Couleur hex | Description              |
|-----------------------------|-------------|--------------------------|
| En-tête tableaux / étiquettes | `1F3864`   | Bleu très foncé (marine) |
| Lignes de groupe / phases   | `4472C4`    | Bleu moyen               |
| Fond cellule label (tableau ID) | `2E4057` | Bleu foncé alternatif    |
| Texte sur fond coloré       | `FFFFFF`    | Blanc                    |
| Texte standard              | `000000`    | Noir                     |
| Fond lignes standard        | `FFFFFF`    | Blanc                    |

Utiliser `ShadingType.CLEAR` (jamais `SOLID`) dans docx-js pour les fonds colorés.

---

## Mise en page Word

- **Format papier** : A4 (11906 x 16838 DXA)
- **Marges** : 1 cm haut/bas, 2 cm gauche/droite (~568 DXA haut/bas, ~1134 DXA gauche/droite)
- **Largeur utile** : ~9638 DXA (avec marges 2cm/2cm)
- **Police** : Arial, 10pt (taille 20 en half-points dans docx-js)
- **Interligne** : simple (240 half-points)
- **Numérotation des sections** : style "1.", "2.", "3." avec indentation légère
- **Tableaux** : pleine largeur (`width: 9638, type: WidthType.DXA`)

### Proportions des colonnes par tableau

**Tableau identification** (2 col) : `[2200, 7438]`

**Tableau participants** (3 col) : `[3200, 4638, 1800]`

**Tableau constats** (3 col) : `[1800, 3819, 4019]`

**Tableau plan d'action** (3 col) : `[3819, 2819, 3000]`

**Tableau arbitrages** (3 col) : `[1800, 3819, 4019]`

**Tableau actions/échéances** (3 col) : `[1800, 4638, 3200]`

---

## Directives de rédaction

- **Aucun emoji** : Interdit dans tout le document
- **Ton** : Factuel, institutionnel, neutre
- **Cellules** : Toujours ajouter des marges internes (`top: 80, bottom: 80, left: 120, right: 120`)
- **Sous-listes dans cellule** : Utiliser des tirets simples (`-`) précédés d'un retour à la ligne (`new Paragraph`)
- **Fusion de lignes groupe** : Utiliser `columnSpan: 3` pour les lignes de groupe/phase
- **Gras** : En-têtes de tableau, étiquettes du tableau d'identification, lignes de phase
- **Sections vides** : Omettre les sections pour lesquelles il n'y a pas de contenu dans le transcript (ex. pas de plan d'action en phases = pas de section 2)

## Points de contrôle

- Tableau d'identification complet (version, objet, rédacteur, diffusion)
- Tableau participants avec groupes et emails
- Chaque constat a une réponse associée
- Actions assignées avec responsable et date
- Décisions clairement distinguées des actions
- Aucun emoji dans le document
- Fichier .docx bien formé et validé
