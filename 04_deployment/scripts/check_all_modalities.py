#!/usr/bin/env python3
"""
Check All Specified Medical Imaging Modalities
Comprehensive status check for US, XR, C ARM/FLUOROSCOPY, CT scan, MR scan, cathlab
"""

import requests
import time
from datetime import datetime

def check_modality_status(modality_code, modality_name):
    """Check status of a specific modality"""
    print(f"\n{modality_name} ({modality_code})")
    print("-" * 50)
    
    results = {}
    
    try:
        # Check modality basic info
        response = requests.get(f"http://localhost:5001/api/modalities/{modality_code}", timeout=5)
        if response.status_code == 200:
            modality_data = response.json()["modality"]
            results["basic_info"] = "✅ AVAILABLE"
            results["modality_name"] = modality_data["modality_name"]
            results["category"] = modality_data["category"]
            results["radiation_type"] = modality_data["radiation_type"]
            results["clinical_applications"] = len(modality_data["clinical_applications"])
            results["advantages"] = len(modality_data["advantages"])
            results["limitations"] = len(modality_data["limitations"])
            results["contraindications"] = len(modality_data["contraindications"])
            results["dose_range"] = modality_data["typical_dose_range"]
            results["acquisition_time"] = modality_data["acquisition_time"]
            
            print(f"   Basic Info: ✅ AVAILABLE")
            print(f"   Full Name: {modality_data['modality_name']}")
            print(f"   Category: {modality_data['category']}")
            print(f"   Radiation: {modality_data['radiation_type']}")
            print(f"   Clinical Applications: {len(modality_data['clinical_applications'])}")
            print(f"   Dose Range: {modality_data['typical_dose_range']}")
            print(f"   Acquisition Time: {modality_data['acquisition_time']}")
        else:
            results["basic_info"] = f"❌ HTTP {response.status_code}"
            print(f"   Basic Info: ❌ NOT FOUND (HTTP {response.status_code})")
            return results
        
        # Check protocols
        response = requests.get(f"http://localhost:5001/api/protocols/modality/{modality_code}", timeout=5)
        if response.status_code == 200:
            protocols_data = response.json()
            results["protocols"] = "✅ AVAILABLE"
            results["protocol_count"] = protocols_data["total"]
            print(f"   Protocols: ✅ AVAILABLE ({protocols_data['total']} protocols)")
            
            if protocols_data["total"] > 0:
                first_protocol = protocols_data["protocols"][0]
                print(f"   First Protocol: {first_protocol['protocol_name']}")
                print(f"   Contrast Required: {first_protocol['contrast_required']}")
                print(f"   Estimated Dose: {first_protocol['estimated_dose']}")
        else:
            results["protocols"] = f"❌ HTTP {response.status_code}"
            print(f"   Protocols: ❌ NOT FOUND (HTTP {response.status_code})")
        
        # Check equipment
        response = requests.get(f"http://localhost:5001/api/equipment/modality/{modality_code}", timeout=5)
        if response.status_code == 200:
            equipment_data = response.json()
            results["equipment"] = "✅ AVAILABLE"
            results["equipment_count"] = equipment_data["total"]
            print(f"   Equipment: ✅ AVAILABLE ({equipment_data['total']} systems)")
            
            if equipment_data["total"] > 0:
                first_equipment = equipment_data["equipment"][0]
                print(f"   First Equipment: {first_equipment['equipment_name']}")
                print(f"   Manufacturer: {first_equipment['manufacturer']}")
                print(f"   Model: {first_equipment['model']}")
                print(f"   Status: {first_equipment['status']}")
                print(f"   Advanced Features: {len(first_equipment['advanced_features'])}")
        else:
            results["equipment"] = f"❌ HTTP {response.status_code}"
            print(f"   Equipment: ❌ NOT FOUND (HTTP {response.status_code})")
        
        # Check clinical applications
        response = requests.get(f"http://localhost:5001/api/applications/modality/{modality_code}", timeout=5)
        if response.status_code == 200:
            applications_data = response.json()
            results["applications"] = "✅ AVAILABLE"
            print(f"   Clinical Applications: ✅ AVAILABLE")
            print(f"   Applications: {', '.join(applications_data['clinical_applications'][:3])}...")
        else:
            results["applications"] = f"❌ HTTP {response.status_code}"
            print(f"   Clinical Applications: ❌ NOT FOUND (HTTP {response.status_code})")
        
        # Check workflow
        response = requests.get(f"http://localhost:5001/api/workflows/modality/{modality_code}", timeout=5)
        if response.status_code == 200:
            workflow_data = response.json()
            results["workflow"] = "✅ AVAILABLE"
            results["workflow_steps"] = len(workflow_data["workflow_steps"])
            print(f"   Workflow: ✅ AVAILABLE ({len(workflow_data['workflow_steps'])} steps)")
        else:
            results["workflow"] = f"❌ HTTP {response.status_code}"
            print(f"   Workflow: ❌ NOT FOUND (HTTP {response.status_code})")
        
        return results
        
    except Exception as e:
        results["error"] = str(e)
        print(f"   ERROR: {e}")
        return results

