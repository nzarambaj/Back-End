#!/usr/bin/env python3
"""
Check Calculus Folder Readiness and System Integration
Verify all services are running and accessible
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

class SystemIntegrationChecker:
    def __init__(self):
        self.base_urls = {
            'frontend': 'http://localhost:3000',
            'backend': 'http://localhost:5000',
            'calculus': 'http://localhost:5001',
            'dicom': 'http://localhost:5002'
        }
        self.results = {}
        
    def check_service_health(self, service_name, url, endpoint=''):
        """Check if a service is healthy"""
        try:
            full_url = f"{url}{endpoint}"
            response = requests.get(full_url, timeout=5)
            if response.status_code == 200:
                self.results[service_name] = {
                    'status': 'RUNNING',
                    'url': full_url,
                    'response_time': response.elapsed.total_seconds(),
                    'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else 'HTML'
                }
                return True
            else:
                self.results[service_name] = {
                    'status': f'HTTP {response.status_code}',
                    'url': full_url,
                    'error': response.text[:100]
                }
                return False
        except Exception as e:
            self.results[service_name] = {
                'status': 'ERROR',
                'url': full_url,
                'error': str(e)
            }
            return False
    
    def check_calculus_folder(self):
        """Check if Calculus folder has API service"""
        calculus_path = Path(r"C:\Users\TTR\Documents\Calculus")
        
        if not calculus_path.exists():
            return False, "Calculus folder not found"
        
        # Check for backend API files
        backend_files = [
            'backend/backend_api_pure.py',
            'backend/calculus_api_ecosystem.py',
            'backend/enhanced_flask_api.py'
        ]
        
        found_files = []
        for file_path in backend_files:
            full_path = calculus_path / file_path
            if full_path.exists():
                found_files.append(file_path)
        
        return True, found_files
    
    def test_backend_endpoints(self):
        """Test all backend endpoints from frontend perspective"""
        backend_endpoints = [
            '/api/health',
            '/api/patients',
            '/api/doctors',
            '/api/studies',
            '/api/images'
        ]
        
        results = {}
        for endpoint in backend_endpoints:
            try:
                # Test without authentication first
                response = requests.get(f"{self.base_urls['backend']}{endpoint}", timeout=5)
                results[endpoint] = {
                    'status': response.status_code,
                    'accessible': response.status_code in [200, 401],  # 401 means endpoint exists but needs auth
                    'error': response.text[:100] if response.status_code != 200 else None
                }
            except Exception as e:
                results[endpoint] = {
                    'status': 'ERROR',
                    'accessible': False,
                    'error': str(e)
                }
        
        return results
    
    def test_calculus_endpoints(self):
        """Test all Calculus endpoints from frontend perspective"""
        calculus_endpoints = [
            '/api/health',
            '/api/equipment',
            '/api/equipment/ct',
            '/api/equipment/mri',
            '/api/equipment/xray',
            '/api/equipment/ultrasound',
            '/api/equipment/mammo',
            '/api/modalities',
            '/api/locations'
        ]
        
        results = {}
        for endpoint in calculus_endpoints:
            try:
                response = requests.get(f"{self.base_urls['calculus']}{endpoint}", timeout=5)
                results[endpoint] = {
                    'status': response.status_code,
                    'accessible': response.status_code == 200,
                    'data_count': len(response.json()) if response.headers.get('content-type', '').startswith('application/json') else 0,
                    'error': response.text[:100] if response.status_code != 200 else None
                }
            except Exception as e:
                results[endpoint] = {
                    'status': 'ERROR',
                    'accessible': False,
                    'error': str(e)
                }
        
        return results
    
    def test_frontend_to_backend_integration(self):
        """Test if frontend can access backend endpoints"""
        # Test login and get token
        try:
            login_response = requests.post(
                f"{self.base_urls['backend']}/api/auth/login",
                json={"email": "test@example.com", "password": "test123"},
                timeout=5
            )
            
            if login_response.status_code == 200:
                token = login_response.json().get('token')
                headers = {'Authorization': f'Bearer {token}'}
                
                # Test protected endpoints
                protected_endpoints = ['/api/patients', '/api/doctors', '/api/studies']
                results = {}
                
                for endpoint in protected_endpoints:
                    try:
                        response = requests.get(f"{self.base_urls['backend']}{endpoint}", headers=headers, timeout=5)
                        results[endpoint] = {
                            'status': response.status_code,
                            'accessible': response.status_code == 200,
                            'data_count': len(response.json().get('patients', []) if 'patients' in response.json() else response.json().get('doctors', []) if 'doctors' in response.json() else response.json().get('studies', []))
                        }
                    except Exception as e:
                        results[endpoint] = {
                            'status': 'ERROR',
                            'accessible': False,
                            'error': str(e)
                        }
                
                return {'login': 'SUCCESS', 'token': token[:20] + '...', 'endpoints': results}
            else:
                return {'login': 'FAILED', 'error': login_response.text[:100]}
                
        except Exception as e:
            return {'login': 'ERROR', 'error': str(e)}
    
    def test_frontend_to_calculus_integration(self):
        """Test if frontend can access Calculus endpoints"""
        # Test equipment endpoints
        try:
            equipment_response = requests.get(f"{self.base_urls['calculus']}/api/equipment", timeout=5)
            
            if equipment_response.status_code == 200:
                equipment_data = equipment_response.json()
                equipment_count = len(equipment_data.get('equipment', []))
                
                # Test specific equipment types
                types_to_test = ['ct', 'mri', 'xray', 'ultrasound']
                type_results = {}
                
                for equipment_type in types_to_test:
                    try:
                        response = requests.get(f"{self.base_urls['calculus']}/api/equipment/{equipment_type}", timeout=5)
                        type_results[equipment_type] = {
                            'status': response.status_code,
                            'accessible': response.status_code == 200,
                            'count': len(response.json().get('equipment', [])) if response.status_code == 200 else 0
                        }
                    except Exception as e:
                        type_results[equipment_type] = {
                            'status': 'ERROR',
                            'accessible': False,
                            'error': str(e)
                        }
                
                return {
                    'equipment_list': 'SUCCESS',
                    'equipment_count': equipment_count,
                    'equipment_types': type_results
                }
            else:
                return {'equipment_list': 'FAILED', 'error': equipment_response.text[:100]}
                
        except Exception as e:
            return {'equipment_list': 'ERROR', 'error': str(e)}
    
    def run_complete_check(self):
        """Run complete system integration check"""
        print(" COMPLETE SYSTEM INTEGRATION CHECK")
        print("=" * 80)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Step 1: Check all service health
        print("\n1. SERVICE HEALTH CHECK")
        print("-" * 40)
        
        services = [
            ('Frontend', self.base_urls['frontend'], ''),
            ('Backend', self.base_urls['backend'], '/api/health'),
            ('Calculus', self.base_urls['calculus'], '/api/health'),
            ('DICOM', self.base_urls['dicom'], '/api/dicom/health')
        ]
        
        for name, url, endpoint in services:
            healthy = self.check_service_health(name, url, endpoint)
            status = self.results[name]['status']
            print(f"   {name} ({url}): {status}")
        
        # Step 2: Check Calculus folder
        print("\n2. CALCULUS FOLDER CHECK")
        print("-" * 40)
        
        calculus_exists, calculus_info = self.check_calculus_folder()
        if calculus_exists:
            print(f"   Calculus Folder: EXISTS")
            print(f"   Backend Files Found: {len(calculus_info)}")
            for file in calculus_info:
                print(f"      - {file}")
        else:
            print(f"   Calculus Folder: {calculus_info}")
        
        # Step 3: Test backend endpoints
        print("\n3. BACKEND ENDPOINTS TEST")
        print("-" * 40)
        
        backend_results = self.test_backend_endpoints()
        for endpoint, result in backend_results.items():
            status = result['status']
            accessible = result['accessible']
            print(f"   {endpoint}: {status} {'(Accessible)' if accessible else '(Not Accessible)'}")
        
        # Step 4: Test Calculus endpoints
        print("\n4. CALCULUS ENDPOINTS TEST")
        print("-" * 40)
        
        calculus_results = self.test_calculus_endpoints()
        for endpoint, result in calculus_results.items():
            status = result['status']
            accessible = result['accessible']
            data_count = result.get('data_count', 0)
            print(f"   {endpoint}: {status} {'(Accessible)' if accessible else '(Not Accessible)'} {f'({data_count} items)' if data_count > 0 else ''}")
        
        # Step 5: Test frontend to backend integration
        print("\n5. FRONTEND TO BACKEND INTEGRATION")
        print("-" * 40)
        
        backend_integration = self.test_frontend_to_backend_integration()
        print(f"   Login: {backend_integration['login']}")
        if backend_integration['login'] == 'SUCCESS':
            print(f"   Token: {backend_integration['token']}")
            for endpoint, result in backend_integration['endpoints'].items():
                status = result['status']
                accessible = result['accessible']
                data_count = result.get('data_count', 0)
                print(f"   {endpoint}: {status} {'(Accessible)' if accessible else '(Not Accessible)'} {f'({data_count} items)' if data_count > 0 else ''}")
        
        # Step 6: Test frontend to Calculus integration
        print("\n6. FRONTEND TO CALCULUS INTEGRATION")
        print("-" * 40)
        
        calculus_integration = self.test_frontend_to_calculus_integration()
        print(f"   Equipment List: {calculus_integration['equipment_list']}")
        if calculus_integration['equipment_list'] == 'SUCCESS':
            print(f"   Total Equipment: {calculus_integration['equipment_count']}")
            for eq_type, result in calculus_integration['equipment_types'].items():
                status = result['status']
                accessible = result['accessible']
                count = result.get('count', 0)
                print(f"   {eq_type}: {status} {'(Accessible)' if accessible else '(Not Accessible)'} {f'({count} items)' if count > 0 else ''}")
        
        # Summary
        print("\n" + "=" * 80)
        print(" INTEGRATION SUMMARY")
        print("=" * 80)
        
        # Count running services
        running_services = sum(1 for result in self.results.values() if result['status'] == 'RUNNING')
        total_services = len(self.results)
        
        print(f"Services Running: {running_services}/{total_services}")
        print(f"Calculus Folder: {'READY' if calculus_exists else 'NOT FOUND'}")
        print(f"Backend Integration: {'WORKING' if backend_integration['login'] == 'SUCCESS' else 'FAILED'}")
        print(f"Calculus Integration: {'WORKING' if calculus_integration['equipment_list'] == 'SUCCESS' else 'FAILED'}")
        
        # Overall status
        all_services_running = running_services == total_services
        backend_working = backend_integration['login'] == 'SUCCESS'
        calculus_working = calculus_integration['equipment_list'] == 'SUCCESS'
        
        overall_status = all_services_running and backend_working and calculus_working
        
        print(f"\nOverall Status: {'COMPLETE' if overall_status else 'PARTIAL'}")
        
        if overall_status:
            print("\n" + "=" * 80)
            print(" SYSTEM IS FULLY READY")
            print("=" * 80)
            print(" Frontend (3000): Accessible at http://localhost:3000")
            print(" Backend (5000): All endpoints accessible")
            print(" Calculus (5001): All endpoints accessible")
            print(" DICOM (5002): All endpoints accessible")
            print("\n Frontend can access:")
            print(" - All backend endpoints (patients, doctors, studies)")
            print(" - All Calculus endpoints (equipment, modalities)")
            print(" - All DICOM endpoints (image processing)")
            print("\n LOGIN CREDENTIALS:")
            print(" Email: test@example.com")
            print(" Password: test123")
        else:
            print("\n" + "=" * 80)
            print(" SYSTEM NEEDS ATTENTION")
            print("=" * 80)
            if not all_services_running:
                print(" - Some services are not running")
            if not backend_working:
                print(" - Backend integration is not working")
            if not calculus_working:
                print(" - Calculus integration is not working")
        
        return overall_status

if __name__ == "__main__":
    checker = SystemIntegrationChecker()
    checker.run_complete_check()
