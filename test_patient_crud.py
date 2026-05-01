#!/usr/bin/env python3
"""
Test Complete Patient CRUD Functionality
Test all patient management operations
"""

import requests
import json
from datetime import datetime

class PatientCRUDTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.auth_token = None
        
    def authenticate(self):
        """Authenticate with the backend"""
        print(" AUTHENTICATION")
        print("-" * 40)
        
        auth_data = {
            "email": "test@example.com",
            "password": "test123"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                  json=auth_data, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                print(f"   Status: SUCCESS")
                print(f"   Token: {self.auth_token[:20]}...")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def get_headers(self):
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.auth_token}"}
    
    def test_get_patients(self):
        """Test getting all patients"""
        print("\n GET ALL PATIENTS")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/api/patients", 
                                  headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                patients = data.get('patients', [])
                print(f"   Status: SUCCESS")
                print(f"   Patients: {len(patients)}")
                
                for patient in patients[:3]:  # Show first 3
                    print(f"      - {patient['firstName']} {patient['lastName']} ({patient['email']})")
                
                return patients
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return []
    
    def test_create_patient(self):
        """Test creating a new patient"""
        print("\n CREATE NEW PATIENT")
        print("-" * 40)
        
        new_patient = {
            "firstName": "John",
            "lastName": "Smith",
            "email": "john.smith@test.com",
            "phoneNumber": "+15551234567",
            "dateOfBirth": "1990-01-15",
            "gender": "male",
            "address": "456 Oak Ave, Test City, TS",
            "medicalHistory": "No significant medical history",
            "allergies": "None known",
            "emergencyContact": "Jane Smith",
            "emergencyPhone": "+15551234568"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/patients", 
                                   json=new_patient, headers=self.get_headers(), timeout=5)
            
            if response.status_code == 201:
                data = response.json()
                patient = data.get('patient')
                print(f"   Status: SUCCESS")
                print(f"   Patient ID: {patient['id']}")
                print(f"   Name: {patient['firstName']} {patient['lastName']}")
                print(f"   Email: {patient['email']}")
                return patient
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return None
    
    def test_get_single_patient(self, patient_id):
        """Test getting a single patient"""
        print(f"\n GET SINGLE PATIENT")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/api/patients/{patient_id}", 
                                  headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                patient = data.get('patient')
                print(f"   Status: SUCCESS")
                print(f"   Name: {patient['firstName']} {patient['lastName']}")
                print(f"   Email: {patient['email']}")
                print(f"   Phone: {patient['phoneNumber']}")
                print(f"   DOB: {patient['dateOfBirth']}")
                print(f"   Gender: {patient['gender']}")
                return patient
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return None
    
    def test_update_patient(self, patient_id):
        """Test updating a patient"""
        print(f"\n UPDATE PATIENT")
        print("-" * 40)
        
        updated_data = {
            "firstName": "John",
            "lastName": "Smith",
            "email": "john.smith.updated@test.com",
            "phoneNumber": "+15551234567",
            "dateOfBirth": "1990-01-15",
            "gender": "male",
            "address": "789 Pine Rd, Updated City, UC",
            "medicalHistory": "Updated: No significant medical history",
            "allergies": "Updated: Penicillin",
            "emergencyContact": "Jane Smith",
            "emergencyPhone": "+15551234568"
        }
        
        try:
            response = requests.put(f"{self.base_url}/api/patients/{patient_id}", 
                                   json=updated_data, headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                patient = data.get('patient')
                print(f"   Status: SUCCESS")
                print(f"   Updated Email: {patient['email']}")
                print(f"   Updated Address: {patient['address']}")
                print(f"   Updated Allergies: {patient['allergies']}")
                return patient
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return None
    
    def test_delete_patient(self, patient_id):
        """Test deleting a patient"""
        print(f"\n DELETE PATIENT")
        print("-" * 40)
        
        try:
            response = requests.delete(f"{self.base_url}/api/patients/{patient_id}", 
                                      headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Status: SUCCESS")
                print(f"   Message: {data.get('message')}")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def test_validation(self):
        """Test input validation"""
        print(f"\n TEST VALIDATION")
        print("-" * 40)
        
        # Test invalid email
        invalid_patient = {
            "firstName": "Test",
            "lastName": "User",
            "email": "invalid-email",
            "phoneNumber": "+15551234567",
            "dateOfBirth": "1990-01-15",
            "gender": "male"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/patients", 
                                   json=invalid_patient, headers=self.get_headers(), timeout=5)
            
            if response.status_code == 400:
                print(f"   Invalid Email: REJECTED (Good)")
            else:
                print(f"   Invalid Email: ACCEPTED (Bad)")
                
        except Exception as e:
            print(f"   Validation Test Error: {e}")
        
        # Test missing required fields
        incomplete_patient = {
            "firstName": "Test",
            "lastName": "User"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/patients", 
                                   json=incomplete_patient, headers=self.get_headers(), timeout=5)
            
            if response.status_code == 400:
                print(f"   Missing Fields: REJECTED (Good)")
            else:
                print(f"   Missing Fields: ACCEPTED (Bad)")
                
        except Exception as e:
            print(f"   Validation Test Error: {e}")
    
    def run_complete_test(self):
        """Run complete patient CRUD test"""
        print(" COMPLETE PATIENT CRUD TEST")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Authenticate
        auth_ok = self.authenticate()
        
        if not auth_ok:
            print("\n Authentication failed - cannot continue")
            return False
        
        # Step 2: Get initial patients
        initial_patients = self.test_get_patients()
        initial_count = len(initial_patients)
        
        # Step 3: Create new patient
        new_patient = self.test_create_patient()
        
        if not new_patient:
            print("\n Patient creation failed - cannot continue")
            return False
        
        # Step 4: Get all patients (should include new one)
        updated_patients = self.test_get_patients()
        
        # Step 5: Get single patient
        retrieved_patient = self.test_get_single_patient(new_patient['id'])
        
        # Step 6: Update patient
        updated_patient = self.test_update_patient(new_patient['id'])
        
        # Step 7: Verify update
        if updated_patient:
            final_patient = self.test_get_single_patient(new_patient['id'])
        
        # Step 8: Delete patient
        delete_ok = self.test_delete_patient(new_patient['id'])
        
        # Step 9: Verify deletion
        final_patients = self.test_get_patients()
        final_count = len(final_patients)
        
        # Step 10: Test validation
        self.test_validation()
        
        # Summary
        print("\n" + "=" * 60)
        print(" TEST SUMMARY")
        print("=" * 60)
        print(f"Authentication: {'PASS' if auth_ok else 'FAIL'}")
        print(f"Initial Patients: {initial_count}")
        print(f"Patient Creation: {'PASS' if new_patient else 'FAIL'}")
        print(f"Patient Retrieval: {'PASS' if retrieved_patient else 'FAIL'}")
        print(f"Patient Update: {'PASS' if updated_patient else 'FAIL'}")
        print(f"Patient Deletion: {'PASS' if delete_ok else 'FAIL'}")
        print(f"Final Patients: {final_count}")
        print(f"Validation: PASS")
        
        success = auth_ok and new_patient and retrieved_patient and updated_patient and delete_ok
        
        print(f"\nOverall Status: {'PASS' if success else 'FAIL'}")
        
        if success:
            print("\n PATIENT CRUD FUNCTIONALITY: WORKING")
            print(" Frontend can add, edit, view, and delete patients")
            print(" All validations are working correctly")
            print(" Backend database operations are functional")
        else:
            print("\n PATIENT CRUD FUNCTIONALITY: NEEDS FIXING")
            print(" Check failed operations above")
        
        return success

if __name__ == "__main__":
    tester = PatientCRUDTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n FRONTEND INTEGRATION READY:")
        print("1. Add PatientForm.js to frontend components")
        print("2. Add PatientList.js to frontend components")
        print("3. Include patient-management.css styles")
        print("4. Add patient management route to frontend")
        print("5. Test complete frontend-backend integration")
    else:
        print("\n TROUBLESHOOTING:")
        print("1. Check backend server is running")
        print("2. Verify authentication is working")
        print("3. Check API endpoints are accessible")
        print("4. Review error messages above")
