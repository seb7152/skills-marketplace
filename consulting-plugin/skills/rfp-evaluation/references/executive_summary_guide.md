# Guide de l'Executive Summary — RFP Evaluation

L'Executive Summary (ES) est produit en Phase 0 avant tout évaluation. Il sert de référentiel tout au long de l'analyse : il aide à maintenir la cohérence des évaluations, à calibrer les niveaux d'exigence et à ne pas perdre de vue l'essentiel.

---

## Objectif de l'Executive Summary

L'ES remplit trois fonctions :
1. **Démontrer la compréhension** du CDC et des enjeux métier avant d'évaluer
2. **Servir de boussole** pendant l'évaluation (rappeler les attentes implicites, les contraintes)
3. **Constituer une référence partagée** avec l'utilisateur pour valider la lecture du dossier

---

## Structure de l'Executive Summary

### Section 1 — Contexte et enjeux du projet

**Ce qu'il faut couvrir :**
- Nature du projet (système, service, intégration...)
- Contexte organisationnel et métier (qui commandite, pour quels utilisateurs, dans quel secteur)
- Enjeux principaux (efficacité opérationnelle, conformité, sécurité, transformation digitale...)
- Contraintes majeures identifiées (calendrier, budget si mentionné, contraintes techniques existantes)
- Critères implicites de succès (ce qui transparaît du CDC sans être explicitement exigé)

**Longueur recommandée :** 5-8 phrases.

**Exemple :**
> "Le projet vise à remplacer le système de gestion documentaire actuel (legacy, fin de vie 2025) par une solution SaaS capable de gérer 50 000 documents actifs et 800 utilisateurs simultanés, dans un contexte de passage au full remote. L'enjeu principal est la continuité de service pendant la migration (contrainte forte : aucune interruption > 4h tolérée) et la conformité RGPD pour un volume significatif de données personnelles. Le CDC signale une forte sensibilité sur la performance (temps de chargement < 2s) et la facilité de prise en main pour des utilisateurs peu technophiles. L'intégration avec l'AD existant (Azure AD) est une contrainte non négociable."

---

### Section 2 — Architecture de la grille d'exigences

**Ce qu'il faut couvrir :**
- Nombre de catégories et leur structure hiérarchique
- Nombre total d'exigences
- Répartition des poids par catégorie (quelle catégorie pèse le plus ?)
- Nombre d'exigences obligatoires et leur répartition

**Format recommandé : tableau**

```
| Catégorie          | Exigences | Poids moyen | Obligatoires |
|--------------------|-----------|-------------|--------------|
| Fonctionnel        |    28      |    0.65     |      8       |
| Technique          |    15      |    0.72     |      5       |
| Sécurité           |    12      |    0.85     |     12       |
| Intégration        |     8      |    0.70     |      3       |
| Support & SLA      |     6      |    0.60     |      2       |
| **Total**          |  **69**   |    **0.70** |    **30**    |
```

---

### Section 3 — Points clés et structurants

**Ce qu'il faut couvrir :**
Identifier les 5 à 10 exigences ou thèmes qui feront réellement la différence entre les offres. Ces points sont ceux sur lesquels une note élevée ou basse aura un impact significatif sur le classement final.

**Critères pour identifier un point structurant :**
- Poids élevé (> 0.75) ET complexité technique importante
- Thème transverse qui impacte plusieurs catégories
- Point sur lequel les fournisseurs ont des approches très différentes (enjeux de différenciation)
- Exigence dont la réponse nécessitera une analyse approfondie (deep dive attendu)

**Format recommandé :**

Pour chaque point structurant :
- Code + titre de l'exigence (ou thème transverse)
- Pourquoi c'est structurant
- Ce qu'on cherche vraiment dans la réponse

**Exemple :**
> **EX-023 — Architecture multi-tenant (poids 0.9, obligatoire)**
> Point structurant car il conditionne l'ensemble de la politique de sécurité et de données. Une réponse convaincante doit démontrer l'isolation réelle des données (pas juste une isolation logique), idéalement avec une certification tierce. Les fournisseurs avec une architecture native multi-tenant auront un avantage significatif.

