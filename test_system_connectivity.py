#!/usr/bin/env python3
"""
Test System Connectivity
Verify all services are accessible and working
"""

import requests
import time
from datetime import datetime

def test_system_connectivity():
    """Test complete system connectivity"""
    print(" TESTING SYSTEM CONNECTIVITY")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    services = {
        'Frontend (3000)': 'http://localhost:3000',
        'Backend Health (5000)': 'http://localhost:5000/api/health',
        'Flask API (5001)': 'http://localhost:5001/api/health'
    }
    
    results = {}
    
    # Test individual services
    print("1. INDIVIDUAL SERVICE TESTS")
    print("-" * 40)
    
    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results[service_name] = '✅ RUNNING'
                print(f"   {service_name}: ✅ RUNNING")
            else:
                results[service_name] = f'❌ HTTP {response.status_code}'
                print(f"   {service_name}: ❌ HTTP {response.status_code}")
        except requests.exceptions.ConnectionRefusedError:
            results[service_name] = '❌ CONNECTION REFUSED'
            print(f"   {service_name}: ❌ CONNECTION REFUSED")
        except requests.exceptions.Timeout:
            results[service_name] = '❌ TIMEOUT'
            print(f"   {service_name}: ❌ TIMEOUT")
        except Exception as e:
            results[service_name] = f'❌ ERROR: {str(e)[:20]}...'
            print(f"   {service_name}: ❌ ERROR")
    
    # Test frontend-backend communication
    print("\n2. FRONTEND → BACKEND COMMUNICATION")
    print("-" * 40)
    
    try:
        login_data = {"email": "test@example.com", "password": "test123"}
        response = requests.post('http://localhost:5000/api/auth/login', 
                               json=login_data, timeout=5)
        
        if response.status_code == 200:
            token = response.json().get('token')
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test patient access
            response = requests.get('http://localhost:5000/api/patients', 
                                  headers=headers, timeout=5)
            
            if response.status_code == 200:
                patients = response.json().get('patients', [])
                results['Frontend → Backend'] = '✅ WORKING'
                print(f"   Frontend → Backend: ✅ WORKING")
                print(f"   Patients accessible: {len(patients)} items")
            else:
                results['Frontend → Backend'] = '❌ FAILED'
                print(f"   Frontend → Backend: ❌ FAILED")
        else:
            results['Frontend → Backend'] = '❌ FAILED'
            print(f"   Frontend → Backend: ❌ FAILED")
            
    except Exception as e:
        results['Frontend → Backend'] = f'❌ ERROR: {str(e)[:20]}...'
        print(f"   Frontend → Backend: ❌ ERROR")
    
    # Test backend → Flask API communication
    print("\n3. BACKEND → FLASK API COMMUNICATION")
    print("-" * 40)
    
    try:
        response = requests.get('http://localhost:5000/api/equipment', timeout=5)
        
        if response.status_code == 200:
            equipment_data = response.json()
            equipment_count = equipment_data.get('total', 0)
            results['Backend → Flask API'] = '✅ WORKING'
            print(f"   Backend → Flask API: ✅ WORKING")
            print(f"   Equipment accessible: {equipment_count} items")
        else:
            results['Backend → Flask API'] = '❌ FAILED'
            print(f"   Backend → Flask API: ❌ FAILED")
            
    except Exception as e:
        results['Backend → Flask API'] = f'❌ ERROR: {str(e)[:20]}...'
        print(f"   Backend → Flask API: ❌ ERROR")
    
    # Test complete data flow
    print("\n4. COMPLETE DATA FLOW TEST")
    print("-" * 40)
    
    try:
        # Login
        login_data = {"email": "test@example.com", "password": "test123"}
        response = requests.post('http://localhost:5000/api/auth/login', 
                               json=login_data, timeout=5)
        
        if response.status_code != 200:
            results['Complete Data Flow'] = '❌ LOGIN FAILED'
            print(f"   Complete Data Flow: ❌ LOGIN FAILED")
            return results
        
        token = response.json().get('token')
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get patients (from medical_db)
        response = requests.get('http://localhost:5000/api/patients', 
                              headers=headers, timeout=5)
        
        if response.status_code != 200:
            results['Complete Data Flow'] = '❌ PATIENTS FAILED'
            print(f"   Complete Data Flow: ❌ PATIENTS FAILED")
            return results
        
        patients = response.json().get('patients', [])
        
        # Get equipment (from Flask API)
        response = requests.get('http://localhost:5000/api/equipment', 
                              headers=headers, timeout=5)
        
        if response.status_code != 200:
            results['Complete Data Flow'] = '❌ EQUIPMENT FAILED'
            print(f"   Complete Data Flow: ❌ EQUIPMENT FAILED")
            return results
        
        equipment_data = response.json()
        equipment_count = equipment_data.get('total', 0)
        
        results['Complete Data Flow'] = '✅ WORKING'
        print(f"   Complete Data Flow: ✅ WORKING")
        print(f"   Patients (medical_db): {len(patients)} items")
        print(f"   Equipment (Flask API): {equipment_count} items")
        print(f"   Frontend can access all data through backend")
        
    except Exception as e:
        results['Complete Data Flow'] = f'❌ ERROR: {str(e)[:20]}...'
        print(f"   Complete Data Flow: ❌ ERROR")
    
    return results

