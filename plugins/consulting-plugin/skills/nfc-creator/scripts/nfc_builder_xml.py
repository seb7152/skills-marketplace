# NFC Skill - Builder XML (Robuste)
# ==================================
# Utilise la méthode de modification XML pour préserver la structure Excel complète
# Cette approche préserve les validations, formules et styles du template

import zipfile
import xml.etree.ElementTree as ET
from shutil import copy2
import tempfile
import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class NCFBuilderXML:
    """Construit une NFC en modifiant directement le XML du template XLSM"""
    
    def __init__(self, template_path: str, output_path: str):
        """
        Initialise le builder
        
        Args:
            template_path: Chemin vers contract_form_CLEANED.xlsm
            output_path: Chemin de sortie pour la NFC
        """
        self.template_path = template_path
        self.output_path = output_path
        self.tmpdir = tempfile.mkdtemp()
        
        # Copier et extraire le template
        copy2(template_path, output_path)
        with zipfile.ZipFile(output_path, 'r') as z:
            z.extractall(self.tmpdir)
        
        # Enregistrer les namespaces
        ET.register_namespace('', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
        ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
        
        self.strings_to_add = {}
        self.string_indices = {}
        self.admin_info = {}
        self.budget_data = []
        self.sales_bonus = []
    
    def add_string(self, value: str) -> int:
        """Ajoute un string à sharedStrings.xml et retourne son index"""
        if value in self.strings_to_add:
            return self.string_indices[value]
        
        # Parser sharedStrings.xml
        ss_path = f'{self.tmpdir}/xl/sharedStrings.xml'
        tree = ET.parse(ss_path)
        root = tree.getroot()
        
        # Ajouter le nouveau string
        si = ET.Element('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si')
        t = ET.SubElement(si, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
        t.text = value
        root.append(si)
        
        idx = len(root) - 1
        self.string_indices[value] = idx
        self.strings_to_add[value] = idx
        
        # Sauvegarder
        tree.write(ss_path, encoding='utf-8', xml_declaration=True)
        
        return idx
    
    def set_admin_info(self, data: Dict) -> None:
        """Configure les informations ADMIN INFO"""
        self.admin_info = data
        
        # Ajouter les strings
        for key, value in data.items():
            if isinstance(value, str):
                self.add_string(value)
    
    def set_sales_bonus(self, beneficiaries: List[Dict]) -> None:
        """Configure le Sales Bonus
        
        Args:
            beneficiaries: Liste [{
                'email_orig': email,
                'percent_orig': 0.01,
                'email_managed': email,
                'percent_managed': 0.005
            }]
        """
        self.sales_bonus = beneficiaries
        
        # Ajouter les emails comme strings
        for b in beneficiaries:
            if 'email_orig' in b:
                self.add_string(b['email_orig'])
            if 'email_managed' in b:
                self.add_string(b['email_managed'])
    
    def add_consultant(self, name: str, grade: str, days: float, 
                      tj: float, office: str = "Paris", 
                      work_type: str = "In the office") -> None:
        """Ajoute un consultant au budget
        
        Note: Relation Type (colonne C) n'est pas fourni car il est 
        pré-rempli par une formule dans le template Excel.
        """
        self.budget_data.append({
            'name': name,
            'grade': grade,
            'days': days,
            'tj': tj,
            'office': office,
            'work_type': work_type
        })
        
        # Ajouter les strings
        self.add_string(name)
        self.add_string(grade)
        self.add_string(office)
        self.add_string(work_type)
    
    def _modify_worksheet(self, worksheet_name: str, modifications: Dict) -> None:
        """Modifie les cellules dans une feuille"""
        sheet_map = {'ADMIN INFO': 'sheet2.xml', 'BUDGET': 'sheet3.xml'}
        sheet_file = sheet_map.get(worksheet_name)
        
        if not sheet_file:
            return
        
        sheet_path = f'{self.tmpdir}/xl/worksheets/{sheet_file}'
        
        with open(sheet_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Appliquer les modifications
        for cell_ref, (value, cell_type) in modifications.items():
            if cell_type == 's':  # String
                if value not in self.string_indices:
                    self.add_string(value)
                idx = self.string_indices[value]
                
                # Chercher et remplacer
                pattern_empty = rf'<c r="{cell_ref}" s="\d+"/>'
                pattern_with_value = rf'<c r="{cell_ref}"[^>]*t="s"><v>\d+</v></c>'
                
                if re.search(pattern_empty, content):
                    new_cell = f'<c r="{cell_ref}" s="700" t="s"><v>{idx}</v></c>'
                    content = re.sub(pattern_empty, new_cell, content)
                elif re.search(pattern_with_value, content):
                    new_cell = f'<c r="{cell_ref}" s="700" t="s"><v>{idx}</v></c>'
                    content = re.sub(pattern_with_value, new_cell, content)
            
            elif cell_type == 'n':  # Number
                # Pour les nombres, utiliser le format directement
                pattern = rf'<c r="{cell_ref}"[^>]*><v>[^<]*</v></c>'
                new_cell = f'<c r="{cell_ref}" s="359"><v>{value}</v></c>'
                
                if re.search(pattern, content):
                    content = re.sub(pattern, new_cell, content)
        
        with open(sheet_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def build(self) -> Tuple[bool, str]:
        """Construit la NFC complète"""
        try:
            # Modifier ADMIN INFO
            admin_modifications = {}
            for key, value in self.admin_info.items():
                cell_map = {
                    'client_name': ('C7', 's'),
                    'project_name': ('C11', 's'),
                    'deal_id': ('C12', 's'),
                    'start_date': ('C14', 's'),
                    'sales_name': ('C16', 's'),
                    'sales_email': ('H16', 's'),
                    'pm_name': ('C20', 's'),
                    'pm_email': ('H20', 's'),
                    'client_contact': ('C23', 's'),
                    'accounting_contact': ('C25', 's'),
                    'billing_company': ('C5', 's'),
                    'billing_bu': ('H18', 's'),
                    'billing_type': ('C36', 's'),
                    'minimum_time_submission': ('C37', 's'),
                }
                
                if key in cell_map:
                    cell_ref, cell_type = cell_map[key]
                    admin_modifications[cell_ref] = (value, cell_type)
            
            self._modify_worksheet('ADMIN INFO', admin_modifications)
            
            # Modifier Sales Bonus
            bonus_mods = {}
            for idx, benefit in enumerate(self.sales_bonus, 1):
                row_admin = 45 + idx
                row_orig = 45 + idx  # Row pour Originated
                
                # Ligne pour Originated
                if 'email_orig' in benefit:
                    bonus_mods[f'C{row_orig}'] = (benefit['email_orig'], 's')
                    bonus_mods[f'F{row_orig}'] = (benefit['percent_orig'], 'n')
                
                # Ligne pour Managed
                if 'email_managed' in benefit:
                    bonus_mods[f'G{row_orig}'] = (benefit['email_managed'], 's')
                    bonus_mods[f'J{row_orig}'] = (benefit['percent_managed'], 'n')
            
            if bonus_mods:
                self._modify_worksheet('ADMIN INFO', bonus_mods)
            
            # Modifier BUDGET
            budget_mods = {}
            for idx, consultant in enumerate(self.budget_data):
                row = 26 + idx
                
                budget_mods[f'B{row}'] = (consultant['name'], 's')
                # ⚠️ NE PAS MODIFIER C{row} - Relation Type est pré-remplie par une formule dans le template
                budget_mods[f'E{row}'] = (consultant['grade'], 's')
                budget_mods[f'F{row}'] = (consultant['office'], 's')
                budget_mods[f'H{row}'] = (consultant['work_type'], 's')
                budget_mods[f'I{row}'] = (consultant['days'], 'n')
                budget_mods[f'R{row}'] = (consultant['tj'], 'n')
            
            if budget_mods:
                self._modify_worksheet('BUDGET', budget_mods)
            
            # Repackager le ZIP
            self._repackage_zip()
            
            return True, f"✅ NFC créée: {self.output_path}"
        
        except Exception as e:
            return False, f"❌ Erreur: {str(e)}"
    
    def _repackage_zip(self) -> None:
        """Repackage le ZIP avec l'ordre correct"""
        os.remove(self.output_path)
        
        file_list = []
        for root_dir, dirs, files in os.walk(self.tmpdir):
            for file in files:
                file_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(file_path, self.tmpdir)
                file_list.append((file_path, arcname))
        
        # IMPORTANT: [Content_Types].xml en PREMIER
        file_list.sort(key=lambda x: (x[1] != '[Content_Types].xml', x[1]))
        
        with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for file_path, arcname in file_list:
                z.write(file_path, arcname)
    
    def cleanup(self) -> None:
        """Nettoie les fichiers temporaires"""
        import shutil
        if self.tmpdir and os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)


def create_nfc(template_path: str, output_path: str, 
               admin_info: Dict, sales_bonus: List[Dict] = None,
               consultants: List[Dict] = None) -> Tuple[bool, str]:
    """
    Fonction principale de création d'une NFC
    
    Args:
        template_path: Chemin du template
        output_path: Chemin de sortie
        admin_info: Dict avec client_name, project_name, start_date, etc.
        sales_bonus: List de beneficiaries
        consultants: List de consultants
    
    Returns:
        Tuple (success, message)
    """
    builder = NCFBuilderXML(template_path, output_path)
    
    try:
        # Configurer les infos
        builder.set_admin_info(admin_info)
        
        if sales_bonus:
            builder.set_sales_bonus(sales_bonus)
        
        if consultants:
            for consultant in consultants:
                builder.add_consultant(
                    name=consultant['name'],
                    grade=consultant['grade'],
                    days=consultant['days'],
                    tj=consultant['tj'],
                    office=consultant.get('office', 'Paris'),
                    work_type=consultant.get('work_type', 'In the office')
                )
        
        # Construire
        success, msg = builder.build()
        
        return success, msg
    
    finally:
        builder.cleanup()
