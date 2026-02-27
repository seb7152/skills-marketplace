# Consulting Plugin - Marketplace

Plugin professionnel de consulting pour Claude Code, offrant des compétences expertes en :

- 📋 **Évaluation d'appels d'offres (RFP)** - Analyse systématique et notation des réponses fournisseurs
- 📥 **Import de données RFP** - Extraction structurée depuis Excel/Word vers JSON
- 💼 **Propositions commerciales** *(à venir)*
- 📝 **Cahiers des charges** *(à venir)*

## Installation

### Depuis GitHub (recommandé)

```bash
# Dans Claude Code
/plugin marketplace add owner/consulting-plugin
/plugin install consulting-plugin@consulting-tools
```

> ⚠️ Remplacez `owner/consulting-plugin` par votre organisation/repo GitHub

### Installation locale (pour tests)

```bash
# Depuis le répertoire du projet
cd /path/to/skills-marketplace

# Dans Claude Code
/plugin marketplace add ./consulting-plugin
/plugin install consulting-plugin@consulting-tools
```

## Configuration MCP

Ce plugin inclut un serveur MCP pour accéder à l'API RFP Analyzer.

### 1. Obtenir votre token

Récupérez votre token d'accès pour le serveur RFP Analyzer depuis votre compte.

### 2. Configurer la variable d'environnement

**Option A : Fichier .env (recommandé pour développement local)**

```bash
# Copier le fichier exemple
cp .env.example .env

# Éditer .env et remplacer 'your_token_here' par votre token
# Le fichier .env est déjà dans .gitignore (sécurisé)
```

**Option B : Variable d'environnement shell (recommandé pour production)**

```bash
# Pour macOS/Linux - Ajoutez à ~/.zshrc ou ~/.bashrc
export RFP_ANALYZER_TOKEN="votre_token_ici"

# Recharger la configuration
source ~/.zshrc  # ou source ~/.bashrc
```

**Pour Windows (PowerShell)** :
```powershell
# Ajouter à votre profil PowerShell
$env:RFP_ANALYZER_TOKEN = "votre_token_ici"

# Ou définir de manière permanente
[System.Environment]::SetEnvironmentVariable('RFP_ANALYZER_TOKEN', 'votre_token_ici', 'User')
```

### 3. Vérifier la configuration

Après installation du plugin, le serveur MCP `rfp-analyzer` sera automatiquement disponible dans Claude Code.

**URL du serveur MCP** : `https://rfp-analyzer-ashy.vercel.app/api/mcp?token=${RFP_ANALYZER_TOKEN}`

⚠️ **Important** : Ne commitez JAMAIS votre token dans Git. Utilisez toujours des variables d'environnement.

## Skills disponibles

### 🎯 rfp-evaluation

Évalue systématiquement les réponses des fournisseurs à un appel d'offres.

**Utilisation :**
- Mentionnez "évalue les offres" ou "lance l'évaluation du RFP"
- Le skill se déclenche automatiquement

**Fonctionnalités :**
- Executive Summary du cahier des charges
- Évaluation catégorie par catégorie avec scores 0-5
- Comparaison multi-fournisseurs
- Export Excel (format par fournisseur ou consolidé)
- Génération de questions pour soutenance
- Intégration MCP rfp-analyzer

**Documentation complète :** [skills/rfp-evaluation/](skills/rfp-evaluation/)

### 📥 rfp-import-extractor

Extrait les données RFP structurées depuis Excel/Word vers JSON validé.

**Utilisation :**
- "Extract requirements from this Excel file"
- "Import supplier responses from this file"

**Fonctionnalités :**
- Analyse intelligente de la structure des fichiers
- Scripts d'extraction personnalisés et réutilisables
- Support Excel (openpyxl) et Word (python-docx)
- Validation JSON stricte
- Export pour import MCP rfp-analyzer

**Documentation complète :** [skills/rfp-import-extractor/](skills/rfp-import-extractor/)

## Prérequis

### Serveur MCP (Requis)

- **RFP Analyzer Token** : Variable d'environnement `RFP_ANALYZER_TOKEN` configurée
- Le serveur MCP sera automatiquement disponible après installation du plugin

### Pour rfp-evaluation

- **Serveur MCP rfp-analyzer** : configuré automatiquement par le plugin
- **Python openpyxl** : pour génération Excel
  ```bash
  pip install openpyxl
  ```
- Documents RFP : CDC, grille d'exigences, réponses fournisseurs

### Pour rfp-import-extractor

- **Python 3.8+**
- **openpyxl** : pour extraction Excel
  ```bash
  pip install openpyxl
  ```
- **python-docx** : pour extraction Word
  ```bash
  pip install python-docx
  ```

## Configuration

Après installation, les skills sont disponibles avec le préfixe du plugin :

```bash
# Si vous utilisez la version avec namespace
/consulting-plugin:rfp-evaluation
/consulting-plugin:rfp-import-extractor

# Ou simplement mentionner le besoin, les skills se déclenchent automatiquement
```

## Structure du plugin

```
consulting-plugin/
├── .claude-plugin/
│   ├── plugin.json           # Manifeste du plugin
│   └── marketplace.json      # Catalogue de la marketplace
│
├── skills/
│   ├── rfp-evaluation/
│   │   ├── skill.MD
│   │   ├── docs/            # MCP API, Workflow, Integration
│   │   ├── references/      # Guides (scoring, executive summary, etc.)
│   │   └── scripts/         # generate_evaluation_grid.py
│   │
│   └── rfp-import-extractor/
│       ├── skill.MD
│       ├── references/      # Guides (JSON schemas, script building, etc.)
│       └── scripts/         # validate_json.py, templates d'extraction
│
└── README.md               # Ce fichier
```

## Roadmap

### Version 1.1.0 (à venir)
- [ ] Skill **commercial-proposal** : Rédaction de propositions commerciales
- [ ] Skill **specification-writing** : Rédaction de cahiers des charges

### Version 1.2.0
- [ ] Templates de propositions par secteur (IT, Conseil, Formation)
- [ ] Calculateur de pricing intégré
- [ ] Export PowerPoint pour présentations

## Développement et contribution

### Tester localement

```bash
# Cloner le repo
git clone https://github.com/owner/consulting-plugin.git
cd consulting-plugin

# Lancer Claude Code avec le plugin
claude --plugin-dir .

# Ou ajouter comme marketplace locale
/plugin marketplace add .
/plugin install consulting-plugin@consulting-tools
```

### Valider le plugin

```bash
claude plugin validate .
```

Ou depuis Claude Code :
```bash
/plugin validate .
```

## Support et documentation

- **Issues** : [GitHub Issues](https://github.com/owner/consulting-plugin/issues)
- **Documentation complète** : Voir les dossiers `docs/` et `references/` dans chaque skill
- **Exemples** : Cas réels (ENGIE Smart Parking) dans la documentation

## License

MIT License - voir [LICENSE](LICENSE)

---

**Créé par** : Sébastien Grandperret
**Version** : 1.0.0
**Dernière mise à jour** : 2026-02-27
