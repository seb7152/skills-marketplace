# NFC Skill - Templates et Valeurs par Défaut
# ============================================

from datetime import datetime

# VALEURS PAR DÉFAUT - ADMIN INFO
# Ces valeurs sont pré-remplies dans chaque NFC créée
DEFAULT_ADMIN_INFO = {
    # Infos automatiques
    "ncf_creation_date": datetime.now().strftime("%d/%m/%Y"),
    
    # Infos système (pré-remplies, non modifiables)
    "billing_entity_hub": "FIM",
    "billing_company": "Sia Partners France",  # C5
    "billing_bu": "FPR",  # H18
    "sales_hub": "FIM",
    "billing_market": "Paris",
    "billing_type": "Schedule (Fixed Fee)",  # C36
    "minimum_time_submission": "Half day",  # C37
    
    # Contacts par défaut (Sébastien Grandperret)
    "operational_manager_name": "Sébastien Grandperret",
    "operational_manager_email": "sebastien.grandperret@sia-partners.com",
    "sales_name": "Sébastien Grandperret",
    "sales_email": "sebastien.grandperret@sia-partners.com",
    
    # Sales Bonus par défaut
    "sales_bonus_max": 0.03,  # 3%
    "sales_bonus_originated": 0.015,  # 1.5%
    "sales_bonus_managed": 0.015,  # 1.5%
    
    # À remplir par l'utilisateur
    "client_name": None,  # Obligatoire
    "project_name": None,  # Obligatoire
    "start_date": None,  # Obligatoire (DD/MM/YYYY)
    "deal_id": "À COMPLÉTER",  # Placeholder
    "project_code": None,  # Optionnel
    "parent_company": None,  # Optionnel
    "industry": None,  # Optionnel
    "client_contact": None,  # Optionnel
    "accounting_contact": None,  # Optionnel
}

# VALEURS PAR DÉFAUT - BUDGET
DEFAULT_BUDGET_PARAMS = {
    "currency": "EUR",
    "basis": "Daily",
    "hub": "FIM",
    "office": "Paris",
    "type": "In the office",
}

# GRADES DISPONIBLES (avec codes)
AVAILABLE_GRADES = {
    "Senior Manager": "SM",
    "Manager": "Mgr",
    "Senior Consultant": "SC",
    "Consultant": "C",
    "Junior": "JC",
    "SME Director": "SMED",
    "Engagement Director": "ED",
    "Managing Director": "MD",
    "Senior Industry Expert": "SIE",
}

# MARGES CIBLES PAR PROFIL (référence)
TARGET_MARGINS = {
    "Senior Manager": 0.50,
    "Manager": 0.50,
    "Senior Consultant": 0.50,
    "Consultant": 0.50,
    "Junior": 0.50,
    "SME Director": 0.45,
    "Engagement Director": 0.45,
    "Managing Director": 0.45,
    "Senior Industry Expert": 0.45,
}

# HUBS ET MARCHÉS CORRESPONDANTS
HUB_MARKETS = {
    "FIM": ["Paris", "Lyon", "Marseille", "Rome", "Milan", "Casablanca", "Marrakech"],
    "BENELUX": ["Bruxelles", "Amsterdam", "Anvers", "Luxembourg"],
    "APAC": ["Singapour", "Hong Kong", "Mumbai", "Bangkok"],
    "UK&I": ["Londres", "Manchester", "Dublin", "Édimbourg"],
    "MIDDLE EAST": ["Dubaï", "Abu Dhabi", "Riyad", "Doha"],
    "NORTH AMERICA": ["New York", "Toronto", "San Francisco", "Chicago"],
}

# TYPES DE TRAVAIL
WORK_TYPES = ["In the office", "At the client", "At home"]

# DEVISES SUPPORTÉES
SUPPORTED_CURRENCIES = ["EUR", "USD", "GBP", "CHF", "CAD", "AED", "AUD", "CNY", "JPY", "MAD"]

# STRUCTURE DE RESSOURCE (template pour une ligne consultant)
CONSULTANT_TEMPLATE = {
    "numero": None,  # Auto
    "name": None,  # À remplir
    "relation_type": "Local / XM",  # Défaut
    "hub": "FIM",  # Défaut
    "role": None,  # À remplir
    "office": "Paris",  # Défaut
    "billable_days": None,  # À remplir
    "grade": None,  # À remplir (liste)
    "work_type": "In the office",  # Défaut
    "start_date": None,  # Optionnel
    "rate": None,  # Calculé automatiquement
}

# MESSAGES UTILISATEUR
MESSAGES = {
    "welcome": "📋 Création d'une nouvelle NCF",
    "client_info": "Informations client & contrat",
    "budget_info": "Structure de ressources (Budget)",
    "optional_import": "Importer une propale Excel (optionnel)",
    "consultant_form": "Ajouter un consultant",
    "summary": "📊 Synthèse des marges",
    "success": "✅ NCF créée avec succès!",
}
