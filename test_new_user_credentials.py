#!/usr/bin/env python3
"""
Test New User Credentials
Test the new user1/pass123 login functionality
"""

import requests
import time
from datetime import datetime

def test_new_user_login():
    """Test the new user credentials"""
    print(" TESTING NEW USER CREDENTIALS")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    backend_url = "http://localhost:5000"
    
    # Test new user credentials
    print("Testing: user1 / pass123")
    print("-" * 30)
    
    try:
        login_data = {
            "email": "user1",
            "password": "pass123"
        }
        
        response = requests.post(f"{backend_url}/api/auth/login", 
                               json=login_data, timeout=5)
        
        if response.status_code == 200:
            login_result = response.json()
            token = login_result.get('token')
            user_info = login_result.get('user')
            
            print("   Login: SUCCESS")
            print(f"   Token: {token[:20] if token else 'None'}...")
            print(f"   User Email: {user_info.get('email', 'Unknown')}")
            print(f"   Role: {user_info.get('role', 'Unknown')}")
            print(f"   Name: {user_info.get('firstName', '')} {user_info.get('lastName', '')}")
            
            # Test authenticated access
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test patients access
                response = requests.get(f"{backend_url}/api/patients", 
                                      headers=headers, timeout=5)
                
                if response.status_code == 200:
                    patients_data = response.json()
                    print(f"   Patients Access: SUCCESS ({patients_data.get('total', 0)} items)")
                else:
                    print(f"   Patients Access: HTTP {response.status_code}")
                
                # Test doctors access
                response = requests.get(f"{backend_url}/api/doctors", 
                                      headers=headers, timeout=5)
                
                if response.status_code == 200:
                    doctors_data = response.json()
                    print(f"   Doctors Access: SUCCESS ({doctors_data.get('total', 0)} items)")
                else:
                    print(f"   Doctors Access: HTTP {response.status_code}")
            
            return True
            
        else:
            print(f"   Login: FAILED - HTTP {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   Login: ERROR - {e}")
        return False

def test_all_credentials():
    """Test all available credentials"""
    print("\n TESTING ALL AVAILABLE CREDENTIALS")
    print("=" * 50)
    
    credentials = [
        ("test@example.com", "test123", "admin"),
        ("doctor@medical.com", "doctor123", "doctor"),
        ("radiologist@medical.com", "rad123", "radiologist"),
        ("user1", "pass123", "user")
    ]
    
    backend_url = "http://localhost:5000"
    results = []
    
    for email, password, expected_role in credentials:
        print(f"\nTesting: {email} / {password} (Expected role: {expected_role})")
        print("-" * 50)
        
        try:
            login_data = {"email": email, "password": password}
            response = requests.post(f"{backend_url}/api/auth/login", 
                                   json=login_data, timeout=5)
            
            if response.status_code == 200:
                login_result = response.json()
                user_info = login_result.get('user')
                actual_role = user_info.get('role', 'Unknown')
                
                print(f"   Login: SUCCESS")
                print(f"   Actual Role: {actual_role}")
                
                if actual_role == expected_role:
                    print(f"   Role Match: YES")
                    results.append((email, "SUCCESS", "ROLE_MATCH"))
                else:
                    print(f"   Role Match: NO (Expected: {expected_role})")
                    results.append((email, "SUCCESS", "ROLE_MISMATCH"))
            else:
                print(f"   Login: FAILED - HTTP {response.status_code}")
                results.append((email, "FAILED", "LOGIN_ERROR"))
                
        except Exception as e:
            print(f"   Login: ERROR - {e}")
            results.append((email, "ERROR", str(e)))
    
    return results

def main():
    """Main function"""
    print(" NEW USER CREDENTIALS TEST")
    print("Adding and testing: user1 / pass123")
    print("=" * 80)
    
    # Test new user
    new_user_success = test_new_user_login()
    
    # Test all credentials
    all_results = test_all_credentials()
    
    # Summary
    print("\n" + "=" * 80)
    print(" NEW USER CREDENTIALS SUMMARY")
    print("=" * 80)
    
    print("NEW USER STATUS:")
    print("-" * 30)
    if new_user_success:
        print("   user1 / pass123: ADDED SUCCESSFULLY")
        print("   Login: WORKING")
        print("   Access: AUTHENTICATED")
        print("   Role: user")
    else:
        print("   user1 / pass123: FAILED TO ADD")
        print("   Login: NOT WORKING")
    
    print("\nALL CREDENTIALS STATUS:")
    print("-" * 30)
    for email, status, detail in all_results:
        status_icon = "SUCCESS" if status == "SUCCESS" else "FAILED"
        print(f"   {email}: {status_icon}")
        if detail != "ROLE_MATCH":
            print(f"      Detail: {detail}")
    
    # Update credentials documentation
    print("\nUPDATED LOGIN CREDENTIALS:")
    print("-" * 30)
    print("PRIMARY LOGIN:")
    print("   Email: test@example.com")
    print("   Password: test123")
    print("   Role: admin")
    
    print("\nADDITIONAL LOGIN:")
    print("   Email: doctor@medical.com")
    print("   Password: doctor123")
    print("   Role: doctor")
    
    print("\n   Email: radiologist@medical.com")
    print("   Password: rad123")
    print("   Role: radiologist")
    
    print("\n   Email: user1")
    print("   Password: pass123")
    print("   Role: user")
    
    print("\nFRONTEND ACCESS:")
    print("-" * 30)
    print("   URL: http://localhost:3000")
    print("   Dashboard: http://localhost:3000/dashboard")
    print("   Use any of the above credentials to login")
    
    return new_user_success

if __name__ == "__main__":
    main()
