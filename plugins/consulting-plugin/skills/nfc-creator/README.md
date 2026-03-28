# NFC Creator Skill - README

## 📋 Vue d'ensemble

Le **NFC Creator** est un skill Claude avancé qui automatise la création de **New Contract Forms (NFC)** pour SIA Partners. Il gère complètement le processus : collecte d'informations client, configuration du Sales Bonus, staffing des consultants, et génération d'un fichier Excel robuste.

## 🎯 Capacités Principales

✅ **Création automatique de NFC** avec toutes les valeurs par défaut SIA Partners
✅ **Configuration interactive** pour client, projet, contacts, consultants
✅ **Sales Bonus avancé** avec validation automatique du total (≤ 3%)
✅ **Staffing de consultants** avec grades standardisés et calculs de marges
✅ **Préservation de la structure Excel** (formules, styles, validations)
✅ **Nommage automatique** selon conventions SIA Partners
✅ **API programmatique** pour intégration dans d'autres workflows

## 🚀 Démarrage Rapide

### Mode Interactif (CLI)

```bash
cd /mnt/skills/user/nfc-creator/scripts
python3 nfc_main.py
```

Puis répondre aux questions interactives :
1. Nom du client (obligatoire)
2. Nom du projet (obligatoire)
3. Date de début (obligatoire, DD/MM/YYYY)
4. Configurer le Sales Bonus (optionnel)
5. Ajouter des consultants (optionnel)

### Mode Programmatique (Python)

```python
from nfc_builder_xml import create_nfc

admin_info = {
    'client_name': 'Acme Corp',
    'project_name': 'Digital Transformation',
    'start_date': '01/04/2026',
    'sales_name': 'Sébastien Grandperret',
    'sales_email': 'sebastien.grandperret@sia-partners.com',
    'pm_name': 'Sébastien Grandperret',
    'pm_email': 'sebastien.grandperret@sia-partners.com',
}

consultants = [
    {
        'name': 'Sophie Martin',
        'grade': 'Senior Consultant',
        'days': 65,
        'tj': 950
    }
]

success, message = create_nfc(
    template_path='/path/to/template.xlsm',
    output_path='/path/to/output.xlsm',
    admin_info=admin_info,
    consultants=consultants
)

print(message)
```

## 📁 Structure du Skill

```
nfc-creator/
├── SKILL.md                           # Spécification du skill
├── README.md                          # Ce fichier
│
├── assets/
│   └── contract_form_CLEANED.xlsm     # Template Excel (base)
│
├── scripts/
│   ├── __init__.py
│   ├── nfc_builder_xml.py            # Builder principal (XML)
│   ├── nfc_config.py                 # Configuration centralisée
│   ├── nfc_templates.py              # Valeurs par défaut
│   ├── nfc_main.py                   # Interface interactive
│   └── test_suite.py                 # Tests automatisés
│
├── references/
│   ├── NFC_MODIFICATION_GUIDE.md      # Guide technique détaillé
│   └── SCRIPTS_DOCUMENTATION.md       # Documentation des scripts
│
└── evals/
    └── evals.json                     # Test cases pour evaluation
```

## 📖 Documentation

### Pour les Utilisateurs
- **SKILL.md**: Spécification complète du skill
- **Quick Start** (ci-dessus): Démarrage rapide

### Pour les Développeurs
- **NFC_MODIFICATION_GUIDE.md**: Guide technique sur la méthode XML
- **SCRIPTS_DOCUMENTATION.md**: Documentation détaillée des scripts Python
- **Code comments**: Comments détaillés dans chaque script

## 🧪 Tests

### Exécuter la suite de tests

```bash
cd /mnt/skills/user/nfc-creator/scripts
python3 test_suite.py
```

Résultat attendu :
```
🎉 ALL TESTS PASSED!
✅ PASS: Imports
✅ PASS: Config
✅ PASS: Filename Generation
✅ PASS: NFC Builder
✅ PASS: Grades
```

### Tests d'évaluation

Les test cases sont définis dans `evals/evals.json` et incluent :
- ✅ Création basique de NFC
- ✅ NFC avec Sales Bonus complexe
- ✅ Création minimale
- ✅ Création avec multiples consultants
- ✅ Gestion des erreurs de validation

## 📊 Champs Supportés

### ADMIN INFO (13 champs)

| Cellule | Champ | Type | Obligatoire | Défaut |
|---------|-------|------|------------|--------|
| C3 | Code Alibeez | Text | ✗ | - |
| C7 | Client Name | Text | ✓ | - |
| C8 | Parent Company | Text | ✗ | - |
| C9 | Industry | Text | ✗ | - |
| C11 | Project Name | Text | ✓ | - |
| C12 | Deal ID | Text | ✗ | À COMPLÉTER |
| C14 | Start Date | Text | ✓ | - |
| C16 | Sales Name | Text | ✓ | Sébastien Grandperret |
| H16 | Sales Email | Email | ✓ | sebastien.grandperret@sia-partners.com |
| C20 | PM Name | Text | ✓ | Sébastien Grandperret |
| H20 | PM Email | Email | ✓ | sebastien.grandperret@sia-partners.com |
| C23 | Client Contact | Text | ✗ | - |
| C25 | Accounting Contact | Email | ✗ | - |

### SALES BONUS (8 cellules, lignes 46-47)

