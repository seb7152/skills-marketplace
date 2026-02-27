# Guide de notation — RFP Evaluation

Ce document définit la grille de notation utilisée pour évaluer les réponses fournisseurs, avec les correspondances de status, les règles de commentaires et des exemples concrets.

---

## Grille de notation 0 à 5

| Score | Label | Signification | Status MCP |
|-------|-------|---------------|------------|
| **0** | Aucune réponse | Pas de réponse fournie pour cette exigence | `fail` |
| **1** | Hors sujet | Réponse fournie mais ne traite pas de l'exigence | `fail` |
| **2** | Insuffisante | Réponse partielle ou trop vague pour convaincre | `partial` |
| **3** | Satisfaisante | Répond aux attentes principales de l'exigence | `pass` |
| **4** | Bonne | Réponse complète, bien détaillée et convaincante | `pass` |
| **5** | Excellente | Au-delà des attentes, apporte de la valeur ajoutée | `pass` |

Les scores intermédiaires en 0.5 sont autorisés (ex: 2.5, 3.5) quand une réponse se situe précisément entre deux niveaux.

---

## Règles spéciales pour les exigences obligatoires (`is_mandatory: true`)

- Un score < 3 sur une exigence obligatoire entraîne toujours le status `fail`, même si le score serait normalement `partial` (score 2)
- Le commentaire doit **toujours** mentionner explicitement le caractère éliminatoire de la lacune
- Une question de soutenance (`question`) est **obligatoire** si score ≤ 2 sur une exigence obligatoire

---

## Détail des niveaux

### Score 0 — Aucune réponse
**Critères :** Le champ réponse est vide, absent, ou contient uniquement "N/A", "voir document X" sans contenu réel.

**Comment le détecter :**
- `response_text` vide ou null dans le MCP
- Réponse type "Cf. notre offre commerciale" sans autre contenu
- Tableau Excel avec cellule vide pour cette exigence

**Status :** `fail`

**Exemple de commentaire :**
> "Aucune réponse fournie pour cette exigence. Le fournisseur n'a pas traité ce point dans son offre."

---

### Score 1 — Réponse hors sujet
**Critères :** Une réponse est fournie mais elle ne répond pas à ce qui est demandé. Peut être une réponse copiée-collée d'une autre exigence, une présentation générique de la société, ou un texte qui n'aborde pas le sujet.

**Comment le détecter :**
- La réponse ne contient aucun mot-clé lié à l'exigence
- Le fournisseur répond sur un aspect différent de l'exigence
- Réponse générique applicable à n'importe quelle exigence

**Status :** `fail`

**Exemple de commentaire :**
> "La réponse fournie présente la philosophie générale du fournisseur en matière de sécurité mais ne traite pas spécifiquement de la gestion des habilitations demandée. Aucun élément concret sur les mécanismes d'autorisation n'est mentionné."

---

### Score 2 — Réponse insuffisante / partielle
**Critères :** L'exigence est bien identifiée et partiellement traitée, mais la réponse manque de profondeur, de détails techniques, de preuves ou de précisions sur des points importants. On comprend que le fournisseur peut adresser le sujet, mais on n'a pas de certitude.

**Cas typiques :**
- Réponse affirmative sans explication ("Oui, nous supportons cette fonctionnalité")
- Éléments partiellement traités avec des lacunes sur des sous-points critiques
- Réponse correcte sur le principe mais sans détail d'implémentation
- Engagement sur un livrable sans calendrier ni méthodologie

**Status :** `partial`

**Exemple de commentaire :**
> "Le fournisseur confirme disposer d'une solution de monitoring en temps réel mais ne détaille pas les métriques surveillées, les seuils d'alerte ni la procédure d'escalade. La réponse reste au niveau des principes sans apporter de preuve concrète de mise en œuvre. Les fournisseurs B et C ont fourni des captures d'écran de leurs tableaux de bord."

---

### Score 3 — Réponse satisfaisante
**Critères :** L'exigence est correctement adressée dans ses attentes principales. La réponse est cohérente, compréhensible et démontre une bonne compréhension du besoin. Des lacunes mineures peuvent exister mais elles ne remettent pas en cause la capacité du fournisseur.

**Cas typiques :**
- Réponse structurée qui couvre les points principaux
- Quelques éléments manquants mais non bloquants
- Bonne description du "quoi" avec un "comment" perfectible

**Status :** `pass`

**Exemple de commentaire :**
> "Réponse satisfaisante qui couvre les principaux aspects de la gestion des incidents : processus de détection, qualification et escalade sont décrits. On note l'absence de SLA précis pour les incidents critiques, ce qui aurait constitué un plus. Les fournisseurs A et C offrent une réponse comparable sur ce point."

---

### Score 4 — Bonne réponse
**Critères :** Réponse complète, bien structurée, convaincante. Tous les aspects de l'exigence sont couverts avec un niveau de détail satisfaisant. Le fournisseur démontre une vraie maîtrise du sujet.

**Cas typiques :**
- Réponse structurée avec exemples ou références
- SLA, métriques, processus décrits avec précision
- Cohérence avec les autres parties de l'offre
- Éventuellement : références client ou preuves d'implémentation

**Status :** `pass`

