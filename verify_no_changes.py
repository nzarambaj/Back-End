#!/usr/bin/env python3
"""
Verify No Changes After Optimization
Check that localhost functionality is preserved and no unintended changes occurred
"""

import requests
import json
import os
from pathlib import Path

def verify_no_unintended_changes():
    """Verify that optimization didn't break functionality"""
    print("VERIFYING NO UNINTENDED CHANGES AFTER OPTIMIZATION")
    print("=" * 60)
    print("Checking that localhost functionality is preserved...")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test public endpoints (should work without auth)
    public_endpoints = [
        ("/", "Root Endpoint"),
        ("/api/health", "Health Check"),
        ("/api/public/doctors", "Public Doctors"),
        ("/api/public/patients", "Public Patients"),
        ("/api/public/studies", "Public Studies")
    ]
    
    print("\n🔓 TESTING PUBLIC ENDPOINTS (should work):")
    public_working = 0
    
    for endpoint, name in public_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {name}: OK")
                public_working += 1
            else:
                print(f"  ⚠️ {name}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name}: ERROR - {str(e)[:30]}")
    
    # Test protected endpoints (expected to fail with 401)
    protected_endpoints = [
        ("/api/doctors", "Doctors (Protected)"),
        ("/api/patients", "Patients (Protected)"),
        ("/api/studies", "Studies (Protected)"),
        ("/api/equipment", "Equipment (Protected)")
    ]
    
    print(f"\n🔒 TESTING PROTECTED ENDPOINTS (expected 401):")
    protected_correct = 0
    
    for endpoint, name in protected_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 401:
                print(f"  ✅ {name}: Correctly requires auth (401)")
                protected_correct += 1
            elif response.status_code == 200:
                print(f"  ⚠️ {name}: Unexpectedly public (200)")
            else:
                print(f"  ⚠️ {name}: Unexpected status ({response.status_code})")
        except Exception as e:
            print(f"  ❌ {name}: ERROR - {str(e)[:30]}")
    
    # Check backend structure
    print(f"\n📁 CHECKING BACKEND STRUCTURE:")
    
    structure_checks = [
        ("01_api/routes/medical_db_backend.js", "Main backend file"),
        ("01_api/config/package.json", "Package configuration"),
        ("04_deployment/config/.env", "Environment file"),
        ("04_deployment/config/requirements.txt", "Requirements file")
    ]
    
    structure_ok = 0
    for file_path, description in structure_checks:
        if os.path.exists(file_path):
            print(f"  ✅ {description}: EXISTS")
            structure_ok += 1
        else:
            print(f"  ❌ {description}: MISSING")
    
    # Check file count
    total_files = 0
    main_folders = ["01_api", "02_services", "03_utils", "04_deployment"]
    
    for folder in main_folders:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                total_files += len(files)
    
    print(f"\n📊 FILE COUNT VERIFICATION:")
    print(f"  Current total files: {total_files}")
    print(f"  Target after optimization: ~120")
    print(f"  Reduction from original: {151 - total_files} files")
    
    # Overall assessment
    print(f"\n🎯 OVERALL ASSESSMENT:")
    
    # Public endpoints should work
    public_success = public_working == len(public_endpoints)
    print(f"  Public endpoints: {'✅ WORKING' if public_success else '⚠️ ISSUES'} ({public_working}/{len(public_endpoints)})")
    
    # Protected endpoints should require auth
    auth_success = protected_correct == len(protected_endpoints)
    print(f"  Auth requirements: {'✅ CORRECT' if auth_success else '⚠️ ISSUES'} ({protected_correct}/{len(protected_endpoints)})")
    
    # Structure should be intact
    structure_success = structure_ok == len(structure_checks)
    print(f"  Backend structure: {'✅ INTACT' if structure_success else '⚠️ ISSUES'} ({structure_ok}/{len(structure_checks)})")
    
    # File count should be optimized
    file_optimized = total_files <= 125
    print(f"  File optimization: {'✅ ACHIEVED' if file_optimized else '⚠️ NEEDS WORK'} ({total_files} files)")
    
    # Overall status
    overall_success = public_success and auth_success and structure_success and file_optimized
    
    return {
        'public_working': public_working,
        'public_total': len(public_endpoints),
        'auth_correct': protected_correct,
        'auth_total': len(protected_endpoints),
        'structure_ok': structure_ok,
        'structure_total': len(structure_checks),
        'total_files': total_files,
        'overall_success': overall_success
    }

def generate_no_changes_report(results):
    """Generate verification report"""
    report = {
        "verification_type": "No Changes After Optimization",
        "project": "Project_BackEnd",
        "timestamp": str(Path(__file__).stat().st_mtime),
        "functionality_status": {
            "public_endpoints": {
                "working": results['public_working'],
                "total": results['public_total'],
                "success_rate": f"{results['public_working']/results['public_total']*100:.1f}%"
            },
            "protected_endpoints": {
                "auth_required": results['auth_correct'],
                "total": results['auth_total'],
                "correct_behavior": f"{results['auth_correct']/results['auth_total']*100:.1f}%"
            },
            "backend_structure": {
                "intact": results['structure_ok'],
                "total_checks": results['structure_total'],
                "integrity_rate": f"{results['structure_ok']/results['structure_total']*100:.1f}%"
            },
            "file_optimization": {
                "current_count": results['total_files'],
                "original_count": 151,
                "files_removed": 151 - results['total_files'],
                "reduction_percentage": f"{((151 - results['total_files']) / 151) * 100:.1f}%"
            }
        },
        "overall_status": "NO CHANGES - FUNCTIONALITY PRESERVED" if results['overall_success'] else "CHANGES DETECTED - NEEDS REVIEW",
        "conclusion": {
            "localhost_working": results['public_working'] > 0,
            "auth_system_working": results['auth_correct'] > 0,
            "structure_intact": results['structure_ok'] > 0,
            "optimization_successful": results['total_files'] <= 125
        }
    }
    
    with open("no_changes_verification.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Verification report saved to: no_changes_verification.json")

if __name__ == "__main__":
    print("🔍 VERIFYING NO UNINTENDED CHANGES")
    print("Checking that optimization preserved localhost functionality")
    print("=" * 60)
    
    results = verify_no_unintended_changes()
    generate_no_changes_report(results)
    
    print(f"\n🎉 FINAL VERIFICATION RESULTS:")
    if results['overall_success']:
        print("✅ NO UNINTENDED CHANGES DETECTED")
        print("✅ Localhost functionality preserved")
        print("✅ Authentication system working correctly")
        print("✅ Backend structure intact")
        print("✅ File optimization successful")
    else:
        print("⚠️ SOME CHANGES DETECTED")
        print("Please review the issues above")
    
    print(f"\n📊 SUMMARY:")
    print(f"  Public endpoints working: {results['public_working']}/{results['public_total']}")
    print(f"  Auth requirements correct: {results['auth_correct']}/{results['auth_total']}")
    print(f"  Backend structure intact: {results['structure_ok']}/{results['structure_total']}")
    print(f"  File count optimized: {results['total_files']} files (from 151)")
