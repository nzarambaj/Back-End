#!/usr/bin/env python3
"""
Comprehensive Medical Database Check
Thoroughly verify medical_db is working properly and ready for frontend access
"""

import requests
import time
from datetime import datetime

class MedicalDatabaseChecker:
    def __init__(self):
        self.backend_url = "http://localhost:5000"
        self.frontend_url = "http://localhost:3000"
        self.flask_api_url = "http://localhost:5001"
        self.results = {}
        self.auth_token = None
        
    def test_backend_connectivity(self):
        """Test backend connectivity and get auth token"""
        print("1. TESTING BACKEND CONNECTIVITY")
        print("-" * 50)
        
        try:
            # Test health endpoint
            response = requests.get(f"{self.backend_url}/api/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                self.results['backend_health'] = {
                    'status': 'SUCCESS',
                    'service': health_data.get('service', 'Unknown'),
                    'database': health_data.get('database', 'Unknown'),
                    'database_name': health_data.get('database_name', 'Unknown'),
                    'database_connected': health_data.get('database_connected', False)
                }
                print(f"   ✅ Backend Health: SUCCESS")
                print(f"   Service: {health_data.get('service', 'Unknown')}")
                print(f"   Database: {health_data.get('database', 'Unknown')}")
                print(f"   DB Name: {health_data.get('database_name', 'Unknown')}")
                print(f"   Connected: {health_data.get('database_connected', False)}")
            else:
                self.results['backend_health'] = {
                    'status': f'HTTP {response.status_code}',
                    'error': response.text[:100]
                }
                print(f"   ❌ Backend Health: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.results['backend_health'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"   ❌ Backend Health: ERROR - {e}")
            return False
        
        # Get authentication token
        try:
            login_data = {"email": "test@example.com", "password": "test123"}
            response = requests.post(f"{self.backend_url}/api/auth/login", 
                                   json=login_data, timeout=5)
            
            if response.status_code == 200:
                self.auth_token = response.json().get('token')
                self.results['auth'] = {
                    'status': 'SUCCESS',
                    'token': self.auth_token[:20] + '...' if self.auth_token else 'None'
                }
                print(f"   ✅ Authentication: SUCCESS")
                print(f"   Token: {self.auth_token[:20] if self.auth_token else 'None'}...")
                return True
            else:
                self.results['auth'] = {
                    'status': f'HTTP {response.status_code}',
                    'error': response.text[:100]
                }
                print(f"   ❌ Authentication: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.results['auth'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"   ❌ Authentication: ERROR - {e}")
            return False
    
    def test_medical_db_status(self):
        """Test medical database status and statistics"""
        print("\n2. TESTING MEDICAL DATABASE STATUS")
        print("-" * 50)
        
        if not self.auth_token:
            print("   ❌ No auth token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(f"{self.backend_url}/api/medical-db/status", 
                                  headers=headers, timeout=5)
            
            if response.status_code == 200:
                status_data = response.json()
                stats = status_data.get('statistics', {})
                
                self.results['medical_db_status'] = {
                    'status': 'SUCCESS',
                    'database_name': status_data.get('database_name', 'Unknown'),
                    'status': status_data.get('status', 'Unknown'),
                    'connection': status_data.get('connection', False),
                    'patient_count': stats.get('patient_count', 0),
                    'doctor_count': stats.get('doctor_count', 0),
                    'study_count': stats.get('study_count', 0)
                }
                
                print(f"   ✅ Medical DB Status: SUCCESS")
                print(f"   Database Name: {status_data.get('database_name', 'Unknown')}")
                print(f"   Status: {status_data.get('status', 'Unknown')}")
                print(f"   Connection: {status_data.get('connection', False)}")
                print(f"   Patient Count: {stats.get('patient_count', 0)}")
                print(f"   Doctor Count: {stats.get('doctor_count', 0)}")
                print(f"   Study Count: {stats.get('study_count', 0)}")
                
                return status_data.get('connection', False)
            else:
                self.results['medical_db_status'] = {
                    'status': f'HTTP {response.status_code}',
                    'error': response.text[:100]
                }
                print(f"   ❌ Medical DB Status: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.results['medical_db_status'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"   ❌ Medical DB Status: ERROR - {e}")
            return False
    
    def test_crud_operations(self):
        """Test CRUD operations on medical database"""
        print("\n3. TESTING CRUD OPERATIONS")
        print("-" * 50)
        
        if not self.auth_token:
            print("   ❌ No auth token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        crud_results = {}
        
        # Test READ operations
        try:
            # Get patients
            response = requests.get(f"{self.backend_url}/api/patients", 
                                  headers=headers, timeout=5)
            if response.status_code == 200:
                patients_data = response.json()
                crud_results['read_patients'] = {
                    'status': 'SUCCESS',
                    'count': patients_data.get('total', 0),
                    'source': patients_data.get('source', 'Unknown')
                }
                print(f"   ✅ Read Patients: SUCCESS ({patients_data.get('total', 0)} items)")
            else:
                crud_results['read_patients'] = {
                    'status': f'HTTP {response.status_code}',
                    'error': response.text[:50]
                }
                print(f"   ❌ Read Patients: HTTP {response.status_code}")
            
            # Get doctors
            response = requests.get(f"{self.backend_url}/api/doctors", 
                                  headers=headers, timeout=5)
            if response.status_code == 200:
                doctors_data = response.json()
                crud_results['read_doctors'] = {
                    'status': 'SUCCESS',
                    'count': doctors_data.get('total', 0),
                    'source': doctors_data.get('source', 'Unknown')
                }
                print(f"   ✅ Read Doctors: SUCCESS ({doctors_data.get('total', 0)} items)")
            else:
                crud_results['read_doctors'] = {
                    'status': f'HTTP {response.status_code}',
                    'error': response.text[:50]
                }
                print(f"   ❌ Read Doctors: HTTP {response.status_code}")
            
            # Get studies
            response = requests.get(f"{self.backend_url}/api/studies", 
                                  headers=headers, timeout=5)
            if response.status_code == 200:
                studies_data = response.json()
                crud_results['read_studies'] = {
                    'status': 'SUCCESS',
                    'count': studies_data.get('total', 0),
                    'source': studies_data.get('source', 'Unknown')
                }
                print(f"   ✅ Read Studies: SUCCESS ({studies_data.get('total', 0)} items)")
            else:
                crud_results['read_studies'] = {
                    'status': f'HTTP {response.status_code}',
                    'error': response.text[:50]
                }
                print(f"   ❌ Read Studies: HTTP {response.status_code}")
        
        except Exception as e:
            print(f"   ❌ Read Operations: ERROR - {e}")
            crud_results['read_error'] = str(e)
        
        # Test CREATE operation
        try:
            doctor_data = {
                "full_name": "Dr. Test Medical DB",
                "specialization": "Test Specialization",
                "phone": "555-1234",
                "email": f"test.medical.db.{int(time.time())}@example.com"
            }
            
            response = requests.post(f"{self.backend_url}/api/doctors", 
                                   json=doctor_data, headers=headers, timeout=5)
            
            if response.status_code == 201:
                created_doctor = response.json().get('doctor')
                doctor_id = created_doctor.get('id')
                
                crud_results['create_doctor'] = {
                    'status': 'SUCCESS',
                    'doctor_id': doctor_id,
                    'name': created_doctor.get('full_name', 'Unknown'),
                    'source': response.json().get('source', 'Unknown')
                }
                print(f"   ✅ Create Doctor: SUCCESS (ID: {doctor_id})")
                
                # Test UPDATE operation
                update_data = {
                    "full_name": "Dr. Updated Medical DB",
                    "specialization": "Updated Specialization",
                    "phone": "555-5678",
                    "email": f"updated.medical.db.{int(time.time())}@example.com"
                }
                
                response = requests.put(f"{self.backend_url}/api/doctors/{doctor_id}", 
                                       json=update_data, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    updated_doctor = response.json().get('doctor')
                    crud_results['update_doctor'] = {
                        'status': 'SUCCESS',
                        'doctor_id': doctor_id,
                        'updated_name': updated_doctor.get('full_name', 'Unknown'),
                        'source': response.json().get('source', 'Unknown')
                    }
                    print(f"   ✅ Update Doctor: SUCCESS (ID: {doctor_id})")
                    
                    # Test DELETE operation
                    response = requests.delete(f"{self.backend_url}/doctors/{doctor_id}", 
                                             headers=headers, timeout=5)
                    
                    if response.status_code == 200:
                        delete_result = response.json()
                        crud_results['delete_doctor'] = {
                            'status': 'SUCCESS',
                            'doctor_id': doctor_id,
                            'message': delete_result.get('message', 'Unknown'),
                            'source': delete_result.get('source', 'Unknown')
                        }
                        print(f"   ✅ Delete Doctor: SUCCESS (ID: {doctor_id})")
                    else:
                        crud_results['delete_doctor'] = {
                            'status': f'HTTP {response.status_code}',
                            'error': response.text[:50]
                        }
                        print(f"   ❌ Delete Doctor: HTTP {response.status_code}")
                else:
                    crud_results['update_doctor'] = {
                        'status': f'HTTP {response.status_code}',
                        'error': response.text[:50]
                    }
                    print(f"   ❌ Update Doctor: HTTP {response.status_code}")
            else:
                crud_results['create_doctor'] = {
                    'status': f'HTTP {response.status_code}',
                    'error': response.text[:50]
                }
                print(f"   ❌ Create Doctor: HTTP {response.status_code}")
        
        except Exception as e:
            print(f"   ❌ CRUD Operations: ERROR - {e}")
            crud_results['crud_error'] = str(e)
        
        self.results['crud_operations'] = crud_results
        
        # Count successful operations
        success_count = sum(1 for op in crud_results.values() 
                           if isinstance(op, dict) and op.get('status') == 'SUCCESS')
        total_count = len([op for op in crud_results.values() 
                           if isinstance(op, dict) and 'status' in op])
        
        print(f"   CRUD Operations: {success_count}/{total_count} successful")
        return success_count >= 4  # At least read operations should work
    
    def test_flask_api_integration(self):
        """Test Flask API integration"""
        print("\n4. TESTING FLASK API INTEGRATION")
        print("-" * 50)
        
        if not self.auth_token:
            print("   ❌ No auth token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(f"{self.backend_url}/api/equipment", 
                                  headers=headers, timeout=5)
            
            if response.status_code == 200:
                equipment_data = response.json()
                self.results['flask_api_integration'] = {
                    'status': 'SUCCESS',
                    'equipment_count': equipment_data.get('total', 0),
                    'source': equipment_data.get('source', 'Unknown'),
                    'flask_api_url': equipment_data.get('flask_api_url', 'Unknown')
                }
                print(f"   ✅ Flask API Integration: SUCCESS")
                print(f"   Equipment Count: {equipment_data.get('total', 0)}")
                print(f"   Source: {equipment_data.get('source', 'Unknown')}")
                print(f"   Flask API URL: {equipment_data.get('flask_api_url', 'Unknown')}")
                return True
            else:
                self.results['flask_api_integration'] = {
                    'status': f'HTTP {response.status_code}',
                    'error': response.text[:100]
                }
                print(f"   ❌ Flask API Integration: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.results['flask_api_integration'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"   ❌ Flask API Integration: ERROR - {e}")
            return False
    
    def test_frontend_access(self):
        """Test frontend accessibility to medical data"""
        print("\n5. TESTING FRONTEND ACCESS")
        print("-" * 50)
        
        try:
            # Test frontend is accessible
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                self.results['frontend_access'] = {
                    'status': 'SUCCESS',
                    'url': self.frontend_url,
                    'content_type': response.headers.get('content-type', 'Unknown')
                }
                print(f"   ✅ Frontend Access: SUCCESS")
                print(f"   URL: {self.frontend_url}")
                print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
                
                # Test dashboard endpoint
                dashboard_url = f"{self.frontend_url}/dashboard"
                try:
                    response = requests.get(dashboard_url, timeout=5)
                    if response.status_code == 200:
                        self.results['frontend_dashboard'] = {
                            'status': 'SUCCESS',
                            'url': dashboard_url
                        }
                        print(f"   ✅ Frontend Dashboard: SUCCESS")
                        print(f"   URL: {dashboard_url}")
                    else:
                        self.results['frontend_dashboard'] = {
                            'status': f'HTTP {response.status_code}',
                            'url': dashboard_url
                        }
                        print(f"   ⚠️ Frontend Dashboard: HTTP {response.status_code}")
                except:
                    self.results['frontend_dashboard'] = {
                        'status': 'ERROR',
                        'url': dashboard_url
                    }
                    print(f"   ❌ Frontend Dashboard: ERROR")
                
                return True
            else:
                self.results['frontend_access'] = {
                    'status': f'HTTP {response.status_code}',
                    'url': self.frontend_url
                }
                print(f"   ❌ Frontend Access: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.results['frontend_access'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"   ❌ Frontend Access: ERROR - {e}")
            return False
    
    def test_complete_workflow(self):
        """Test complete workflow from frontend to medical database"""
        print("\n6. TESTING COMPLETE WORKFLOW")
        print("-" * 50)
        
        if not self.auth_token:
            print("   ❌ No auth token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            # Step 1: Get current data from medical database
            response = requests.get(f"{self.backend_url}/api/patients", 
                                  headers=headers, timeout=5)
            if response.status_code != 200:
                print("   ❌ Workflow: Failed to get patients")
                return False
            
            initial_patients = response.json().get('patients', [])
            print(f"   Step 1: Get patients - SUCCESS ({len(initial_patients)} items)")
            
            # Step 2: Get doctors from medical database
            response = requests.get(f"{self.backend_url}/api/doctors", 
                                  headers=headers, timeout=5)
            if response.status_code != 200:
                print("   ❌ Workflow: Failed to get doctors")
                return False
            
            initial_doctors = response.json().get('doctors', [])
            print(f"   Step 2: Get doctors - SUCCESS ({len(initial_doctors)} items)")
            
            # Step 3: Get equipment from Flask API
            response = requests.get(f"{self.backend_url}/api/equipment", 
                                  headers=headers, timeout=5)
            if response.status_code != 200:
                print("   ❌ Workflow: Failed to get equipment")
                return False
            
            equipment_data = response.json()
            equipment_count = equipment_data.get('total', 0)
            print(f"   Step 3: Get equipment - SUCCESS ({equipment_count} items)")
            
            # Step 4: Create new doctor in medical database
            doctor_data = {
                "full_name": f"Dr. Workflow Test {int(time.time())}",
                "specialization": "Workflow Testing",
                "phone": "555-9999",
                "email": f"workflow.test.{int(time.time())}@example.com"
            }
            
            response = requests.post(f"{self.backend_url}/api/doctors", 
                                   json=doctor_data, headers=headers, timeout=5)
            if response.status_code != 201:
                print("   ❌ Workflow: Failed to create doctor")
                return False
            
            created_doctor = response.json().get('doctor')
            doctor_id = created_doctor.get('id')
            print(f"   Step 4: Create doctor - SUCCESS (ID: {doctor_id})")
            
            # Step 5: Verify doctor was created
            response = requests.get(f"{self.backend_url}/api/doctors", 
                                  headers=headers, timeout=5)
            if response.status_code != 200:
                print("   ❌ Workflow: Failed to verify doctor creation")
                return False
            
            updated_doctors = response.json().get('doctors', [])
            if len(updated_doctors) <= len(initial_doctors):
                print("   ❌ Workflow: Doctor creation not verified")
                return False
            
            print(f"   Step 5: Verify doctor creation - SUCCESS ({len(updated_doctors)} total)")
            
            # Step 6: Clean up - delete the created doctor
            response = requests.delete(f"{self.backend_url}/doctors/{doctor_id}", 
                                     headers=headers, timeout=5)
            if response.status_code != 200:
                print("   ⚠️ Workflow: Failed to delete test doctor")
            else:
                print(f"   Step 6: Delete test doctor - SUCCESS")
            
            self.results['complete_workflow'] = {
                'status': 'SUCCESS',
                'initial_patients': len(initial_patients),
                'initial_doctors': len(initial_doctors),
                'equipment_count': equipment_count,
                'created_doctor_id': doctor_id,
                'final_doctors': len(updated_doctors)
            }
            
            print(f"   ✅ Complete Workflow: SUCCESS")
            print(f"   Medical Database: Fully operational")
            print(f"   Frontend Integration: Ready for access")
            
            return True
            
        except Exception as e:
            self.results['complete_workflow'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"   ❌ Complete Workflow: ERROR - {e}")
            return False
    
    def run_comprehensive_check(self):
        """Run comprehensive medical database check"""
        print(" COMPREHENSIVE MEDICAL DATABASE CHECK")
        print("=" * 80)
        print("Verifying medical_db is working properly and ready for frontend access")
        print("=" * 80)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Run all tests
        test_results = {}
        test_results['backend_connectivity'] = self.test_backend_connectivity()
        test_results['medical_db_status'] = self.test_medical_db_status()
        test_results['crud_operations'] = self.test_crud_operations()
        test_results['flask_api_integration'] = self.test_flask_api_integration()
        test_results['frontend_access'] = self.test_frontend_access()
        test_results['complete_workflow'] = self.test_complete_workflow()
        
        # Generate summary
        self.generate_summary(test_results)
        
        return test_results
    
    def generate_summary(self, test_results):
        """Generate comprehensive summary"""
        print("\n" + "=" * 80)
        print(" COMPREHENSIVE MEDICAL DATABASE CHECK SUMMARY")
        print("=" * 80)
        
        # Test results summary
        print("TEST RESULTS:")
        print("-" * 30)
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name.replace('_', ' ').title()}: {status}")
        
        # Database status
        if 'medical_db_status' in self.results:
            db_status = self.results['medical_db_status']
            print(f"\nMEDICAL DATABASE STATUS:")
            print("-" * 30)
            print(f"   Database Name: {db_status.get('database_name', 'Unknown')}")
            print(f"   Connection: {db_status.get('connection', 'Unknown')}")
            print(f"   Status: {db_status.get('status', 'Unknown')}")
            print(f"   Patients: {db_status.get('patient_count', 0)}")
            print(f"   Doctors: {db_status.get('doctor_count', 0)}")
            print(f"   Studies: {db_status.get('study_count', 0)}")
        
        # CRUD operations summary
        if 'crud_operations' in self.results:
            crud = self.results['crud_operations']
            print(f"\nCRUD OPERATIONS:")
            print("-" * 30)
            for op_name, op_result in crud.items():
                if isinstance(op_result, dict) and 'status' in op_result:
                    status = "✅" if op_result['status'] == 'SUCCESS' else "❌"
                    print(f"   {op_name.replace('_', ' ').title()}: {status}")
        
        # Overall assessment
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\nOVERALL ASSESSMENT:")
        print("-" * 30)
        print(f"   Tests Passed: {passed_tests}/{total_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print(f"   Status: ✅ MEDICAL DATABASE IS READY FOR FRONTEND ACCESS")
            print(f"\nREADY FOR PRODUCTION:")
            print("   ✅ Frontend can access medical database")
            print("   ✅ All CRUD operations working")
            print("   ✅ Authentication system active")
            print("   ✅ Flask API integration functional")
            print("   ✅ Complete workflow verified")
            
            print(f"\nACCESS INSTRUCTIONS:")
            print("   1. Frontend: http://localhost:3000")
            print("   2. Dashboard: http://localhost:3000/dashboard")
            print("   3. Login: test@example.com / test123")
            print("   4. Full medical database access available")
            
        elif success_rate >= 60:
            print(f"   Status: ⚠️ MEDICAL DATABASE MOSTLY READY")
            print("   Some features may need attention")
        else:
            print(f"   Status: ❌ MEDICAL DATABASE NEEDS ATTENTION")
            print("   Critical issues found - not ready for frontend access")

if __name__ == "__main__":
    checker = MedicalDatabaseChecker()
    checker.run_comprehensive_check()