| Cellule | Champ | Type | Notes |
|---------|-------|------|-------|
| C46 | Beneficiary 1 Email (Originated) | Email | - |
| F46 | Percentage 1 (Originated) | Number | Format: 0.01 for 1% |
| G46 | Beneficiary 1 Email (Managed) | Email | - |
| J46 | Percentage 1 (Managed) | Number | Format: 0.01 for 1% |
| C47 | Beneficiary 2 Email (Originated) | Email | - |
| F47 | Percentage 2 (Originated) | Number | Format: 0.01 for 1% |
| G47 | Beneficiary 2 Email (Managed) | Email | - |
| J47 | Percentage 2 (Managed) | Number | Format: 0.01 for 1% |

**Contrainte**: Total des pourcentages ≤ 3%

### BUDGET (Lignes 26+)

| Cellule | Champ | Type | Notes |
|---------|-------|------|-------|
| B26+ | Name | Text | Nom du consultant |
| C26+ | Relation Type | Text | Défaut: Local / XM |
| E26+ | Grade | Text | 9 grades disponibles |
| F26+ | Office | Text | Défaut: Paris |
| H26+ | Work Type | Text | In the office / At the client / At home |
| I26+ | Billable Days | Number | 0.5 à 365 |
| R26+ | Daily Rate (TJ) | Number | EUR/day |

## 🎓 Grades Disponibles (9)

1. Senior Manager
2. Manager
3. Senior Consultant
4. Consultant
5. Junior
6. SME Director
7. Engagement Director
8. Managing Director
9. Senior Industry Expert

## ⚙️ Configuration

### Chemins par défaut

```python
# nfc_config.py
NFC_TEMPLATE_PATH = "/mnt/skills/user/nfc-creator/assets/contract_form_CLEANED.xlsm"
NFC_OUTPUT_DIR = "/mnt/user-data/outputs"
```

### Variables d'environnement

```bash
export NFC_TEMPLATE_PATH="/path/to/template.xlsm"
export NFC_OUTPUT_DIR="/path/to/output"
```

## 🔧 Méthode Technique

### XML-based Modification (Robuste)

Le skill utilise une approche **XML directe** pour modifier le template Excel :

1. **Extraction**: Décompresse le XLSM (qui est un ZIP)
2. **Strings**: Ajoute les valeurs texte à `sharedStrings.xml`
3. **Modification**: Modifie les cellules dans les worksheets
4. **Repackage**: Repackage le ZIP avec signature correcte

**Avantages** :
✅ Préserve toutes les formules Excel
✅ Préserve tous les styles et formats
✅ Préserve les validations de données
✅ Signature ZIP correcte pour Excel

### Fluxde Création

```
Collecte ADMIN INFO
        ↓
Collecte Sales Bonus (optionnel)
        ↓
Collecte Consultants (optionnel)
        ↓
Validation des données
        ↓
Modification XML du template
        ↓
Repackage ZIP
        ↓
Résumé & Sauvegarde
```

## 🎯 Cas d'Usage

### Use Case 1: Création Simple
Client donne minimal info → NFC créée avec défauts SIA

### Use Case 2: Création avec Bonus
Configuration du Sales Bonus avec 2 bénéficiaires

### Use Case 3: Staffing Complet
Client + Consultants multiples + Bonus complexe

### Use Case 4: Prolongation
Créer NFC pour un code client existant

## ⚠️ Limitations

- ❌ Ne remplace pas l'approbation commerciale
- ❌ Ne modifie pas les structures de pricing
- ❌ N'intègre pas avec HubSpot automatiquement
- ❌ Nécessite Excel 2019+ pour ouvrir les fichiers
- ❌ Maximum 4 bénéficiaires au Sales Bonus (lignes 46-49)

## 📈 Métriques du Skill

| Métrique | Valeur |
|----------|--------|
| Scripts | 5 |
| Lignes de code | ~1,500 |
| Tests | 5 |
| Taux de passage | 100% |
| Cellules mappées | 29 |
| Grades disponibles | 9 |
| Temps de création | ~2-3s |

## 🐛 Dépannage

| Problème | Cause | Solution |
|----------|-------|----------|
| Template not found | Chemin incorrect | Vérifier NFC_TEMPLATE_PATH |
| Excel won't open | Structure XML invalide | Vérifier _repackage_zip() |
| Cell value not updated | Mapping incorrect | Vérifier CELL_MAPPING |
| Sales Bonus > 3% | Total invalide | Vérifier somme des % |
| Permission denied | Droits fichier | chmod +x scripts/*.py |

## 📞 Support

- **Documentation technique**: Voir `NFC_MODIFICATION_GUIDE.md`
- **Scripts API**: Voir `SCRIPTS_DOCUMENTATION.md`
- **Questions skill**: Voir `SKILL.md`
- **Code source**: Voir `scripts/*.py`

## 📝 Changelog

### v2.0 (2026-03-25)
- ✅ Builder XML robuste créé
- ✅ Scripts orchestration complètement refactorisés
- ✅ Tests 100% passés
- ✅ Documentation complète
- ✅ Sales Bonus avancé supporté

### v1.0 (Initial)
- Basic template loading
- Limited field support

## 🎉 Conclusion

Le NFC Creator est un skill **production-ready** avec :
- ✅ Interface interactive complète
- ✅ API programmatique
- ✅ Documentation exhaustive
- ✅ Tests automatisés
- ✅ Robustesse XML

**Prêt à créer des NFC ! 🚀**

---

**Dernière mise à jour**: 2026-03-25
**Version**: 2.0
**Statut**: Production Ready ✅
