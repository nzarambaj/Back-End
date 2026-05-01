#!/usr/bin/env python3
"""
Quick Server Status Check
Verify both frontend and backend servers are running
"""

import requests
from datetime import datetime

def check_servers():
    print(" SERVER STATUS CHECK")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Check frontend (port 3000)
    print("\n FRONTEND SERVER (Port 3000):")
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("   Status: RUNNING")
            print("   Home: ACCESSIBLE")
        else:
            print(f"   Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"   Status: ERROR - {e}")
    
    # Check dashboard
    print("\n DASHBOARD (Port 3000):")
    try:
        response = requests.get('http://localhost:3000/dashboard', timeout=5)
        if response.status_code == 200:
            print("   Status: ACCESSIBLE")
        else:
            print(f"   Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"   Status: ERROR - {e}")
    
    # Check login page
    print("\n LOGIN PAGE (Port 3000):")
    try:
        response = requests.get('http://localhost:3000/login', timeout=5)
        if response.status_code == 200:
            print("   Status: ACCESSIBLE")
        else:
            print(f"   Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"   Status: ERROR - {e}")
    
    # Check backend (port 5000)
    print("\n BACKEND SERVER (Port 5000):")
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   Status: RUNNING")
            print("   Database:", data.get('database', 'Unknown'))
        else:
            print(f"   Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"   Status: ERROR - {e}")
    
    # Check backend login
    print("\n BACKEND LOGIN (Port 5000):")
    try:
        auth_data = {"email": "test@example.com", "password": "test123"}
        response = requests.post('http://localhost:5000/api/auth/login', 
                              json=auth_data, timeout=5)
        if response.status_code == 200:
            print("   Status: WORKING")
        else:
            print(f"   Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"   Status: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(" ACCESS INSTRUCTIONS:")
    print("1. Open browser: http://localhost:3000/login")
    print("2. Login with: test@example.com / test123")
    print("3. Access dashboard: http://localhost:3000/dashboard")
    print("=" * 50)

if __name__ == "__main__":
    check_servers()