def check_c_arm_fluoroscopy():
    """Check C-Arm/Fluoroscopy specifically"""
    print("\nC-ARM/FLUOROSCOPY")
    print("-" * 50)
    
    results = {}
    
    # Check for Fluoroscopy (RF)
    try:
        response = requests.get("http://localhost:5001/api/modalities/RF", timeout=5)
        if response.status_code == 200:
            modality_data = response.json()["modality"]
            results["fluoroscopy"] = "✅ AVAILABLE"
            results["modality_name"] = modality_data["modality_name"]
            print(f"   Fluoroscopy (RF): ✅ AVAILABLE")
            print(f"   Full Name: {modality_data['modality_name']}")
            print(f"   Category: {modality_data['category']}")
            print(f"   Radiation: {modality_data['radiation_type']}")
            print(f"   Clinical Applications: {', '.join(modality_data['clinical_applications'][:3])}...")
            
            # Check for C-Arm specific equipment
            response = requests.get("http://localhost:5001/api/equipment", timeout=5)
            if response.status_code == 200:
                equipment_data = response.json()
                c_arm_equipment = [e for e in equipment_data["equipment"] 
                                  if "c-arm" in e["equipment_name"].lower() or 
                                     "fluoroscopy" in e["equipment_name"].lower()]
                
                if c_arm_equipment:
                    results["c_arm_equipment"] = "✅ AVAILABLE"
                    results["c_arm_count"] = len(c_arm_equipment)
                    print(f"   C-Arm Equipment: ✅ AVAILABLE ({len(c_arm_equipment)} systems)")
                    for equipment in c_arm_equipment:
                        print(f"     - {equipment['equipment_name']} ({equipment['manufacturer']})")
                else:
                    results["c_arm_equipment"] = "⚠️ NO SPECIFIC C-ARM EQUIPMENT"
                    print(f"   C-Arm Equipment: ⚠️ NO SPECIFIC C-ARM EQUIPMENT")
                    print(f"   (General fluoroscopy equipment may be available)")
        else:
            results["fluoroscopy"] = f"❌ HTTP {response.status_code}"
            print(f"   Fluoroscopy (RF): ❌ NOT FOUND (HTTP {response.status_code})")
            
    except Exception as e:
        results["error"] = str(e)
        print(f"   ERROR: {e}")
    
    return results

def check_cathlab():
    """Check CathLab specifically"""
    print("\nCATHLAB")
    print("-" * 50)
    
    results = {}
    
    # CathLab typically uses multiple modalities
    modalities_to_check = ["RF", "CT", "XR", "US"]
    cathlab_modalities = []
    
    for modality in modalities_to_check:
        try:
            response = requests.get(f"http://localhost:5001/api/modalities/{modality}", timeout=5)
            if response.status_code == 200:
                modality_data = response.json()["modality"]
                # Check if this modality is used in cathlab procedures
                cathlab_applications = [app for app in modality_data["clinical_applications"] 
                                     if any(term in app.lower() for term in ["angiography", "cardiac", "vascular", "interventional", "catheter"])]
                
                if cathlab_applications:
                    cathlab_modalities.append({
                        "modality": modality,
                        "name": modality_data["modality_name"],
                        "applications": cathlab_applications
                    })
        except:
            continue
    
    if cathlab_modalities:
        results["cathlab_modalities"] = "✅ AVAILABLE"
        results["modality_count"] = len(cathlab_modalities)
        print(f"   CathLab Modalities: ✅ AVAILABLE ({len(cathlab_modalities)} modalities)")
        
        for mod_info in cathlab_modalities:
            print(f"   - {mod_info['name']} ({mod_info['modality']})")
            print(f"     Applications: {', '.join(mod_info['applications'])}")
        
        # Check for interventional equipment
        try:
            response = requests.get("http://localhost:5001/api/equipment", timeout=5)
            if response.status_code == 200:
                equipment_data = response.json()
                interventional_equipment = [e for e in equipment_data["equipment"] 
                                          if any(term in e["equipment_name"].lower() or 
                                                term in e["model"].lower() or
                                                term in str(e["advanced_features"]).lower()
                                                for term in ["angiography", "interventional", "cathlab", "cardiac", "vascular"])]
                
                if interventional_equipment:
                    results["interventional_equipment"] = "✅ AVAILABLE"
                    results["interventional_count"] = len(interventional_equipment)
                    print(f"   Interventional Equipment: ✅ AVAILABLE ({len(interventional_equipment)} systems)")
                    for equipment in interventional_equipment:
                        print(f"     - {equipment['equipment_name']} ({equipment['manufacturer']})")
                else:
                    results["interventional_equipment"] = "⚠️ NO SPECIFIC INTERVENTIONAL EQUIPMENT"
                    print(f"   Interventional Equipment: ⚠️ NO SPECIFIC INTERVENTIONAL EQUIPMENT")
        except:
            pass
    else:
        results["cathlab_modalities"] = "❌ NO CATHLAB MODALITIES"
        print(f"   CathLab Modalities: ❌ NO CATHLAB MODALITIES FOUND")
    
    return results

