# NFC Skill - Script Principal
# =============================
# Orchestre la création complète d'une NFC avec collecte de données interactive

import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# Import des modules du skill
from nfc_builder_xml import NCFBuilderXML, create_nfc
from nfc_config import (
    NFC_TEMPLATE_PATH, NFC_OUTPUT_DIR, CELL_MAPPING,
    get_output_filename, QUESTIONS, CONSULTANT_QUESTIONS,
    MESSAGES, DEFAULT_CONFIG
)
from nfc_templates import DEFAULT_ADMIN_INFO, AVAILABLE_GRADES


class NCFCreator:
    """Orchestrateur de la création d'une NFC complète"""
    
    def __init__(self):
        self.admin_info = {}
        self.sales_bonus = []
        self.consultants = []
        self.output_path = None
    
    def collect_admin_info(self) -> Dict:
        """Collecte les infos ADMIN INFO (client, projet, contacts)"""
        print("\n" + "=" * 70)
        print("📋 INFORMATIONS CLIENT & PROJET")
        print("=" * 70)
        
        admin_info = DEFAULT_ADMIN_INFO.copy()
        
        # Questions obligatoires
        print("\n✓ Champs obligatoires:")
        
        # Client name
        while True:
            client_name = input("\n1️⃣ Nom du client? ")
            if len(client_name) >= 2:
                admin_info["client_name"] = client_name
                break
            print("   ❌ Le nom doit contenir au moins 2 caractères")
        
        # Project name
        while True:
            project_name = input("2️⃣ Nom du projet? ")
            if len(project_name) >= 2:
                admin_info["project_name"] = project_name
                break
            print("   ❌ Le nom doit contenir au moins 2 caractères")
        
        # Start date
        while True:
            start_date = input("3️⃣ Date de début (DD/MM/YYYY)? ")
            try:
                datetime.strptime(start_date, "%d/%m/%Y")
                admin_info["start_date"] = start_date
                break
            except ValueError:
                print("   ❌ Format invalide. Utiliser DD/MM/YYYY")
        
        # Questions optionnelles
        print("\n✓ Champs optionnels (appuyer sur Entrée pour ignorer):")
        
        project_code = input("4️⃣ Code Alibeez? ").strip()
        if project_code:
            admin_info["project_code"] = project_code
        
        parent_company = input("5️⃣ Groupe parent? ").strip()
        if parent_company:
            admin_info["parent_company"] = parent_company
        
        industry = input("6️⃣ Secteur? ").strip()
        if industry:
            admin_info["industry"] = industry
        
        client_contact = input("7️⃣ Contact client (nom)? ").strip()
        if client_contact:
            admin_info["client_contact"] = client_contact
        
        accounting_contact = input("8️⃣ Contact comptabilité (email)? ").strip()
        if accounting_contact:
            admin_info["accounting_contact"] = accounting_contact
        
        # Deal ID
        deal_id = input("9️⃣ Deal ID HubSpot (optionnel)? ").strip()
        if deal_id:
            admin_info["deal_id"] = deal_id
        
        self.admin_info = admin_info
        
        print(f"\n✅ Infos client collectées:")
        print(f"   • Client: {admin_info['client_name']}")
        print(f"   • Projet: {admin_info['project_name']}")
        print(f"   • Démarrage: {admin_info['start_date']}")
        
        return admin_info
    
    def collect_sales_bonus(self) -> List[Dict]:
        """Collecte la configuration du Sales Bonus"""
        print("\n" + "=" * 70)
        print("💰 CONFIGURATION SALES BONUS (optionnel)")
        print("=" * 70)
        print("Max 3% total | Réparti entre Originated (origination) et Managed (gestion)")
        
        while True:
            configure = input("\nConfigurer le Sales Bonus (o/n)? [n] ").strip().lower()
            if configure in ['o', 'y', 'oui']:
                break
            elif configure in ['n', 'non', '']:
                # Utiliser les valeurs par défaut
                print("ℹ️ Utilisation des valeurs par défaut (Sébastien Grandperret 3%)")
                self.sales_bonus = []
                return []
            print("   Tapez 'o' ou 'n'")
        
        # Collecter les bénéficiaires
        beneficiaries = []
        for idx in range(1, 3):  # Max 2 bénéficiaires
            print(f"\n--- Bénéficiaire {idx} ---")
            
            email_orig = input(f"Email (Originated)? ").strip()
            if not email_orig:
                break
            
            while True:
                try:
                    percent_orig = float(input(f"Pourcentage Originated (ex: 0.01 pour 1%)? "))
                    if 0 <= percent_orig <= 1:
                        break
                    print("   ❌ Doit être entre 0 et 1")
                except ValueError:
                    print("   ❌ Nombre invalide")
            
            email_managed = input(f"Email (Managed)? ").strip()
            if not email_managed:
                email_managed = email_orig
            
            while True:
                try:
                    percent_managed = float(input(f"Pourcentage Managed (ex: 0.005 pour 0.5%)? "))
                    if 0 <= percent_managed <= 1:
                        break
                    print("   ❌ Doit être entre 0 et 1")
                except ValueError:
                    print("   ❌ Nombre invalide")
            
            beneficiaries.append({
                'email_orig': email_orig,
                'percent_orig': percent_orig,
                'email_managed': email_managed,
                'percent_managed': percent_managed
            })
        
        # Valider le total
        total = sum(b['percent_orig'] + b['percent_managed'] for b in beneficiaries)
        if total > 0.03:
            print(f"\n❌ Total {total*100:.1f}% > 3% max!")
            print("   Recommencez...")
            return self.collect_sales_bonus()
        
        self.sales_bonus = beneficiaries
        print(f"\n✅ Sales Bonus configuré: {len(beneficiaries)} bénéficiaires, total {total*100:.1f}%")
        
        return beneficiaries
    
    def collect_consultants(self) -> List[Dict]:
        """Collecte les données des consultants"""
        print("\n" + "=" * 70)
        print("👥 AJOUTER LES CONSULTANTS (Budget)")
        print("=" * 70)
        
        consultants = []
        idx = 1
        
        while True:
            print(f"\n--- Consultant {idx} ---")
            
            # Nom
            name = input("Nom? ").strip()
            if not name:
                break
            
            # Grade
            print("\nGrades disponibles:")
            for i, grade in enumerate(AVAILABLE_GRADES.keys(), 1):
                print(f"  {i}. {grade}")
            
            while True:
                try:
                    grade_choice = int(input("Numéro du grade? "))
                    grade = list(AVAILABLE_GRADES.keys())[grade_choice - 1]
                    break
                except (ValueError, IndexError):
                    print("   ❌ Choix invalide")
            
            # Jours
            while True:
                try:
                    days = float(input("Jours facturés? "))
                    if 0.5 <= days <= 365:
                        break
                    print("   ❌ Entre 0.5 et 365")
                except ValueError:
                    print("   ❌ Nombre invalide")
            
            # TJ
            while True:
                try:
                    tj = float(input("TJ (EUR/jour)? "))
                    if 100 <= tj <= 10000:
                        break
                    print("   ❌ Entre 100 et 10000 EUR")
                except ValueError:
                    print("   ❌ Nombre invalide")
            
            # Optionnels
            office = input("Bureau (défaut Paris)? ").strip() or "Paris"
            work_type = input("Type travail (défaut In the office)? ").strip() or "In the office"
            
            consultant = {
                'name': name,
                'grade': grade,
                'days': days,
                'tj': tj,
                'office': office,
                'work_type': work_type
            }
            
            consultants.append(consultant)
            print(f"✅ {name} ajouté ({grade}, {days}j @ {tj}€/j)")
            
            # Continuer?
            while True:
                continue_choice = input("\nAjouter un autre consultant (o/n)? [n] ").strip().lower()
                if continue_choice in ['o', 'y', 'oui']:
                    idx += 1
                    break
                elif continue_choice in ['n', 'non', '']:
                    break
                print("   Tapez 'o' ou 'n'")
            
            if not continue_choice or continue_choice in ['n', 'non', '']:
                break
        
        self.consultants = consultants
        print(f"\n✅ {len(consultants)} consultant(s) ajouté(s)")
        
        return consultants
    
    def generate_nfc(self) -> bool:
        """Génère le fichier NFC"""
        print("\n" + "=" * 70)
        print("🔨 GÉNÉRATION DE LA NFC")
        print("=" * 70)
        
        # Générer le nom de fichier
        filename = get_output_filename(self.admin_info['client_name'])
        self.output_path = os.path.join(NFC_OUTPUT_DIR, filename)
        
        print(f"\n📄 Génération: {filename}")
        
        try:
            # Créer la NFC
            success, message = create_nfc(
                template_path=NFC_TEMPLATE_PATH,
                output_path=self.output_path,
                admin_info=self.admin_info,
                sales_bonus=self.sales_bonus if self.sales_bonus else None,
                consultants=self.consultants if self.consultants else None
            )
            
            if success:
                print(f"✅ {message}")
                print(f"📁 Fichier: {self.output_path}")
                return True
            else:
                print(f"❌ {message}")
                return False
        
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            return False
    
    def show_summary(self) -> None:
        """Affiche un résumé de la NFC créée"""
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ DE LA NFC CRÉÉE")
        print("=" * 70)
        
        print(f"\n📋 CLIENT & PROJET:")
        print(f"   • Client: {self.admin_info['client_name']}")
        print(f"   • Projet: {self.admin_info['project_name']}")
        print(f"   • Démarrage: {self.admin_info['start_date']}")
        
        if self.sales_bonus:
            total_bonus = sum(b['percent_orig'] + b['percent_managed'] for b in self.sales_bonus)
            print(f"\n💰 SALES BONUS:")
            for b in self.sales_bonus:
                total = b['percent_orig'] + b['percent_managed']
                print(f"   • {b['email_orig']}: {total*100:.1f}%")
            print(f"   Total: {total_bonus*100:.1f}%")
        else:
            print(f"\n💰 SALES BONUS: Défaut (Sébastien Grandperret 3%)")
        
        print(f"\n👥 CONSULTANTS: {len(self.consultants)}")
        for c in self.consultants:
            revenue = c['days'] * c['tj']
            print(f"   • {c['name']}: {c['grade']}, {c['days']}j @ {c['tj']}€ = {revenue:,.0f}€")
        
        print(f"\n✅ NFC créée: {os.path.basename(self.output_path)}")
    
    def run(self) -> bool:
        """Exécute le flux complet"""
        try:
            # Bienvenue
            print("\n" + "=" * 70)
            print("🎯 CRÉER UNE NOUVELLE NFC - SIA PARTNERS")
            print("=" * 70)
            print("\nDefaults pré-remplis:")
            print("  • Hub: FIM")
            print("  • Marché: Paris")
            print("  • Devise: EUR")
            print("  • PM: Sébastien Grandperret")
            
            # Collecter les données
            self.collect_admin_info()
            self.collect_sales_bonus()
            self.collect_consultants()
            
            # Confirmation
            print("\n" + "=" * 70)
            print("⚠️ AVANT DE CONTINUER")
            print("=" * 70)
            confirm = input("\nLes données sont correctes? (o/n) [o] ").strip().lower()
            if confirm in ['n', 'non']:
                print("❌ Annulation")
                return False
            
            # Générer
            if not self.generate_nfc():
                return False
            
            # Résumé
            self.show_summary()
            
            print("\n✅ NFC créée avec succès!")
            print(f"📁 Chemin: {self.output_path}")
            
            return True
        
        except KeyboardInterrupt:
            print("\n\n❌ Opération annulée par l'utilisateur")
            return False
        except Exception as e:
            print(f"\n❌ Erreur: {str(e)}")
            return False


def main():
    """Point d'entrée - accepte un template en paramètre"""
    if len(sys.argv) > 1:
        template_path = sys.argv[1]
        if not os.path.exists(template_path):
            print(f"❌ Erreur: Template non trouvé: {template_path}")
            sys.exit(1)
        print(f"\n📄 Utilisation du template: {template_path}")
        # TODO: Passer le template à NCFCreator
    else:
        template_path = NFC_TEMPLATE_PATH
        if not os.path.exists(template_path):
            print(f"❌ Erreur: Template par défaut non trouvé: {template_path}")
            print(f"⚠️ Veuillez fournir un template en paramètre:")
            print(f"   python nfc_main.py /chemin/vers/template.xlsm")
            sys.exit(1)
    
    creator = NCFCreator()
    success = creator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