**Exemple de commentaire :**
> "Excellente réponse qui détaille précisément le processus de reprise après incident : RTO de 4h et RPO de 1h sont garantis contractuellement, la procédure de bascule est documentée et deux références clients en production sont citées. Légèrement en retrait vs Fournisseur A qui propose un RTO de 2h, mais l'approche est mature et bien documentée."

---

### Score 5 — Au-delà des attentes
**Critères :** La réponse dépasse ce qui était demandé de manière qualitative. Le fournisseur apporte une approche innovante, des garanties supplémentaires, des fonctionnalités non demandées mais pertinentes, ou démontre une expertise distinctive.

**Cas typiques :**
- Proposition d'une solution plus performante que le minimum requis
- Valeur ajoutée non sollicitée mais clairement pertinente
- Démonstration d'une expertise rare ou différenciante
- Engagement contractuel au-delà du standard du marché

**Status :** `pass`

**Exemple de commentaire :**
> "Réponse exemplaire : le fournisseur non seulement répond à l'exigence de chiffrement AES-256 mais propose en plus une architecture zero-trust avec rotation automatique des clés toutes les 24h et audit trail certifié ISO 27001. Cette approche va significativement au-delà des attentes et constitue un avantage différenciant réel par rapport aux autres soumissionnaires."

---

## Profondeur des commentaires selon la criticité

| Critère | Longueur recommandée | Contenu attendu |
|---------|----------------------|-----------------|
| `is_mandatory: true` | 4-6 phrases | Justification score, comparaison fournisseurs, lacunes précises, impact sur la conformité |
| `weight > 0.7` | 4-6 phrases | Justification score, points différenciants, ce qui aurait justifié un score supérieur |
| `weight 0.4-0.7` | 2-3 phrases | Justification score, point principal manquant ou point fort |
| `weight < 0.4` | 1-2 phrases | Justification concise |

**Règles transversales pour tous les commentaires :**

1. **Comparer** — Mentionner comment les autres fournisseurs ont traité le même point (sans forcément citer leur note)
2. **Préciser** — Dire ce qui manque exactement, pas juste "réponse incomplète"
3. **Contextualiser** — Relier à l'exigence et au CDC si pertinent
4. **Éviter** les termes vagues : "bonne réponse", "acceptable", "insuffisant" sans explication

---

## Questions de soutenance (`question`)

Renseigner le champ `question` dans les cas suivants :

| Situation | Exemple de question |
|-----------|---------------------|
| Affirmation forte non étayée | "Pouvez-vous fournir un exemple de mise en œuvre de ce mécanisme chez un client existant ?" |
| Chiffre ou engagement non contractualisé | "Ce SLA de 99,9% est-il garanti contractuellement ? Dans quelles conditions peut-il être revu ?" |
| Référence à un document non fourni | "Vous mentionnez votre 'guide de sécurité interne' — pouvez-vous nous le communiquer ?" |
| Lacune sur un point critique | "Comment gérez-vous la continuité de service en cas de défaillance de votre datacenter principal ?" |
| Incohérence entre réponse et annexe | "Votre réponse indique une capacité de 1000 utilisateurs simultanés, mais votre fiche technique mentionne 500. Quel est le chiffre garanti ?" |
| Démonstration attendue | "Pouvez-vous prévoir une démonstration de ce module lors de la soutenance ?" |

---

## Tableau de correspondance score → status

```
Score 0.0              → fail
Score 0.5              → fail
Score 1.0              → fail
Score 1.5              → fail
Score 2.0              → partial  (fail si is_mandatory)
Score 2.5              → partial  (fail si is_mandatory)
Score 3.0              → pass
Score 3.5              → pass
Score 4.0              → pass
Score 4.5              → pass
Score 5.0              → pass
```

---

## Exemple d'évaluation complète

**Exigence :** EX-042 — Gestion des habilitations par rôles (RBAC)
**Poids :** 0.85 | **Obligatoire :** oui | **Catégorie :** Sécurité > Contrôle d'accès

**Fournisseur A**
- Response_text : "Notre solution intègre un système RBAC natif avec gestion hiérarchique des rôles, délégation d'administration et audit trail complet. Nous gérons actuellement plus de 200 clients avec ce module, dont 3 dans le secteur public (références disponibles sur demande). Nos rôles sont configurables sans développement via l'interface d'administration. Conformité NF Z42-020 et ISO 27001."
- Score : 4.5
- Status : pass
- Comment : "Réponse très complète qui couvre tous les aspects de l'exigence RBAC : gestion hiérarchique, délégation, audit trail et conformité réglementaire. Les références secteur public sont un plus. Légèrement en deçà du score maximum car les mécanismes de révision périodique des habilitations ne sont pas décrits. Meilleure réponse de l'appel d'offres sur ce point."

**Fournisseur B**
- Response_text : "Oui, nous gérons les droits utilisateurs par profils configurables."
- Score : 2
- Status : fail (obligatoire)
- Comment : "Réponse extrêmement succincte qui confirme l'existence d'une gestion par profils sans aucun détail sur l'implémentation RBAC, la granularité des rôles, la délégation ou l'audit trail. Cette exigence est obligatoire et la réponse ne permet pas d'évaluer la capacité réelle du fournisseur. Écart très significatif avec les Fournisseurs A et C."
- Question : "Pouvez-vous détailler votre architecture RBAC : gestion hiérarchique des rôles, délégation d'administration, mécanisme d'audit ? Une démonstration lors de la soutenance serait fortement appréciée."