def main():
    """Main function"""
    print(" COMPREHENSIVE MODALITY STATUS CHECK")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Check API health first
    try:
        response = requests.get("http://localhost:5001/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ API NOT ACCESSIBLE")
            return
        print("✅ API HEALTH: OK")
    except:
        print("❌ API CONNECTION FAILED")
        return
    
    # Check all specified modalities
    modalities_to_check = [
        ("US", "ULTRASOUND"),
        ("XR", "X-RAY RADIOGRAPHY"),
        ("CT", "CT SCAN"),
        ("MR", "MR SCAN")
    ]
    
    all_results = {}
    
    for modality_code, modality_name in modalities_to_check:
        results = check_modality_status(modality_code, modality_name)
        all_results[modality_code] = results
        time.sleep(0.5)  # Brief pause between requests
    
    # Check C-Arm/Fluoroscopy
    c_arm_results = check_c_arm_fluoroscopy()
    all_results["C_ARM"] = c_arm_results
    
    # Check CathLab
    cathlab_results = check_cathlab()
    all_results["CATHLAB"] = cathlab_results
    
    # Generate summary report
    print("\n" + "=" * 80)
    print(" MODALITY STATUS SUMMARY")
    print("=" * 80)
    
    print("OVERALL STATUS:")
    print("-" * 30)
    
    for modality_code, results in all_results.items():
        if modality_code in ["US", "XR", "CT", "MR"]:
            status = "✅ FULLY AVAILABLE" if (
                results.get("basic_info", "").startswith("✅") and
                results.get("protocols", "").startswith("✅") and
                results.get("equipment", "").startswith("✅")
            ) else "⚠️ PARTIALLY AVAILABLE" if (
                results.get("basic_info", "").startswith("✅")
            ) else "❌ NOT AVAILABLE"
            
            modality_name = next((name for code, name in modalities_to_check if code == modality_code), modality_code)
            print(f"   {modality_name}: {status}")
        elif modality_code == "C_ARM":
            status = "✅ AVAILABLE" if results.get("fluoroscopy", "").startswith("✅") else "❌ NOT AVAILABLE"
            print(f"   C-ARM/FLUOROSCOPY: {status}")
        elif modality_code == "CATHLAB":
            status = "✅ AVAILABLE" if results.get("cathlab_modalities", "").startswith("✅") else "❌ NOT AVAILABLE"
            print(f"   CATHLAB: {status}")
    
    # Equipment summary
    print("\nEQUIPMENT SUMMARY:")
    print("-" * 30)
    try:
        response = requests.get("http://localhost:5001/api/equipment", timeout=5)
        if response.status_code == 200:
            equipment_data = response.json()
            print(f"   Total Equipment: {equipment_data['total']}")
            print(f"   Modalities: {', '.join(equipment_data['modalities'])}")
            print(f"   Manufacturers: {', '.join(equipment_data['manufacturers'])}")
    except:
        print("   Equipment data not accessible")
    
    # Protocols summary
    print("\nPROTOCOLS SUMMARY:")
    print("-" * 30)
    try:
        response = requests.get("http://localhost:5001/api/protocols", timeout=5)
        if response.status_code == 200:
            protocols_data = response.json()
            print(f"   Total Protocols: {protocols_data['total']}")
            print(f"   Modalities: {', '.join(protocols_data['modalities'])}")
    except:
        print("   Protocols data not accessible")
    
    print("\n" + "=" * 80)
    print("DETAILED ACCESS INFORMATION:")
    print("=" * 80)
    print("BASE URL: http://localhost:5001")
    print("ALL MODALITIES: http://localhost:5001/api/modalities")
    print("EQUIPMENT: http://localhost:5001/api/equipment")
    print("PROTOCOLS: http://localhost:5001/api/protocols")
    print("APPLICATIONS: http://localhost:5001/api/applications")
    print("WORKFLOWS: http://localhost:5001/api/workflows")
    print("SAFETY: http://localhost:5001/api/safety")

if __name__ == "__main__":
    main()
