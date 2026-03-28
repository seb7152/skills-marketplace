#!/usr/bin/env python3
# Test Suite - NFC Creator Skill
# ==============================

import sys
import os
import tempfile
from pathlib import Path

# Ajouter le répertoire scripts au path
sys.path.insert(0, '/mnt/skills/user/nfc-creator/scripts')

# Import des modules
from nfc_builder_xml import NCFBuilderXML, create_nfc
from nfc_config import (
    NFC_TEMPLATE_PATH, NFC_OUTPUT_DIR, CELL_MAPPING,
    get_output_filename, DEFAULT_CONFIG, init_skill
)
from nfc_templates import DEFAULT_ADMIN_INFO, AVAILABLE_GRADES


def test_imports():
    """Test 1: Vérifier les imports"""
    print("\n" + "=" * 70)
    print("TEST 1: Imports")
    print("=" * 70)
    
    try:
        print("✅ nfc_builder_xml imported")
        print("✅ nfc_config imported")
        print("✅ nfc_templates imported")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_config():
    """Test 2: Vérifier la configuration"""
    print("\n" + "=" * 70)
    print("TEST 2: Configuration & Paths")
    print("=" * 70)
    
    try:
        print(f"Template path: {NFC_TEMPLATE_PATH}")
        if not os.path.exists(NFC_TEMPLATE_PATH):
            print(f"❌ Template not found at {NFC_TEMPLATE_PATH}")
            return False
        print("✅ Template found")
        
        print(f"Output dir: {NFC_OUTPUT_DIR}")
        Path(NFC_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        print("✅ Output directory ready")
        
        # Check cell mapping
        print(f"\nCell mappings loaded:")
        print(f"  • ADMIN_INFO: {len(CELL_MAPPING['ADMIN_INFO'])} fields")
        print(f"  • SALES_BONUS: {len(CELL_MAPPING['SALES_BONUS'])} fields")
        print(f"  • BUDGET: {len(CELL_MAPPING['BUDGET'])} fields")
        print("✅ Cell mappings valid")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False


def test_filename_generation():
    """Test 3: Génération de noms de fichier"""
    print("\n" + "=" * 70)
    print("TEST 3: Filename Generation")
    print("=" * 70)
    
    try:
        filename1 = get_output_filename("Acme Corporation")
        print(f"Filename 1: {filename1}")
        assert filename1.endswith('.xlsm'), "Must end with .xlsm"
        assert "Acme" in filename1, "Must contain client name"
        print("✅ Filename 1 valid")
        
        filename2 = get_output_filename("TechLabs Inc.", "25-03")
        print(f"Filename 2: {filename2}")
        assert "25-03" in filename2, "Must contain year-month"
        print("✅ Filename 2 valid")
        
        return True
    except Exception as e:
        print(f"❌ Filename test failed: {e}")
        return False


def test_nfc_builder():
    """Test 4: NFC Builder - Modifie le template"""
    print("\n" + "=" * 70)
    print("TEST 4: NFC Builder (XML modification)")
    print("=" * 70)
    
    try:
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix='.xlsm', delete=False) as tmp:
            output_path = tmp.name
        
        print(f"Creating test NFC: {output_path}")
        
        # Données de test
        admin_info = {
            'client_name': 'Test Client ACME',
            'project_name': 'Digital Transformation',
            'start_date': '01/04/2026',
            'sales_name': 'Sébastien Grandperret',
            'sales_email': 'sebastien.grandperret@sia-partners.com',
            'pm_name': 'Sébastien Grandperret',
            'pm_email': 'sebastien.grandperret@sia-partners.com',
            'deal_id': 'HUB-123456',
            'client_contact': 'John Manager',
            'accounting_contact': 'accounts@acme.com'
        }
        
        sales_bonus = [
            {
                'email_orig': 'sebastien.grandperret@sia-partners.com',
                'percent_orig': 0.01,
                'email_managed': 'paul.dubois@sia-partners.com',
                'percent_managed': 0.005
            },
            {
                'email_orig': 'paul.dubois@sia-partners.com',
                'percent_orig': 0.005,
                'email_managed': 'sebastien.grandperret@sia-partners.com',
                'percent_managed': 0.01
            }
        ]
        
        consultants = [
            {
                'name': 'Sophie Martin',
                'grade': 'Senior Consultant',
                'days': 65,
                'tj': 950,
                'office': 'Paris',
                'work_type': 'In the office',
                'relation_type': 'Local / XM'
            },
            {
                'name': 'Marc Dupont',
                'grade': 'Consultant',
                'days': 50,
                'tj': 800,
                'office': 'Paris',
                'work_type': 'In the office',
                'relation_type': 'Local / XM'
            }
        ]
        
        # Créer la NFC
        success, message = create_nfc(
            template_path=NFC_TEMPLATE_PATH,
            output_path=output_path,
            admin_info=admin_info,
            sales_bonus=sales_bonus,
            consultants=consultants
        )
        
        print(f"Build result: {message}")
        
        if not success:
            print(f"❌ Build failed: {message}")
            return False
        
        # Vérifier le fichier
        if not os.path.exists(output_path):
            print(f"❌ Output file not created")
            return False
        
        file_size = os.path.getsize(output_path)
        print(f"✅ NFC created: {file_size:,} bytes")
        
        # Nettoyer
        os.remove(output_path)
        
        return True
    
    except Exception as e:
        print(f"❌ Builder test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_grades():
    """Test 5: Grades disponibles"""
    print("\n" + "=" * 70)
    print("TEST 5: Available Grades")
    print("=" * 70)
    
    try:
        grades = list(AVAILABLE_GRADES.keys())
        print(f"Total grades: {len(grades)}")
        
        for i, grade in enumerate(grades, 1):
            code = AVAILABLE_GRADES[grade]
            print(f"  {i}. {grade:25} ({code})")
        
        expected_grades = [
            "Senior Manager", "Manager", "Senior Consultant",
            "Consultant", "Junior", "SME Director",
            "Engagement Director", "Managing Director", "Senior Industry Expert"
        ]
        
        for grade in expected_grades:
            if grade not in grades:
                print(f"❌ Missing grade: {grade}")
                return False
        
        print("✅ All expected grades present")
        return True
    
    except Exception as e:
        print(f"❌ Grades test failed: {e}")
        return False


def main():
    """Exécute tous les tests"""
    print("\n" + "=" * 70)
    print("🧪 NFC CREATOR - TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Imports", test_imports),
        ("Config", test_config),
        ("Filename Generation", test_filename_generation),
        ("NFC Builder", test_nfc_builder),
        ("Grades", test_grades),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
