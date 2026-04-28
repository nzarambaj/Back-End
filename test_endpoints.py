#!/usr/bin/env python3
"""
Test script to run all API endpoints on localhost:5000
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_endpoint(method, url, data=None, headers=None):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            print(f"Unsupported method: {method}")
            return False

        print(f"{method} {url} -> {response.status_code}")
        if response.status_code >= 400:
            print(f"  Error: {response.text[:200]}...")
        return response.status_code < 400
    except Exception as e:
        print(f"{method} {url} -> ERROR: {str(e)}")
        return False

def main():
    print("Testing all API endpoints on localhost:5000\n")

    # Root and health
    endpoints = [
        ("GET", "/"),
        ("GET", "/health"),
        ("GET", "/api/health"),
        ("GET", "/api/stats"),
        ("GET", "/api/dashboard"),
    ]

    # Authentication (will fail without data, but test structure)
    auth_endpoints = [
        ("POST", "/auth/register", {"username": "test", "password": "test"}),
        ("POST", "/auth/login", {"username": "test", "password": "test"}),
    ]

    # Medical staff
    medical_staff_endpoints = [
        ("GET", "/api/medical-staff/radiologists"),
        ("GET", "/api/medical-staff/referring-doctors"),
        ("GET", "/api/medical-staff/imaging-technicians"),
        ("GET", "/api/medical-staff/all"),
        ("GET", "/api/medical-staff/search?q=test"),
    ]

    # MWL
    mwl_endpoints = [
        ("GET", "/mwl/patients"),
        ("GET", "/mwl/worklists"),
    ]

    # Professional API
    pro_endpoints = [
        ("GET", "/api/doctors"),
        ("GET", "/api/patients"),
        ("GET", "/api/studies"),
    ]

    # DICOM
    dicom_endpoints = [
        ("GET", "/dicom/studies"),
    ]

    # Settings
    settings_endpoints = [
        ("GET", "/settings/modalities"),
        ("GET", "/settings/presets"),
    ]

    all_endpoints = endpoints + auth_endpoints + medical_staff_endpoints + mwl_endpoints + pro_endpoints + dicom_endpoints + settings_endpoints

    success_count = 0
    total_count = len(all_endpoints)

    for method, url, *args in all_endpoints:
        data = args[0] if args else None
        if test_endpoint(method, BASE_URL + url, data):
            success_count += 1

    print(f"\nSummary: {success_count}/{total_count} endpoints responded successfully")

if __name__ == "__main__":
    main()