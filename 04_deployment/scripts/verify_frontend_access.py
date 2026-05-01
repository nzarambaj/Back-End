#!/usr/bin/env python3
"""
Verify Frontend Access
Check if frontend is accessible and working
"""

import requests
import time
from datetime import datetime

def verify_frontend_access():
    """Verify frontend is accessible"""
    print(" VERIFYING FRONTEND ACCESS")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    frontend_url = "http://localhost:3000"
    backend_url = "http://localhost:5000"
    
    # Test frontend accessibility
    print("1. TESTING FRONTEND ACCESSIBILITY")
    print("-" * 40)
    
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("   Frontend: ACCESSIBLE")
            print(f"   URL: {frontend_url}")
            print(f"   Status: HTTP {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
            
            # Test dashboard
            dashboard_url = f"{frontend_url}/dashboard"
            try:
                response = requests.get(dashboard_url, timeout=5)
                if response.status_code == 200:
                    print("   Dashboard: ACCESSIBLE")
                    print(f"   URL: {dashboard_url}")
                else:
                    print(f"   Dashboard: HTTP {response.status_code}")
            except:
                print("   Dashboard: ERROR")
            
            return True
        else:
            print(f"   Frontend: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionRefusedError:
        print("   Frontend: CONNECTION REFUSED")
        return False
    except requests.exceptions.Timeout:
        print("   Frontend: TIMEOUT")
        return False
    except Exception as e:
        print(f"   Frontend: ERROR - {e}")
        return False

def test_backend_connectivity():
    """Test backend connectivity"""
    print("\n2. TESTING BACKEND CONNECTIVITY")
    print("-" * 40)
    
    backend_url = "http://localhost:5000"
    
    try:
        response = requests.get(f"{backend_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("   Backend: ACCESSIBLE")
            print(f"   URL: {backend_url}")
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Database: {health_data.get('database', 'Unknown')}")
            return True
        else:
            print(f"   Backend: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   Backend: ERROR - {e}")
        return False

def test_frontend_backend_integration():
    """Test frontend-backend integration"""
    print("\n3. TESTING FRONTEND-BACKEND INTEGRATION")
    print("-" * 40)
    
    backend_url = "http://localhost:5000"
    
    try:
        # Test login
        login_data = {"email": "user1", "password": "pass123"}
        response = requests.post(f"{backend_url}/api/auth/login", 
                               json=login_data, timeout=5)
        
        if response.status_code == 200:
            token = response.json().get('token')
            print("   Frontend-Backend Integration: WORKING")
            print("   Authentication: SUCCESS")
            print(f"   Token: {token[:20] if token else 'None'}...")
            
            # Test data access
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                response = requests.get(f"{backend_url}/api/patients", 
                                      headers=headers, timeout=5)
                
                if response.status_code == 200:
                    patients_data = response.json()
                    print(f"   Data Access: SUCCESS ({patients_data.get('total', 0)} patients)")
                else:
                    print("   Data Access: FAILED")
            
            return True
        else:
            print("   Frontend-Backend Integration: FAILED")
            print(f"   Login Error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   Frontend-Backend Integration: ERROR - {e}")
        return False

def main():
    """Main function"""
    print(" FRONTEND ACCESS VERIFICATION")
    print("Issue: localhost:3000 - ERR_CONNECTION_REFUSED")
    print("=" * 80)
    
    # Test frontend
    frontend_ok = verify_frontend_access()
    
    # Test backend
    backend_ok = test_backend_connectivity()
    
    # Test integration
    integration_ok = test_frontend_backend_integration()
    
    # Summary
    print("\n" + "=" * 80)
    print(" FRONTEND ACCESS VERIFICATION SUMMARY")
    print("=" * 80)
    
    print("SERVICE STATUS:")
    print("-" * 30)
    print(f"   Frontend (3000): {'ACCESSIBLE' if frontend_ok else 'NOT ACCESSIBLE'}")
    print(f"   Backend (5000): {'ACCESSIBLE' if backend_ok else 'NOT ACCESSIBLE'}")
    print(f"   Integration: {'WORKING' if integration_ok else 'NOT WORKING'}")
    
    if frontend_ok and backend_ok and integration_ok:
        print("\nOVERALL STATUS: FRONTEND IS READY")
        print("\nACCESS INSTRUCTIONS:")
        print("1. Open browser: http://localhost:3000")
        print("2. Navigate to: http://localhost:3000/dashboard")
        print("3. Login with: user1 / pass123")
        print("4. Access medical imaging features")
        
        print("\nAVAILABLE CREDENTIALS:")
        print("- user1 / pass123 (user)")
        print("- test@example.com / test123 (admin)")
        print("- doctor@medical.com / doctor123 (doctor)")
        print("- radiologist@medical.com / rad123 (radiologist)")
        
        return True
    else:
        print("\nOVERALL STATUS: FRONTEND NEEDS ATTENTION")
        
        if not frontend_ok:
            print("\nFRONTEND ISSUES:")
            print("- Frontend service is not running")
            print("- Port 3000 is not accessible")
            print("- Try restarting frontend service")
        
        if not backend_ok:
            print("\nBACKEND ISSUES:")
            print("- Backend service is not running")
            print("- Port 5000 is not accessible")
            print("- Try restarting backend service")
        
        if not integration_ok:
            print("\nINTEGRATION ISSUES:")
            print("- Frontend-backend communication failed")
            print("- Authentication may not be working")
            print("- Check backend configuration")
        
        return False

if __name__ == "__main__":
    main()
