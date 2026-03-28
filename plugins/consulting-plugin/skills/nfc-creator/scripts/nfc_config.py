# NFC Skill - Init et Configuration
# ==================================

"""
Fichier de configuration pour initialiser le skill NFC
Contient tous les réglages par défaut et chemins
"""

import os
from pathlib import Path
from typing import Dict

# ============================================================================
# CHEMINS
# ============================================================================

# Chemin du template NFC - DOIT ÊTRE FOURNI EN PARAMÈTRE OU VIA ENV
# ⚠️ Le template n'est PAS embarqué dans le skill (trop volumineux ~60MB)
# Fournir un template en paramètre: python nfc_main.py /chemin/vers/template.xlsm
NFC_TEMPLATE_PATH = os.getenv("NFC_TEMPLATE_PATH", None)

# Chemin de sortie (dossier où sauvegarder les NCF créées)
NFC_OUTPUT_DIR = os.getenv(
    "NFC_OUTPUT_DIR",
    "/mnt/user-data/outputs"
)

# Assurer que les répertoires existent
Path(NFC_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# ============================================================================
# MAPPING DES CELLULES EXCEL
# ============================================================================

CELL_MAPPING = {
    "ADMIN_INFO": {
        # Projet et Client
        "client_name": "C7",
        "parent_company": "C8",
        "industry": "C9",
        "project_code": "C3",
        "project_name": "C11",
        "deal_id": "C12",
        "start_date": "C14",
        
        # Contacts commerciaux
        "sales_name": "C16",
        "sales_email": "H16",
        "pm_name": "C20",
        "pm_email": "H20",
        
        # Contacts client
        "client_contact": "C23",
        "accounting_contact": "C25",
    },
    "SALES_BONUS": {
        # Bénéficiaire 1 (Ligne 46)
        "beneficiary_1_email_orig": "C46",
        "beneficiary_1_percent_orig": "F46",
        "beneficiary_1_email_managed": "G46",
        "beneficiary_1_percent_managed": "J46",
        
        # Bénéficiaire 2 (Ligne 47)
        "beneficiary_2_email_orig": "C47",
        "beneficiary_2_percent_orig": "F47",
        "beneficiary_2_email_managed": "G47",
        "beneficiary_2_percent_managed": "J47",
    },
    "BUDGET": {
        "consultant_name": "B",
        "relation_type": "C",
        "hub": "D",
        "grade": "E",
        "office": "F",
        "work_type": "H",
        "billable_days": "I",
        "daily_rate": "R",
    }
}

# ============================================================================
# VALEURS PAR DÉFAUT
# ============================================================================

DEFAULT_CONFIG = {
    # Admin Info
    "admin_info": {
        "ncf_creation_date": "=TODAY()",
        "billing_entity_hub": "FIM",
        "billing_company": "Sia Partners France",
        "sales_hub": "FIM",
        "billing_market": "Paris",
        "operational_manager_name": "Sébastien Grandperret",
        "operational_manager_email": "sebastien.grandperret@sia-partners.com",
        "sales_bonus_max": 0.03,
        "sales_bonus_originated": 0.015,
        "sales_bonus_managed": 0.015,
    },
    
    # Budget
    "budget": {
        "currency": "EUR",
        "basis": "Daily",
        "hub": "FIM",
        "office": "Paris",
        "work_type": "In the office",
        "relation_type": "Local / XM",
    },
    
    # Grades disponibles
    "grades": [
        "Senior Manager",
        "Manager",
        "Senior Consultant",
        "Consultant",
        "Junior",
        "SME Director",
        "Engagement Director",
        "Managing Director",
        "Senior Industry Expert",
    ],
    
    # Marges cibles
    "target_margins": {
        "Senior Manager": 0.50,
        "Manager": 0.50,
        "Senior Consultant": 0.50,
        "Consultant": 0.50,
        "Junior": 0.50,
        "SME Director": 0.45,
        "Engagement Director": 0.45,
        "Managing Director": 0.45,
        "Senior Industry Expert": 0.45,
    },
    
    # Hubs et marchés correspondants
    "hubs": {
        "FIM": ["Paris", "Lyon", "Marseille", "Rome", "Milan", "Casablanca", "Marrakech"],
        "BENELUX": ["Bruxelles", "Amsterdam", "Anvers", "Luxembourg"],
        "APAC": ["Singapour", "Hong Kong", "Mumbai", "Bangkok"],
        "UK&I": ["Londres", "Manchester", "Dublin", "Édimbourg"],
        "MIDDLE EAST": ["Dubaï", "Abu Dhabi", "Riyad", "Doha"],
        "NORTH AMERICA": ["New York", "Toronto", "San Francisco", "Chicago"],
    },
    
    # Types de travail
    "work_types": ["In the office", "At the client", "At home"],
    
    # Devises
    "currencies": ["EUR", "USD", "GBP", "CHF", "CAD", "AED", "AUD", "CNY", "JPY", "MAD"],
}

# ============================================================================
# QUESTIONS INTERACTIVES
# ============================================================================

QUESTIONS = {
    "client_name": {
        "label": "Nom du client (exact)?",
        "required": True,
        "type": "text",
    },
    "billing_market": {
        "label": "Marché/Localité (défaut Paris)?",
        "required": False,
        "type": "select",
        "default": "Paris",
    },
    "project_code": {
        "label": "Code Alibeez (optionnel)?",
        "required": False,
        "type": "text",
    },
    "parent_company": {
        "label": "Groupe parent (optionnel)?",
        "required": False,
        "type": "text",
    },
    "industry": {
        "label": "Secteur (optionnel)?",
        "required": False,
        "type": "text",
    },
}

CONSULTANT_QUESTIONS = {
    "name": {
        "label": "Nom du consultant?",
        "required": True,
        "type": "text",
    },
    "grade": {
        "label": "Grade/Profil?",
        "required": True,
        "type": "select",
        "options": DEFAULT_CONFIG["grades"],
    },
    "days": {
        "label": "Jours facturés?",
        "required": True,
        "type": "number",
        "min": 0,
        "max": 365,
    },
    "tj": {
        "label": "TJ (optionnel, sinon auto)?",
        "required": False,
        "type": "number",
        "min": 0,
    },
    "work_type": {
        "label": "Type travail (défaut In the office)?",
        "required": False,
        "type": "select",
        "options": DEFAULT_CONFIG["work_types"],
        "default": "In the office",
    },
}

# ============================================================================
# MESSAGES
# ============================================================================

MESSAGES = {
    "welcome": """
🎯 Créer une nouvelle NCF (New Contract Form)

Les champs par défaut sont pré-remplis:
  • Hub: FIM
  • Marché: Paris
  • Devise: EUR
  • Basis: Daily
  • PM: Sébastien Grandperret
  • Sales Bonus: 3% (1.5% Originated + 1.5% Managed)

Tu vas maintenant remplir les infos client et les ressources.
""",
    
    "client_info_start": "📋 Informations client & contrat",
    "budget_start": "💼 Ajouter les consultants (Budget)",
    "import_proposal": "📁 Importer une propale Excel (optionnel)?",
    "summary": "📊 Synthèse des marges",
    "success": "✅ NCF créée avec succès!",
    
    "add_another": "Ajouter un autre consultant?",
    "confirm_data": "Les données sont correctes?",
    "extraction_found": "Données trouvées dans la propale. À vérifier?",
}

# ============================================================================
# VALIDATION
# ============================================================================

VALIDATION_RULES = {
    "client_name": {
        "min_length": 2,
        "max_length": 100,
    },
    "days": {
        "min": 0.5,
        "max": 365,
    },
    "tj": {
        "min": 100,
        "max": 10000,
    },
}

# ============================================================================
# FORMAT DE SORTIE NCF
# ============================================================================

def get_output_filename(client_name: str, year_month: str = None) -> str:
    """
    Génère le nom du fichier NCF
    
    Format: NCF_CPxxxxx_YY-mm_ClientName.xlsm
    
    Args:
        client_name: Nom du client
        year_month: YY-mm (ex: 25-01)
    
    Returns:
        Nom du fichier
    """
    from datetime import datetime
    
    if not year_month:
        now = datetime.now()
        year_month = now.strftime("%y-%m")
    
    # Nettoyer le nom du client
    clean_name = client_name.replace(" ", "").replace("/", "").replace("\\", "")[:30]
    
    return f"NCF_{year_month}_{clean_name}.xlsm"


# ============================================================================
# FONCTION D'INITIALISATION
# ============================================================================

def init_skill() -> Dict:
    """Initialise le skill avec vérifications"""
    
    config = DEFAULT_CONFIG.copy()
    
    # Vérifier le template (optionnel - doit être fourni explicitement)
    if NFC_TEMPLATE_PATH:
        if not os.path.exists(NFC_TEMPLATE_PATH):
            raise FileNotFoundError(f"Template NFC non trouvé: {NFC_TEMPLATE_PATH}")
        config["template_path"] = NFC_TEMPLATE_PATH
    else:
        config["template_path"] = None
    
    # Vérifier le dossier output
    if not os.path.exists(NFC_OUTPUT_DIR):
        os.makedirs(NFC_OUTPUT_DIR)
    
    # Ajouter les infos de chemin
    config["output_dir"] = NFC_OUTPUT_DIR
    
    return config


# ============================================================================
# VALEURS MODIFIABLES
# ============================================================================

"""
Les défauts ci-dessus peuvent être overridés à l'exécution.

Exemple:
    create_nfc(
        client_name="ABC Client",
        billing_market="Bruxelles",  # Au lieu de Paris
        currency="USD",              # Au lieu de EUR
        consultants=[...]
    )

Seules les valeurs non fournies utilisent les défauts.
"""
