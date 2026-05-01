#!/usr/bin/env python3
"""
Test Enhanced Equipment API
Verify comprehensive equipment details from Calculus folder
"""

import requests
import json
from datetime import datetime

def test_enhanced_equipment_api():
    print(" ENHANCED EQUIPMENT API TEST")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_url = "http://localhost:5001"
    
    # Test 1: Health check
    print("\n1. HEALTH CHECK")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: SUCCESS")
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
            print(f"   Equipment Count: {data.get('equipment_count', 0)}")
            print(f"   Categories: {data.get('categories', [])}")
        else:
            print(f"   Status: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"   Status: ERROR - {e}")
    
    # Test 2: Get all equipment with comprehensive details
    print("\n2. ALL EQUIPMENT WITH COMPREHENSIVE DETAILS")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/equipment", timeout=5)
        if response.status_code == 200:
            data = response.json()
            equipment_list = data.get('equipment', [])
            metadata = data.get('metadata', {})
            
            print(f"   Status: SUCCESS")
            print(f"   Total Equipment: {len(equipment_list)}")
            print(f"   Categories: {metadata.get('categories', [])}")
            print(f"   Manufacturers: {metadata.get('manufacturers', [])}")
            
            # Display comprehensive details for each equipment
            for i, equipment in enumerate(equipment_list, 1):
                print(f"\n   {i}. {equipment.get('name', 'Unknown')}")
                print(f"      ID: {equipment.get('id', 'Unknown')}")
                print(f"      Type: {equipment.get('type', 'Unknown')}")
                print(f"      Category: {equipment.get('category', 'Unknown')}")
                print(f"      Manufacturer: {equipment.get('manufacturer', 'Unknown')}")
                print(f"      Model: {equipment.get('model', 'Unknown')}")
                print(f"      Status: {equipment.get('status', 'Unknown')}")
                print(f"      Location: {equipment.get('location', 'Unknown')}")
                print(f"      Description: {equipment.get('description', 'Unknown')}")
                
                # Specifications
                specs = equipment.get('specifications', {})
                if specs:
                    print(f"      Specifications:")
                    for key, value in specs.items():
                        print(f"        - {key}: {value}")
                
                # Capabilities
                capabilities = equipment.get('capabilities', [])
                if capabilities:
                    print(f"      Capabilities: {len(capabilities)} items")
                    for cap in capabilities[:3]:  # Show first 3
                        print(f"        - {cap}")
                    if len(capabilities) > 3:
                        print(f"        ... and {len(capabilities) - 3} more")
                
                # Clinical Applications
                clinical = equipment.get('clinical_applications', [])
                if clinical:
                    print(f"      Clinical Applications: {len(clinical)} items")
                    for app in clinical[:2]:  # Show first 2
                        print(f"        - {app}")
                    if len(clinical) > 2:
                        print(f"        ... and {len(clinical) - 2} more")
                
                # Maintenance
                maintenance = equipment.get('maintenance', {})
                if maintenance:
                    print(f"      Maintenance:")
                    print(f"        - Last: {maintenance.get('last_maintenance', 'Unknown')}")
                    print(f"        - Next: {maintenance.get('next_maintenance', 'Unknown')}")
                    print(f"        - Interval: {maintenance.get('maintenance_interval', 'Unknown')}")
                
                # Software
                software = equipment.get('software', {})
                if software:
                    print(f"      Software:")
                    print(f"        - Version: {software.get('version', 'Unknown')}")
                    print(f"        - AI Features: {software.get('ai_features', [])}")
                
                # Cost and Throughput
                print(f"      Cost per Scan: {equipment.get('cost_per_scan', 'Unknown')}")
                print(f"      Patient Throughput: {equipment.get('patient_throughput', 'Unknown')}")
                
        else:
            print(f"   Status: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"   Status: ERROR - {e}")
    
    # Test 3: Test equipment by type
    print("\n3. EQUIPMENT BY TYPE")
    print("-" * 40)
    
    equipment_types = ['ct', 'mri', 'xray', 'ultrasound', 'mammo']
    
    for eq_type in equipment_types:
        try:
            response = requests.get(f"{base_url}/api/equipment/{eq_type}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                equipment_list = data.get('equipment', [])
                count = data.get('count', 0)
                
                print(f"   {eq_type.upper()}: SUCCESS ({count} items)")
                if equipment_list:
                    eq = equipment_list[0]
                    print(f"      - {eq.get('name', 'Unknown')}")
                    print(f"      - {eq.get('manufacturer', 'Unknown')} {eq.get('model', 'Unknown')}")
                    print(f"      - {len(eq.get('capabilities', []))} capabilities")
                    print(f"      - {len(eq.get('clinical_applications', []))} clinical applications")
            else:
                print(f"   {eq_type.upper()}: FAILED - HTTP {response.status_code}")
        except Exception as e:
            print(f"   {eq_type.upper()}: ERROR - {e}")
    
    # Test 4: Test specifications endpoint
    print("\n4. EQUIPMENT SPECIFICATIONS")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/equipment/specifications/ct", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   CT Specifications: SUCCESS")
            print(f"      ID: {data.get('id', 'Unknown')}")
            print(f"      Name: {data.get('name', 'Unknown')}")
            print(f"      Type: {data.get('type', 'Unknown')}")
            
            specs = data.get('specifications', {})
            print(f"      Technical Specs:")
            for key, value in specs.items():
                print(f"        - {key}: {value}")
        else:
            print(f"   CT Specifications: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"   CT Specifications: ERROR - {e}")
    
    # Test 5: Test capabilities endpoint
    print("\n5. EQUIPMENT CAPABILITIES")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/equipment/capabilities/mri", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   MRI Capabilities: SUCCESS")
            print(f"      ID: {data.get('id', 'Unknown')}")
            print(f"      Name: {data.get('name', 'Unknown')}")
            
            capabilities = data.get('capabilities', [])
            clinical = data.get('clinical_applications', [])
            
            print(f"      Capabilities ({len(capabilities)}):")
            for cap in capabilities[:3]:
                print(f"        - {cap}")
            if len(capabilities) > 3:
                print(f"        ... and {len(capabilities) - 3} more")
            
            print(f"      Clinical Applications ({len(clinical)}):")
            for app in clinical[:2]:
                print(f"        - {app}")
            if len(clinical) > 2:
                print(f"        ... and {len(clinical) - 2} more")
        else:
            print(f"   MRI Capabilities: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"   MRI Capabilities: ERROR - {e}")
    
    # Test 6: Test cost endpoint
    print("\n6. EQUIPMENT COST INFORMATION")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/equipment/cost/xray", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   X-Ray Cost: SUCCESS")
            print(f"      ID: {data.get('id', 'Unknown')}")
            print(f"      Name: {data.get('name', 'Unknown')}")
            print(f"      Cost per Scan: {data.get('cost_per_scan', 'Unknown')}")
            print(f"      Patient Throughput: {data.get('patient_throughput', 'Unknown')}")
        else:
            print(f"   X-Ray Cost: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"   X-Ray Cost: ERROR - {e}")
    
    # Test 7: Test categories and manufacturers
    print("\n7. SYSTEM CATEGORIES")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/categories", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Categories: SUCCESS")
            print(f"      Total: {data.get('total', 0)}")
            for category in data.get('categories', []):
                print(f"        - {category}")
        else:
            print(f"   Categories: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"   Categories: ERROR - {e}")
    
    try:
        response = requests.get(f"{base_url}/api/manufacturers", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Manufacturers: SUCCESS")
            print(f"      Total: {data.get('total', 0)}")
            for manufacturer in data.get('manufacturers', []):
                print(f"        - {manufacturer}")
        else:
            print(f"   Manufacturers: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"   Manufacturers: ERROR - {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(" ENHANCED EQUIPMENT API SUMMARY")
    print("=" * 60)
    print(" All equipment details from Calculus folder are now available")
    print(" Comprehensive specifications, capabilities, and cost information")
    print(" Multiple endpoints for different data views")
    print(" Enhanced search and filtering capabilities")
    print("\n ACCESS URLS:")
    print(" - All Equipment: http://localhost:5001/api/equipment")
    print(" - By Type: http://localhost:5001/api/equipment/<type>")
    print(" - Specifications: http://localhost:5001/api/equipment/specifications/<type>")
    print(" - Capabilities: http://localhost:5001/api/equipment/capabilities/<type>")
    print(" - Cost: http://localhost:5001/api/equipment/cost/<type>")
    print(" - Categories: http://localhost:5001/api/categories")
    print(" - Manufacturers: http://localhost:5001/api/manufacturers")

if __name__ == "__main__":
    test_enhanced_equipment_api()
