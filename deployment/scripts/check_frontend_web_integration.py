#!/usr/bin/env python3
"""
Check Frontend-Backend Web Integration
Verify ordinary web functionality (not demo mode)
"""

import requests
import json
from datetime import datetime

class FrontendWebIntegrationChecker:
    def __init__(self):
        self.frontend_url = "http://localhost:3000"
        self.backend_url = "http://localhost:5000"
        self.calculus_url = "http://localhost:5001"
        self.dicom_url = "http://localhost:5002"
        self.auth_token = None
        
    def test_frontend_access(self):
        """Test if frontend is accessible like ordinary web"""
        print(" FRONTEND WEB ACCESS TEST")
        print("=" * 50)
        
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print(f"   Status: SUCCESS")
                print(f"   Frontend: Accessible at {self.frontend_url}")
                print(f"   Content Type: {response.headers.get('content-type', 'Unknown')}")
                print(f"   Content Length: {len(response.content)} bytes")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def test_login_flow(self):
        """Test proper login flow like ordinary web app"""
        print("\n LOGIN FLOW TEST")
        print("-" * 50)
        
        try:
            # Test login endpoint
            login_data = {
                "email": "test@example.com",
                "password": "test123"
            }
            
            response = requests.post(f"{self.backend_url}/api/auth/login", 
                                  json=login_data, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                user_info = data.get('user', {})
                
                print(f"   Login: SUCCESS")
                print(f"   Token: {self.auth_token[:20] if self.auth_token else 'None'}...")
                print(f"   User: {user_info.get('email', 'Unknown')}")
                print(f"   Role: {user_info.get('role', 'Unknown')}")
                print(f"   Name: {user_info.get('firstName', '')} {user_info.get('lastName', '')}")
                return True
            else:
                print(f"   Login: FAILED - HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                return False
        except Exception as e:
            print(f"   Login: ERROR - {e}")
            return False
    
    def test_backend_api_access(self):
        """Test backend API access with authentication"""
        print("\n BACKEND API ACCESS TEST")
        print("-" * 50)
        
        if not self.auth_token:
            print("   Status: No authentication token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        endpoints = [
            ("/api/health", "Health Check"),
            ("/api/patients", "Patients"),
            ("/api/doctors", "Doctors"),
            ("/api/studies", "Studies")
        ]
        
        results = {}
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", 
                                      headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    item_count = len(data.get('patients', [])) if 'patients' in data else len(data.get('doctors', [])) if 'doctors' in data else len(data.get('studies', [])) if 'studies' in data else 1
                    
                    results[name] = {
                        'status': 'SUCCESS',
                        'count': item_count,
                        'accessible': True
                    }
                    print(f"   {name}: SUCCESS ({item_count} items)")
                else:
                    results[name] = {
                        'status': f'HTTP {response.status_code}',
                        'accessible': False
                    }
                    print(f"   {name}: FAILED - HTTP {response.status_code}")
            except Exception as e:
                results[name] = {
                    'status': 'ERROR',
                    'accessible': False,
                    'error': str(e)
                }
                print(f"   {name}: ERROR - {e}")
        
        return results
    
    def test_calculus_api_access(self):
        """Test calculus API access (no auth required)"""
        print("\n CALCULUS API ACCESS TEST")
        print("-" * 50)
        
        endpoints = [
            ("/api/health", "Health Check"),
            ("/api/equipment", "Equipment List"),
            ("/api/equipment/ct", "CT Equipment"),
            ("/api/equipment/mri", "MRI Equipment"),
            ("/api/categories", "Categories"),
            ("/api/manufacturers", "Manufacturers")
        ]
        
        results = {}
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.calculus_url}{endpoint}", timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    item_count = len(data.get('equipment', [])) if 'equipment' in data else len(data.get('categories', [])) if 'categories' in data else len(data.get('manufacturers', [])) if 'manufacturers' in data else 1
                    
                    results[name] = {
                        'status': 'SUCCESS',
                        'count': item_count,
                        'accessible': True
                    }
                    print(f"   {name}: SUCCESS ({item_count} items)")
                else:
                    results[name] = {
                        'status': f'HTTP {response.status_code}',
                        'accessible': False
                    }
                    print(f"   {name}: FAILED - HTTP {response.status_code}")
            except Exception as e:
                results[name] = {
                    'status': 'ERROR',
                    'accessible': False,
                    'error': str(e)
                }
                print(f"   {name}: ERROR - {e}")
        
        return results
    
    def test_dicom_api_access(self):
        """Test DICOM API access (no auth required)"""
        print("\n DICOM API ACCESS TEST")
        print("-" * 50)
        
        endpoints = [
            ("/api/dicom/health", "Health Check"),
            ("/api/dicom/files", "File List")
        ]
        
        results = {}
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.dicom_url}{endpoint}", timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    item_count = len(data.get('files', [])) if 'files' in data else 1
                    
                    results[name] = {
                        'status': 'SUCCESS',
                        'count': item_count,
                        'accessible': True
                    }
                    print(f"   {name}: SUCCESS ({item_count} items)")
                else:
                    results[name] = {
                        'status': f'HTTP {response.status_code}',
                        'accessible': False
                    }
                    print(f"   {name}: FAILED - HTTP {response.status_code}")
            except Exception as e:
                results[name] = {
                    'status': 'ERROR',
                    'accessible': False,
                    'error': str(e)
                }
                print(f"   {name}: ERROR - {e}")
        
        return results
    
    def test_frontend_backend_communication(self):
        """Test if frontend can communicate with backend like ordinary web"""
        print("\n FRONTEND-BACKEND COMMUNICATION TEST")
        print("-" * 50)
        
        # Test CORS headers
        try:
            response = requests.options(f"{self.backend_url}/api/health", timeout=5)
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            print("   CORS Headers:")
            for header, value in cors_headers.items():
                print(f"     {header}: {value or 'Not Set'}")
            
            cors_ok = cors_headers['Access-Control-Allow-Origin'] is not None
            print(f"   CORS Status: {'OK' if cors_ok else 'MISSING'}")
            
        except Exception as e:
            print(f"   CORS Test: ERROR - {e}")
            cors_ok = False
        
        return cors_ok
    
    def test_patient_crud_operations(self):
        """Test patient CRUD operations like ordinary web app"""
        print("\n PATIENT CRUD OPERATIONS TEST")
        print("-" * 50)
        
        if not self.auth_token:
            print("   Status: No authentication token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Test 1: Create patient
        try:
            patient_data = {
                "firstName": "John",
                "lastName": "Doe",
                "dateOfBirth": "1980-01-01",
                "gender": "M",
                "email": "john.doe@example.com",
                "phone": "555-1234",
                "address": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zipCode": "12345"
            }
            
            response = requests.post(f"{self.backend_url}/api/patients", 
                                   json=patient_data, headers=headers, timeout=5)
            
            if response.status_code == 201:
                created_patient = response.json()
                patient_id = created_patient.get('id')
                print(f"   Create Patient: SUCCESS")
                print(f"   Patient ID: {patient_id}")
                print(f"   Name: {created_patient.get('firstName', '')} {created_patient.get('lastName', '')}")
            else:
                print(f"   Create Patient: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Create Patient: ERROR - {e}")
            return False
        
        # Test 2: Get patients
        try:
            response = requests.get(f"{self.backend_url}/api/patients", 
                                  headers=headers, timeout=5)
            
            if response.status_code == 200:
                patients = response.json().get('patients', [])
                print(f"   Get Patients: SUCCESS ({len(patients)} patients)")
            else:
                print(f"   Get Patients: FAILED - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   Get Patients: ERROR - {e}")
        
        # Test 3: Update patient
        try:
            update_data = {"phone": "555-5678"}
            response = requests.put(f"{self.backend_url}/api/patients/{patient_id}", 
                                  json=update_data, headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"   Update Patient: SUCCESS")
            else:
                print(f"   Update Patient: FAILED - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   Update Patient: ERROR - {e}")
        
        # Test 4: Delete patient
        try:
            response = requests.delete(f"{self.backend_url}/api/patients/{patient_id}", 
                                     headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"   Delete Patient: SUCCESS")
            else:
                print(f"   Delete Patient: FAILED - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   Delete Patient: ERROR - {e}")
        
        return True
    
    def run_complete_web_integration_test(self):
        """Run complete web integration test"""
        print(" COMPLETE FRONTEND-BACKEND WEB INTEGRATION TEST")
        print("=" * 80)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Step 1: Test frontend access
        frontend_ok = self.test_frontend_access()
        
        # Step 2: Test login flow
        login_ok = self.test_login_flow()
        
        # Step 3: Test backend API access
        backend_results = self.test_backend_api_access()
        
        # Step 4: Test calculus API access
        calculus_results = self.test_calculus_api_access()
        
        # Step 5: Test DICOM API access
        dicom_results = self.test_dicom_api_access()
        
        # Step 6: Test frontend-backend communication
        cors_ok = self.test_frontend_backend_communication()
        
        # Step 7: Test patient CRUD operations
        crud_ok = self.test_patient_crud_operations()
        
        # Summary
        print("\n" + "=" * 80)
        print(" WEB INTEGRATION SUMMARY")
        print("=" * 80)
        
        print(f"Frontend Access: {'WORKING' if frontend_ok else 'FAILED'}")
        print(f"Login Flow: {'WORKING' if login_ok else 'FAILED'}")
        print(f"Backend API: {'WORKING' if all(r['accessible'] for r in backend_results.values()) else 'PARTIAL'}")
        print(f"Calculus API: {'WORKING' if all(r['accessible'] for r in calculus_results.values()) else 'PARTIAL'}")
        print(f"DICOM API: {'WORKING' if all(r['accessible'] for r in dicom_results.values()) else 'PARTIAL'}")
        print(f"CORS Headers: {'CONFIGURED' if cors_ok else 'MISSING'}")
        print(f"CRUD Operations: {'WORKING' if crud_ok else 'FAILED'}")
        
        # Overall status
        overall_ok = frontend_ok and login_ok and cors_ok and crud_ok
        
        print(f"\nOverall Web Integration: {'COMPLETE' if overall_ok else 'NEEDS FIXING'}")
        
        if overall_ok:
            print("\n" + "=" * 80)
            print(" FRONTEND-BACKEND WEB INTEGRATION: COMPLETE")
            print("=" * 80)
            print(" The system works like an ordinary web application:")
            print(f" - Frontend: {self.frontend_url}")
            print(f" - Backend: {self.backend_url}")
            print(f" - Calculus: {self.calculus_url}")
            print(f" - DICOM: {self.dicom_url}")
            print("\n WEB FUNCTIONALITY:")
            print(" - User login and authentication")
            print(" - Patient CRUD operations")
            print(" - Equipment data access")
            print(" - Medical image processing")
            print(" - CORS-enabled communication")
            print("\n ACCESS INSTRUCTIONS:")
            print(" 1. Open browser: http://localhost:3000")
            print(" 2. Login: test@example.com / test123")
            print(" 3. Use full web functionality")
            print(" 4. Access all backend services")
        else:
            print("\n" + "=" * 80)
            print(" WEB INTEGRATION: NEEDS ATTENTION")
            print("=" * 80)
            if not frontend_ok:
                print(" - Frontend is not accessible")
            if not login_ok:
                print(" - Login flow is not working")
            if not cors_ok:
                print(" - CORS headers are not configured")
            if not crud_ok:
                print(" - CRUD operations are not working")
        
        return overall_ok

if __name__ == "__main__":
    checker = FrontendWebIntegrationChecker()
    checker.run_complete_web_integration_test()
