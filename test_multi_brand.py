#!/usr/bin/env python3
"""
Test Multi-Brand Medical Imaging API
Comprehensive testing of all manufacturers and modalities
"""

import requests
import time
from datetime import datetime

def test_multi_brand_system():
    """Test the complete multi-brand system"""
    print(" MULTI-BRAND MEDICAL IMAGING SYSTEM TEST")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Test health
    try:
        response = requests.get("http://localhost:5001/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ API HEALTH: OK")
            print(f"   Total Equipment: {health_data['total_equipment']}")
            print(f"   Total Protocols: {health_data['total_protocols']}")
            print(f"   Manufacturers: {', '.join(health_data['manufacturers'])}")
            print(f"   Modalities: {', '.join(health_data['modalities'])}")
        else:
            print("❌ API HEALTH: FAILED")
            return
    except Exception as e:
        print(f"❌ API CONNECTION: FAILED - {e}")
        return
    
    # Test manufacturers
    print("\n MANUFACTURER ANALYSIS")
    print("-" * 40)
    manufacturers = ["GE Healthcare", "Siemens Healthineers", "Philips Healthcare", "Mindray", "Canon Medical Systems", "Fujifilm Healthcare", "Shimadzu"]
    
    for manufacturer in manufacturers:
        try:
            response = requests.get(f"http://localhost:5001/api/equipment/manufacturer/{manufacturer}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   {manufacturer}: ✅ {data['total']} systems")
                print(f"      Modalities: {', '.join(data['modalities'])}")
            else:
                print(f"   {manufacturer}: ❌ HTTP {response.status_code}")
        except:
            print(f"   {manufacturer}: ❌ ERROR")
    
    # Test modalities
    print("\n MODALITY ANALYSIS")
    print("-" * 40)
    modalities = ["US", "XR", "CT", "MRI", "RF"]
    
    for modality in modalities:
        try:
            # Test equipment
            eq_response = requests.get(f"http://localhost:5001/api/equipment/modality/{modality}", timeout=5)
            if eq_response.status_code == 200:
                eq_data = eq_response.json()
                print(f"   {modality.upper()}: ✅ {eq_data['total']} systems")
                print(f"      Manufacturers: {', '.join(eq_data['manufacturers'])}")
                
                # Test protocols
                proto_response = requests.get(f"http://localhost:5001/api/protocols/modality/{modality}", timeout=5)
                if proto_response.status_code == 200:
                    proto_data = proto_response.json()
                    print(f"      Protocols: {proto_data['total']} protocols")
                    print(f"      Protocol Manufacturers: {', '.join(proto_data['manufacturers'])}")
                else:
                    print(f"      Protocols: ❌ HTTP {proto_response.status_code}")
            else:
                print(f"   {modality.upper()}: ❌ HTTP {eq_response.status_code}")
        except:
            print(f"   {modality.upper()}: ❌ ERROR")
    
    # Test specific equipment examples
    print("\n SPECIFIC EQUIPMENT EXAMPLES")
    print("-" * 40)
    
    examples = [
        ("GE Healthcare", "CT"),
        ("Siemens Healthineers", "MRI"),
        ("Philips Healthcare", "US"),
        ("Mindray", "XR"),
        ("Canon Medical Systems", "CT")
    ]
    
    for manufacturer, modality in examples:
        try:
            response = requests.get(f"http://localhost:5001/api/equipment/manufacturer/{manufacturer}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                modality_equipment = [e for e in data["equipment"] if e["modality_code"] == modality]
                if modality_equipment:
                    equipment = modality_equipment[0]
                    print(f"   {manufacturer} {modality.upper()}:")
                    print(f"      Model: {equipment['model']}")
                    print(f"      Location: {equipment['location']}")
                    print(f"      Advanced Features: {len(equipment['advanced_features'])}")
                    print(f"      Status: {equipment['status']}")
        except:
            print(f"   {manufacturer} {modality.upper()}: ❌ ERROR")
    
    # Test protocols
    print("\n PROTOCOL ANALYSIS")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:5001/api/protocols", timeout=5)
        if response.status_code == 200:
            protocols_data = response.json()
            print(f"   Total Protocols: {protocols_data['total']}")
            print(f"   Manufacturers: {', '.join(protocols_data['manufacturers'])}")
            print(f"   Modalities: {', '.join(protocols_data['modalities'])}")
            
            # Show some protocol examples
            for protocol in protocols_data["protocols"][:3]:
                print(f"   Example: {protocol['protocol_name']}")
                print(f"      Manufacturer: {protocol['manufacturer']}")
                print(f"      Modality: {protocol['modality_code']}")
                print(f"      Contrast Required: {protocol['contrast_required']}")
                print(f"      Equipment: {', '.join(protocol['equipment_compatibility'])}")
        else:
            print(f"   Protocols: ❌ HTTP {response.status_code}")
    except:
        print("   Protocols: ❌ ERROR")
    
    # Test manufacturer comparison
    print("\n MANUFACTURER COMPARISON")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:5001/api/manufacturers/compare?manufacturers=GE Healthcare,Siemens Healthineers,Philips Healthcare", timeout=5)
        if response.status_code == 200:
            comparison_data = response.json()
            print("   GE vs Siemens vs Philips:")
            for manufacturer, data in comparison_data["comparison"].items():
                print(f"      {manufacturer}:")
                print(f"         Equipment: {data['equipment_count']}")
                print(f"         Protocols: {data['protocol_count']}")
                print(f"         Modalities: {', '.join(data['modalities'])}")
        else:
            print(f"   Comparison: ❌ HTTP {response.status_code}")
    except:
        print("   Comparison: ❌ ERROR")
    
    # Test market analysis
    print("\n MARKET ANALYSIS")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:5001/api/manufacturers/market_share", timeout=5)
        if response.status_code == 200:
            market_data = response.json()
            print("   Market Share:")
            for manufacturer, data in market_data["market_share"].items():
                print(f"      {manufacturer}: {data['market_share_percentage']}% ({data['equipment_count']} systems)")
        else:
            print(f"   Market Share: ❌ HTTP {response.status_code}")
    except:
        print("   Market Share: ❌ ERROR")
    
    # Summary
    print("\n" + "=" * 80)
    print(" MULTI-BRAND SYSTEM SUMMARY")
    print("=" * 80)
    
    try:
        equipment_response = requests.get("http://localhost:5001/api/equipment", timeout=5)
        protocols_response = requests.get("http://localhost:5001/api/protocols", timeout=5)
        
        if equipment_response.status_code == 200 and protocols_response.status_code == 200:
            equipment_data = equipment_response.json()
            protocols_data = protocols_response.json()
            
            print("✅ SYSTEM STATUS: FULLY OPERATIONAL")
            print(f"   Total Equipment: {equipment_data['total']}")
            print(f"   Total Manufacturers: {len(equipment_data['manufacturers'])}")
            print(f"   Total Modalities: {len(equipment_data['modalities'])}")
            print(f"   Total Protocols: {protocols_data['total']}")
            
            print("\n🏥 MODALITY COVERAGE:")
            for modality in equipment_data['modalities']:
                mod_eq = [e for e in equipment_data['equipment'] if e['modality_code'] == modality]
                mod_manufacturers = list(set(e['manufacturer'] for e in mod_eq))
                print(f"   {modality}: {len(mod_eq)} systems, {len(mod_manufacturers)} manufacturers")
            
            print("\n🏭 MANUFACTURER COVERAGE:")
            for manufacturer in equipment_data['manufacturers']:
                man_eq = [e for e in equipment_data['equipment'] if e['manufacturer'] == manufacturer]
                man_modalities = list(set(e['modality_code'] for e in man_eq))
                print(f"   {manufacturer}: {len(man_eq)} systems, {len(man_modalities)} modalities")
            
            print("\n🌐 ACCESS URLS:")
            print("   Base URL: http://localhost:5001")
            print("   All Equipment: http://localhost:5001/api/equipment")
            print("   All Protocols: http://localhost:5001/api/protocols")
            print("   Manufacturers: http://localhost:5001/api/manufacturers")
            print("   GE Equipment: http://localhost:5001/api/equipment/manufacturer/GE")
            print("   Siemens Equipment: http://localhost:5001/api/equipment/manufacturer/Siemens")
            print("   Philips Equipment: http://localhost:5001/api/equipment/manufacturer/Philips")
            print("   Mindray Equipment: http://localhost:5001/api/equipment/manufacturer/Mindray")
            
        else:
            print("❌ SYSTEM STATUS: PARTIAL FAILURE")
    except:
        print("❌ SYSTEM STATUS: FAILED")

if __name__ == "__main__":
    test_multi_brand_system()
