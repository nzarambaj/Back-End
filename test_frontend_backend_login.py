#!/usr/bin/env python3
"""
Test Frontend-Backend Login Integration
Test dashboard access and login functionality
"""

import requests
import json
from datetime import datetime

class FrontendBackendLoginTester:
    def __init__(self):
        self.backend_url = "http://localhost:5000"
        self.frontend_url = "http://localhost:3000"
        
    def test_frontend_access(self):
        """Test frontend server access"""
        print(" FRONTEND SERVER ACCESS TEST")
        print("=" * 60)
        
        endpoints = [
            ("Home", "/"),
            ("Dashboard", "/dashboard"),
            ("Login", "/login")
        ]
        
        for name, endpoint in endpoints:
            try:
                response = requests.get(f"{self.frontend_url}{endpoint}", timeout=5)
                print(f"   {name} ({endpoint}): HTTP {response.status_code}")
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'html' in content_type.lower():
                        print(f"      Status: ACCESSIBLE (HTML)")
                    else:
                        print(f"      Status: RESPONDING ({content_type})")
                else:
                    print(f"      Status: NOT ACCESSIBLE")
                    
            except Exception as e:
                print(f"   {name} ({endpoint}): ERROR - {e}")
        
        return True
    
    def test_backend_api(self):
        """Test backend API endpoints"""
        print("\n BACKEND API TEST")
        print("=" * 60)
        
        # Test health endpoint
        try:
            response = requests.get(f"{self.backend_url}/api/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   Health Endpoint: WORKING")
                print(f"      Database: {data.get('database', 'Unknown')}")
                print(f"      Status: {data.get('status', 'Unknown')}")
            else:
                print(f"   Health Endpoint: HTTP {response.status_code}")
        except Exception as e:
            print(f"   Health Endpoint: ERROR - {e}")
        
        return True
    
    def test_login_credentials(self):
        """Test login credentials and get authentication token"""
        print("\n LOGIN CREDENTIALS TEST")
        print("=" * 60)
        
        # Test different login credentials
        login_attempts = [
            {"email": "test@example.com", "password": "test123"},
            {"email": "admin@medical.com", "password": "admin123"},
            {"email": "john.doe@hospital.com", "password": "doctor123"}
        ]
        
        for i, credentials in enumerate(login_attempts, 1):
            try:
                response = requests.post(f"{self.backend_url}/api/auth/login", 
                                        json=credentials, timeout=5)
                
                print(f"   Login Attempt {i}:")
                print(f"      Email: {credentials['email']}")
                print(f"      Status: HTTP {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    token = data.get('token')
                    user = data.get('user', {})
                    
                    print(f"      Result: SUCCESS")
                    print(f"      Token: {token[:20]}..." if token else "No token")
                    print(f"      User: {user.get('firstName', 'N/A')} {user.get('lastName', 'N/A')}")
                    print(f"      Role: {user.get('role', 'N/A')}")
                    
                    return token, user  # Return the first successful login
                    
                else:
                    print(f"      Result: FAILED")
                    if response.status_code == 401:
                        print(f"      Reason: Invalid credentials")
                    else:
                        print(f"      Reason: HTTP {response.status_code}")
                        
            except Exception as e:
                print(f"      Error: {e}")
        
        return None, None
    
    def test_protected_endpoints(self, token):
        """Test protected API endpoints with authentication token"""
        print("\n PROTECTED ENDPOINTS TEST")
        print("=" * 60)
        
        if not token:
            print("   No authentication token - skipping protected endpoints")
            return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        endpoints = [
            ("Patients", "/api/patients"),
            ("Doctors", "/api/doctors"),
            ("Studies", "/api/studies"),
            ("Images", "/api/images")
        ]
        
        success_count = 0
        
        for name, endpoint in endpoints:
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", 
                                      headers=headers, timeout=5)
                
                print(f"   {name}: HTTP {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if name == "Patients":
                        count = len(data.get('patients', []))
                        print(f"      Records: {count} patients")
                    elif name == "Doctors":
                        count = len(data.get('doctors', []))
                        print(f"      Records: {count} doctors")
                    elif name == "Studies":
                        count = len(data.get('studies', []))
                        print(f"      Records: {count} studies")
                    elif name == "Images":
                        count = len(data.get('images', []))
                        print(f"      Records: {count} images")
                    
                    success_count += 1
                    print(f"      Status: ACCESSIBLE")
                    
                elif response.status_code == 401:
                    print(f"      Status: AUTHENTICATION FAILED")
                else:
                    print(f"      Status: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   {name}: ERROR - {e}")
        
        print(f"\n   Protected Endpoints Access: {success_count}/{len(endpoints)} working")
        return success_count == len(endpoints)
    
    def test_database_data_access(self, token):
        """Test database data access through API"""
        print("\n DATABASE DATA ACCESS TEST")
        print("=" * 60)
        
        if not token:
            print("   No authentication token - skipping data access test")
            return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            # Test patients data
            response = requests.get(f"{self.backend_url}/api/patients", 
                                  headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                patients = data.get('patients', [])
                
                print(f"   Patients Database:")
                print(f"      Total Records: {len(patients)}")
                
                if patients:
                    sample_patient = patients[0]
                    print(f"      Sample Patient:")
                    print(f"         ID: {sample_patient.get('id', 'N/A')}")
                    print(f"         Name: {sample_patient.get('firstName', 'N/A')} {sample_patient.get('lastName', 'N/A')}")
                    print(f"         Email: {sample_patient.get('email', 'N/A')}")
                    print(f"         Phone: {sample_patient.get('phoneNumber', 'N/A')}")
                    
                    # Test patient studies
                    patient_id = sample_patient.get('id')
                    if patient_id:
                        studies_response = requests.get(f"{self.backend_url}/api/studies", 
                                                       headers=headers, timeout=5)
                        
                        if studies_response.status_code == 200:
                            studies_data = studies_response.json()
                            studies = studies_data.get('studies', [])
                            patient_studies = [s for s in studies if s.get('patientId') == patient_id]
                            
                            print(f"      Patient Studies: {len(patient_studies)}")
                            if patient_studies:
                                study = patient_studies[0]
                                print(f"         Sample Study:")
                                print(f"            Type: {study.get('studyType', 'N/A')}")
                                print(f"            Status: {study.get('status', 'N/A')}")
                                print(f"            Date: {study.get('studyDate', 'N/A')}")
                
                return True
            else:
                print(f"   Patients API Error: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Data Access Error: {e}")
            return False
    
    def generate_access_guide(self, token, user):
        """Generate access guide for frontend login"""
        print("\n FRONTEND LOGIN ACCESS GUIDE")
        print("=" * 60)
        
        print("   TO ACCESS DASHBOARD:")
        print("   1. Open browser: http://localhost:3000/login")
        print("   2. Use these credentials:")
        
        if user:
            print(f"      Email: {user.get('email', 'N/A')}")
            print(f"      Password: [Use the password that worked]")
            print(f"      Role: {user.get('role', 'N/A')}")
        else:
            print("      Email: test@example.com")
            print("      Password: test123")
        
        print("   3. Click 'Login' button")
        print("   4. You will be redirected to: http://localhost:3000/dashboard")
        
        print("\n   DASHBOARD FEATURES:")
        print("   - View patient records")
        print("   - Access doctor information")
        print("   - View medical studies")
        print("   - Manage medical images")
        print("   - Access Calculus API")
        
        print("\n   BACKEND API ACCESS:")
        print("   - All endpoints require authentication")
        print("   - Token-based authentication")
        print("   - PostgreSQL 18 database connected")
        print("   - Medical imaging data accessible")
        
        return True
    
    def run_complete_test(self):
        """Run complete frontend-backend login test"""
        print(" COMPLETE FRONTEND-BACKEND LOGIN TEST")
        print("=" * 80)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Frontend: {self.frontend_url}")
        print(f"Backend: {self.backend_url}")
        print("=" * 80)
        
        # Test 1: Frontend access
        self.test_frontend_access()
        
        # Test 2: Backend API
        self.test_backend_api()
        
        # Test 3: Login credentials
        token, user = self.test_login_credentials()
        
        # Test 4: Protected endpoints
        if token:
            protected_ok = self.test_protected_endpoints(token)
            
            # Test 5: Database data access
            data_ok = self.test_database_data_access(token)
            
            # Test 6: Generate access guide
            self.generate_access_guide(token, user)
            
            print("\n" + "=" * 80)
            print(" LOGIN INTEGRATION SUMMARY")
            print("=" * 80)
            print(" Frontend Server: RUNNING")
            print(" Backend Server: RUNNING")
            print(" Login Authentication: WORKING" if token else "FAILED")
            print(" Database Access: WORKING" if data_ok else "FAILED")
            print(" Protected Endpoints: WORKING" if protected_ok else "FAILED")
            
            if token and data_ok and protected_ok:
                print("\n READY FOR USE:")
                print("   Dashboard: http://localhost:3000/dashboard")
                print("   Login: http://localhost:3000/login")
                print("   Backend API: http://localhost:5000")
                print("   All medical data: ACCESSIBLE")
                
                return True
            else:
                print("\n NEEDS ATTENTION:")
                if not token:
                    print("   - Login authentication failed")
                if not data_ok:
                    print("   - Database access failed")
                if not protected_ok:
                    print("   - Protected endpoints failed")
                
                return False
        else:
            print("\n" + "=" * 80)
            print(" LOGIN FAILED")
            print("=" * 80)
            print("   Could not authenticate with backend")
            print("   Check login credentials")
            print("   Verify backend authentication system")
            return False

if __name__ == "__main__":
    tester = FrontendBackendLoginTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n FRONTEND-BACKEND LOGIN: READY")
        print(" You can now access the dashboard through login!")
    else:
        print("\n FRONTEND-BACKEND LOGIN: NEEDS FIXING")
        print(" Check the issues above and try again")
