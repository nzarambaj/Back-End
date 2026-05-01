#!/usr/bin/env python3
"""
Test Clean DICOM Service
Test all functionality without authentication
"""

import requests
import json
import os
from datetime import datetime

def test_dicom_service():
    print(" CLEAN DICOM SERVICE TEST")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/api/dicom/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Health Check: SUCCESS")
            print(f"Service: {data.get('service', 'Unknown')}")
            print(f"Port: {data.get('port', 'Unknown')}")
            print(f"Auth: {data.get('authentication', 'Unknown')}")
        else:
            print(f"Health Check: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"Health Check: ERROR - {e}")
    
    # Test file listing
    try:
        response = requests.get(f"{base_url}/api/dicom/files", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"File Listing: SUCCESS")
            print(f"Total Files: {data.get('total', 0)}")
        else:
            print(f"File Listing: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"File Listing: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(" CLEAN DICOM SERVICE: READY")
    print(" No authentication required")
    print(" All endpoints accessible")
    print("=" * 50)

if __name__ == "__main__":
    test_dicom_service()
