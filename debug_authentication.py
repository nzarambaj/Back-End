#!/usr/bin/env python3
"""
Debug Authentication System
Check why user1/pass123 credentials are not working
"""

import requests
import time
from datetime import datetime

def test_authentication_debug():
    """Debug authentication system"""
    print(" DEBUGGING AUTHENTICATION SYSTEM")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    backend_url = "http://localhost:5000"
    
    # Test all credentials
    credentials = [
        ("test@example.com", "test123", "admin"),
        ("doctor@medical.com", "doctor123", "doctor"),
        ("radiologist@medical.com", "rad123", "radiologist"),
        ("user1", "pass123", "user")
    ]
    
    print("TESTING ALL CREDENTIALS:")
    print("-" * 40)
    
    working_credentials = []
    failed_credentials = []
    
    for email, password, expected_role in credentials:
        print(f"\nTesting: {email} / {password}")
        print("-" * 30)
        
        try:
            login_data = {"email": email, "password": password}
            response = requests.post(f"{backend_url}/api/auth/login", 
                                   json=login_data, timeout=5)
            
            if response.status_code == 200:
                login_result = response.json()
                user_info = login_result.get('user')
                actual_role = user_info.get('role', 'Unknown')
                
                print(f"   Login: SUCCESS")
                print(f"   Expected Role: {expected_role}")
                print(f"   Actual Role: {actual_role}")
                print(f"   Token: {login_result.get('token', 'None')[:20]}...")
                
                working_credentials.append((email, password, actual_role))
                
                if actual_role != expected_role:
                    print(f"   WARNING: Role mismatch!")
            else:
                print(f"   Login: FAILED - HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                failed_credentials.append((email, password, response.status_code))
                
        except Exception as e:
            print(f"   Login: ERROR - {e}")
            failed_credentials.append((email, password, str(e)))
    
    # Summary
    print("\n" + "=" * 60)
    print("AUTHENTICATION DEBUG SUMMARY")
    print("=" * 60)
    
    print("WORKING CREDENTIALS:")
    print("-" * 30)
    if working_credentials:
        for email, password, role in working_credentials:
            print(f"   {email} / {password} - Role: {role}")
    else:
        print("   No working credentials found!")
    
    print("\nFAILED CREDENTIALS:")
    print("-" * 30)
    if failed_credentials:
        for email, password, error in failed_credentials:
            print(f"   {email} / {password} - Error: {error}")
    else:
        print("   All credentials working!")
    
    # Check backend health
    print("\nBACKEND HEALTH CHECK:")
    print("-" * 30)
    try:
        response = requests.get(f"{backend_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Backend Status: RUNNING")
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Database: {health_data.get('database', 'Unknown')}")
        else:
            print(f"   Backend Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"   Backend Status: ERROR - {e}")
    
    return working_credentials, failed_credentials

def check_backend_code():
    """Check if user1 is in backend code"""
    print("\nCHECKING BACKEND CODE:")
    print("-" * 30)
    
    try:
        with open(r"C:\Users\TTR\Documents\Project_BackEnd\medical_db_backend.js", "r") as f:
            content = f.read()
        
        if "user1" in content and "pass123" in content:
            print("   user1/pass123 found in backend code")
            return True
        else:
            print("   user1/pass123 NOT found in backend code")
            return False
    except Exception as e:
        print(f"   Error reading backend code: {e}")
        return False

def fix_authentication():
    """Fix authentication if needed"""
    print("\nFIXING AUTHENTICATION:")
    print("-" * 30)
    
    # Read current backend file
    try:
        with open(r"C:\Users\TTR\Documents\Project_BackEnd\medical_db_backend.js", "r") as f:
            content = f.read()
        
        # Check if user1 is already there
        if "user1" in content and "pass123" in content:
            print("   user1/pass123 already in backend code")
            print("   Issue might be backend not restarted")
            return False
        
        # Find the testUsers array
        test_users_start = content.find("const testUsers = [")
        if test_users_start == -1:
            print("   testUsers array not found")
            return False
        
        # Find the end of the array
        test_users_end = content.find("];", test_users_start)
        if test_users_end == -1:
            print("   testUsers array end not found")
            return False
        
        # Extract current array
        current_array = content[test_users_start:test_users_end + 2]
        print(f"   Current testUsers array found")
        
        # Add user1 to the array
        new_user_line = "      { email: 'user1', password: 'pass123', role: 'user', firstName: 'User', lastName: 'One' }"
        
        # Find the last user entry
        last_user_pos = current_array.rfind("      {")
        if last_user_pos == -1:
            print("   Could not find last user entry")
            return False
        
        # Insert new user before the closing ]
        new_array = current_array[:last_user_pos] + new_user_line + ",\n    ]"
        
        # Replace in content
        new_content = content[:test_users_start] + new_array + content[test_users_end + 2:]
        
        # Write back
        with open(r"C:\Users\TTR\Documents\Project_BackEnd\medical_db_backend.js", "w") as f:
            f.write(new_content)
        
        print("   user1/pass123 added to backend code")
        return True
        
    except Exception as e:
        print(f"   Error fixing authentication: {e}")
        return False

def main():
    """Main function"""
    print(" AUTHENTICATION DEBUG AND FIX")
    print("Issue: Added password user1/pass123 not working")
    print("=" * 80)
    
    # Test current authentication
    working, failed = test_authentication_debug()
    
    # Check backend code
    user1_in_code = check_backend_code()
    
    # If user1 not working, try to fix
    if not any(email == "user1" for email, _, _ in working):
        print("\nATTEMPTING TO FIX AUTHENTICATION:")
        print("-" * 40)
        
        if fix_authentication():
            print("   Backend code updated")
            print("   Please restart backend service")
            
            # Instructions for manual restart
            print("\nMANUAL RESTART INSTRUCTIONS:")
            print("1. Stop current backend: taskkill /f /im node.exe")
            print("2. Start backend: node medical_db_backend.js")
            print("3. Test login again")
        else:
            print("   Could not fix authentication automatically")
    else:
        print("\nuser1/pass123 is working correctly!")
    
    # Provide working credentials
    print("\n" + "=" * 80)
    print("WORKING CREDENTIALS SUMMARY")
    print("=" * 80)
    
    if working:
        print("USE THESE CREDENTIALS TO LOGIN:")
        print("-" * 40)
        for email, password, role in working:
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   Role: {role}")
            print()
        
        print("FRONTEND ACCESS:")
        print("-" * 40)
        print("   URL: http://localhost:3000")
        print("   Dashboard: http://localhost:3000/dashboard")
        print("   Use any of the above credentials")
    else:
        print("NO WORKING CREDENTIALS FOUND!")
        print("Please check backend service and restart if needed")

if __name__ == "__main__":
    main()
