#!/usr/bin/env python3
"""
Quick Troubleshoot
Fast check of system status to identify login issues
"""

import requests
import time
from datetime import datetime

def quick_system_check():
    """Quick system status check"""
    print(" QUICK SYSTEM TROUBLESHOOT")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    issues = []
    
    # Check 1: Frontend accessibility
    print("1. FRONTEND ACCESSIBILITY")
    print("-" * 30)
    try:
        response = requests.get("http://localhost:3000", timeout=3)
        if response.status_code == 200:
            print("   ✅ Frontend: ACCESSIBLE")
        else:
            print(f"   ❌ Frontend: HTTP {response.status_code}")
            issues.append("Frontend not responding correctly")
    except:
        print("   ❌ Frontend: NOT ACCESSIBLE")
        issues.append("Frontend service not running")
    
    # Check 2: Backend accessibility
    print("\n2. BACKEND ACCESSIBILITY")
    print("-" * 30)
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=3)
        if response.status_code == 200:
            print("   ✅ Backend: ACCESSIBLE")
        else:
            print(f"   ❌ Backend: HTTP {response.status_code}")
            issues.append("Backend not responding correctly")
    except:
        print("   ❌ Backend: NOT ACCESSIBLE")
        issues.append("Backend service not running")
    
    # Check 3: Login test
    print("\n3. LOGIN TEST")
    print("-" * 30)
    try:
        login_data = {"email": "user1", "password": "pass123"}
        response = requests.post("http://localhost:5000/api/auth/login", 
                               json=login_data, timeout=3)
        if response.status_code == 200:
            print("   ✅ Login: WORKING")
            token = response.json().get('token')
            print(f"   Token: {token[:20] if token else 'None'}...")
        else:
            print(f"   ❌ Login: HTTP {response.status_code}")
            issues.append("Login API not working")
    except:
        print("   ❌ Login: ERROR")
        issues.append("Login request failed")
    
    # Check 4: Data access
    print("\n4. DATA ACCESS")
    print("-" * 30)
    try:
        login_data = {"email": "user1", "password": "pass123"}
        response = requests.post("http://localhost:5000/api/auth/login", 
                               json=login_data, timeout=3)
        if response.status_code == 200:
            token = response.json().get('token')
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get("http://localhost:5000/api/patients", 
                                  headers=headers, timeout=3)
            if response.status_code == 200:
                print("   ✅ Data Access: WORKING")
            else:
                print(f"   ❌ Data Access: HTTP {response.status_code}")
                issues.append("Data access not working")
        else:
            print("   ❌ Data Access: LOGIN FAILED")
            issues.append("Cannot test data access - login failed")
    except:
        print("   ❌ Data Access: ERROR")
        issues.append("Data access test failed")
    
    # Summary
    print("\n" + "=" * 50)
    print("TROUBLESHOOT SUMMARY")
    print("=" * 50)
    
    if issues:
        print("ISSUES FOUND:")
        print("-" * 20)
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        
        print("\nQUICK FIXES:")
        print("-" * 20)
        if "Frontend" in str(issues):
            print("   • Restart frontend: npm run dev (in Project_FrontEnd)")
        if "Backend" in str(issues):
            print("   • Restart backend: node medical_db_backend.js")
        if "Login" in str(issues):
            print("   • Check backend authentication")
            print("   • Try other credentials: test@example.com / test123")
        
        print("\nALTERNATIVE LOGIN:")
        print("-" * 20)
        print("   If user1/pass123 fails, try:")
        print("   • test@example.com / test123 (admin)")
        print("   • doctor@medical.com / doctor123")
        
        return False
    else:
        print("✅ NO ISSUES FOUND")
        print("\nEVERYTHING IS WORKING!")
        print("Try these steps:")
        print("1. Open browser: http://localhost:3000")
        print("2. Go to: http://localhost:3000/dashboard")
        print("3. Login: user1 / pass123")
        print("4. If still fails, try: test@example.com / test123")
        
        return True

def main():
    """Main function"""
    print("WHY ISN'T IT WORKING? - QUICK DIAGNOSIS")
    print("=" * 80)
    
    system_ok = quick_system_check()
    
    if not system_ok:
        print("\n" + "=" * 80)
        print("IMMEDIATE ACTIONS TO TRY:")
        print("=" * 80)
        print("1. REFRESH your browser page")
        print("2. CHECK spelling: user1 / pass123")
        print("3. TRY alternative login: test@example.com / test123")
        print("4. CLEAR browser cache and cookies")
        print("5. CHECK console for JavaScript errors")
        print("6. VERIFY you're on http://localhost:3000 (not https)")
        
        print("\nIf still not working:")
        print("• Restart frontend: Stop Node.js, run 'npm run dev'")
        print("• Restart backend: Stop Node.js, run 'node medical_db_backend.js'")
        print("• Check if ports 3000 and 5000 are available")

if __name__ == "__main__":
    main()