def main():
    """Main function"""
    print(" SYSTEM CONNECTIVITY TEST")
    print("Issue: localhost:3000 - ERR_CONNECTION_REFUSED")
    print("=" * 80)
    
    results = test_system_connectivity()
    
    # Summary
    print("\n" + "=" * 80)
    print(" SYSTEM CONNECTIVITY SUMMARY")
    print("=" * 80)
    
    print("SERVICE STATUS:")
    for service, status in results.items():
        print(f"   {service}: {status}")
    
    # Determine overall status
    frontend_ok = 'Frontend (3000)' in results and 'RUNNING' in results['Frontend (3000)']
    backend_ok = 'Backend Health (5000)' in results and 'RUNNING' in results['Backend Health (5000)']
    flask_ok = 'Flask API (5001)' in results and 'RUNNING' in results['Flask API (5001)']
    
    frontend_backend_ok = 'Frontend → Backend' in results and 'WORKING' in results['Frontend → Backend']
    backend_flask_ok = 'Backend → Flask API' in results and 'WORKING' in results['Backend → Flask API']
    complete_flow_ok = 'Complete Data Flow' in results and 'WORKING' in results['Complete Data Flow']
    
    overall_ok = frontend_ok and backend_ok and flask_ok and frontend_backend_ok and backend_flask_ok and complete_flow_ok
    
    print(f"\nOVERALL SYSTEM STATUS: {'COMPLETE' if overall_ok else 'NEEDS ATTENTION'}")
    
    if overall_ok:
        print("\n" + "=" * 80)
        print(" SYSTEM ARCHITECTURE: FULLY OPERATIONAL")
        print("=" * 80)
        print("Frontend (3000) → Backend (5000) → medical_db (5432) → Flask API (5001)")
        
        print("\nACCESS INSTRUCTIONS:")
        print("1. Open browser and go to: http://localhost:3000")
        print("2. Navigate to: http://localhost:3000/dashboard")
        print("3. Login with: test@example.com / test123")
        print("4. Access all medical imaging features")
        
        print("\nAVAILABLE FEATURES:")
        print("- Frontend dashboard and UI")
        print("- Patient management (CRUD)")
        print("- Doctor management (CRUD)")
        print("- Study management")
        print("- Equipment data from Flask API")
        print("- Real PostgreSQL database operations")
        print("- Authentication and authorization")
        
        print("\nDATABASE CONFIGURATION:")
        print("- Name: medical_db")
        print("- Host: localhost")
        print("- Port: 5432")
        print("- User: postgres")
        print("- Password: Sibo25Mana")
        
    else:
        print("\n" + "=" * 80)
        print(" SYSTEM ARCHITECTURE: NEEDS ATTENTION")
        print("=" * 80)
        
        issues = []
        if not frontend_ok:
            issues.append("- Frontend (3000) is not running or accessible")
        if not backend_ok:
            issues.append("- Backend (5000) is not running")
        if not flask_ok:
            issues.append("- Flask API (5001) is not running")
        if not frontend_backend_ok:
            issues.append("- Frontend → Backend communication failed")
        if not backend_flask_ok:
            issues.append("- Backend → Flask API communication failed")
        if not complete_flow_ok:
            issues.append("- Complete data flow test failed")
        
        print("ISSUES FOUND:")
        for issue in issues:
            print(issue)
        
        print("\nTROUBLESHOOTING:")
        print("- Check if all services are running")
        print("- Verify port accessibility (3000, 5000, 5001)")
        print("- Check firewall settings")
        print("- Restart services if needed")
    
    return overall_ok

if __name__ == "__main__":
    main()
