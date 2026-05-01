#!/usr/bin/env python3
"""
Check DICOM Service Status
Quick check of DICOM backend service
"""

import requests
from datetime import datetime

def check_dicom_service():
    print(" DICOM SERVICE STATUS CHECK")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Check health endpoint
    print("\n HEALTH ENDPOINT:")
    try:
        response = requests.get('http://localhost:5001/api/dicom/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   Status: RUNNING")
            print("   Service:", data.get('service', 'Unknown'))
            print("   Version:", data.get('version', 'Unknown'))
        else:
            print(f"   Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"   Status: ERROR - {e}")
    
    # Check login endpoint
    print("\n LOGIN ENDPOINT:")
    try:
        auth_data = {"email": "test@example.com", "password": "test123"}
        response = requests.post('http://localhost:5001/api/auth/login', 
                              json=auth_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   Status: WORKING")
            print("   Token:", data.get('token', '')[:20] + "...")
        else:
            print(f"   Status: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Status: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(" DICOM BACKEND STATUS:")
    print(" - Health Check: Check if service is running")
    print(" - Authentication: Check if login endpoint works")
    print(" - Port: 5001 (separate from main backend)")
    print("=" * 50)

if __name__ == "__main__":
    check_dicom_service()