---

### Section 4 — Exigences éliminatoires

**Lister explicitement** toutes les exigences `is_mandatory: true`, avec pour chacune :
- Code + titre
- Pourquoi c'est éliminatoire (contexte CDC si disponible)
- Ce qu'on considère comme une réponse minimalement acceptable (score 3)

Ces exigences feront l'objet d'une attention particulière pendant l'évaluation. Un fournisseur avec `fail` sur l'une d'elles doit être signalé clairement dans la synthèse.

**Format recommandé :**

```
Exigences éliminatoires (30 identifiées) :

🔴 EX-001 — Certification ISO 27001 : Obligatoire pour conformité client. Minimum acceptable : présenter le certificat valide.
🔴 EX-015 — Hébergement données en UE : Contrainte RGPD non négociable. Minimum acceptable : contrat garantissant l'hébergement exclusif UE.
🔴 EX-031 — SLA disponibilité 99.5% : Niveau de service minimum pour usage 24/7. Minimum acceptable : SLA contractuel avec pénalités.
...
```

---

### Section 5 — Zones de vigilance

Identifier les points qui rendront l'évaluation difficile ou risquée :

**Types de zones de vigilance :**
- **Ambiguïtés du CDC** : exigences formulées de façon vague ou contradictoire
- **Exigences difficiles à évaluer** : points qui ne peuvent être vraiment validés qu'en soutenance ou POC
- **Risques de réponses génériques** : exigences auxquelles tous les fournisseurs vont répondre "oui" sans différenciation
- **Points potentiellement mal compris** : exigences techniques pointues pour lesquelles une mauvaise compréhension donnera des réponses hors sujet
- **Dépendances entre exigences** : si EX-045 est mal répondu, EX-046 et 047 seront probablement aussi insuffisants

**Format recommandé :**

> ⚠️ **Exigences d'intégration EX-051 à EX-058** — Ces exigences supposent une connaissance du SI existant que les fournisseurs n'ont probablement pas. Risque élevé de réponses génériques. Privilégier les fournisseurs qui posent des questions en retour ou qui proposent un atelier de cadrage.

> ⚠️ **EX-020 — Performance sous charge** — Sans spécification précise du profil de charge (nb users concurrents, taille des fichiers), les réponses seront difficilement comparables. Poser une question soutenance systématique sur les hypothèses retenues.

---

## Template complet

```markdown
# Executive Summary — Évaluation [Nom du projet] — [Date]

## 1. Contexte et enjeux
[5-8 phrases : nature, contexte, enjeux, contraintes, critères implicites]

## 2. Architecture de la grille
[Tableau catégories × exigences × poids × obligatoires]

Total : [n] exigences | [n] obligatoires | [n] catégories

## 3. Points clés et structurants

### [Code] — [Titre exigence]
**Poids :** [x] | **Obligatoire :** [oui/non]
[Pourquoi c'est structurant + ce qu'on cherche dans la réponse]

[Répéter pour 5-10 points]

## 4. Exigences éliminatoires
🔴 [Code] — [Titre] : [Contexte + minimum acceptable]
[Répéter pour chaque exigence obligatoire]

## 5. Zones de vigilance
⚠️ [Description de la zone + recommandation d'évaluation]
[Répéter si nécessaire]
```

---

## Bonnes pratiques

1. **Rédiger l'ES avant d'ouvrir les offres fournisseurs** — pour ne pas biaiser la lecture du CDC
2. **Être synthétique** — l'ES n'est pas un résumé exhaustif du CDC, c'est un filtre des points critiques
3. **Formuler les attentes concrètement** — "réponse qui inclut un SLA contractualisé" plutôt que "bonne réponse sur le SLA"
4. **Faire valider par l'utilisateur** — l'ES reflète LEUR lecture, pas seulement la nôtre
5. **Conserver l'ES** comme référence jusqu'à la fin — relire avant chaque catégorie si nécessaire
