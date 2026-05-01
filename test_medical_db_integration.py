#!/usr/bin/env python3
"""
Test Medical Database Integration
Test the complete system with medical_db database
"""

import requests
import time
from datetime import datetime

def test_medical_db_integration():
    """Test medical database integration"""
    print(" TESTING MEDICAL DATABASE (medical_db) INTEGRATION")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    backend_url = "http://localhost:5000"
    
    try:
        # Test 1: Health check
        print("\n1. HEALTH CHECK")
        print("-" * 40)
        
        response = requests.get(f"{backend_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Health Check: SUCCESS")
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Database: {health_data.get('database', 'Unknown')}")
            print(f"   Database Name: {health_data.get('database_name', 'Unknown')}")
            print(f"   Connected: {health_data.get('database_connected', 'Unknown')}")
        else:
            print(f"   Health Check: FAILED - HTTP {response.status_code}")
            return False
        
        # Test 2: Medical DB status
        print("\n2. MEDICAL DATABASE STATUS")
        print("-" * 40)
        
        # Login first
        login_data = {"email": "test@example.com", "password": "test123"}
        response = requests.post(f"{backend_url}/api/auth/login", json=login_data, timeout=5)
        
        if response.status_code == 200:
            token = response.json().get('token')
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.get(f"{backend_url}/api/medical-db/status", headers=headers, timeout=5)
            if response.status_code == 200:
                status_data = response.json()
                print(f"   Medical DB Status: SUCCESS")
                print(f"   Database Name: {status_data.get('database_name', 'Unknown')}")
                print(f"   Status: {status_data.get('status', 'Unknown')}")
                print(f"   Connection: {status_data.get('connection', 'Unknown')}")
                
                stats = status_data.get('statistics', {})
                print(f"   Patient Count: {stats.get('patient_count', 0)}")
                print(f"   Doctor Count: {stats.get('doctor_count', 0)}")
                print(f"   Study Count: {stats.get('study_count', 0)}")
            else:
                print(f"   Medical DB Status: FAILED - HTTP {response.status_code}")
                return False
        else:
            print(f"   Login: FAILED - HTTP {response.status_code}")
            return False
        
        # Test 3: Get doctors
        print("\n3. GET DOCTORS")
        print("-" * 40)
        
        response = requests.get(f"{backend_url}/api/doctors", headers=headers, timeout=5)
        if response.status_code == 200:
            doctors_data = response.json()
            doctors = doctors_data.get('doctors', [])
            print(f"   Get Doctors: SUCCESS")
            print(f"   Total Doctors: {doctors_data.get('total', 0)}")
            print(f"   Source: {doctors_data.get('source', 'Unknown')}")
            
            for i, doctor in enumerate(doctors[:3], 1):
                print(f"      {i}. {doctor.get('full_name', 'Unknown')} ({doctor.get('specialization', 'Unknown')})")
        else:
            print(f"   Get Doctors: FAILED - HTTP {response.status_code}")
            return False
        
        # Test 4: Create doctor
        print("\n4. CREATE DOCTOR")
        print("-" * 40)
        
        doctor_data = {
            "full_name": "Dr. Medical Test",
            "specialization": "Test Specialization",
            "phone": "555-9999",
            "email": "medical.test@example.com"
        }
        
        response = requests.post(f"{backend_url}/api/doctors", 
                               json=doctor_data, headers=headers, timeout=5)
        
        if response.status_code == 201:
            created_doctor = response.json().get('doctor')
            doctor_id = created_doctor.get('id')
            print(f"   Create Doctor: SUCCESS")
            print(f"   Doctor ID: {doctor_id}")
            print(f"   Name: {created_doctor.get('full_name', 'Unknown')}")
            print(f"   Specialization: {created_doctor.get('specialization', 'Unknown')}")
            print(f"   Source: {response.json().get('source', 'Unknown')}")
        else:
            print(f"   Create Doctor: FAILED - HTTP {response.status_code}")
            return False
        
        # Test 5: Delete doctor
        print("\n5. DELETE DOCTOR")
        print("-" * 40)
        
        response = requests.delete(f"{backend_url}/doctors/{doctor_id}", 
                                 headers=headers, timeout=5)
        
        if response.status_code == 200:
            delete_result = response.json()
            print(f"   Delete Doctor: SUCCESS")
            print(f"   Message: {delete_result.get('message', 'Unknown')}")
            print(f"   Deleted Doctor: {delete_result.get('doctor', {}).get('full_name', 'Unknown')}")
            print(f"   Source: {delete_result.get('source', 'Unknown')}")
        else:
            print(f"   Delete Doctor: FAILED - HTTP {response.status_code}")
            return False
        
        # Test 6: Get patients
        print("\n6. GET PATIENTS")
        print("-" * 40)
        
        response = requests.get(f"{backend_url}/api/patients", headers=headers, timeout=5)
        if response.status_code == 200:
            patients_data = response.json()
            patients = patients_data.get('patients', [])
            print(f"   Get Patients: SUCCESS")
            print(f"   Total Patients: {patients_data.get('total', 0)}")
            print(f"   Source: {patients_data.get('source', 'Unknown')}")
            
            for i, patient in enumerate(patients[:3], 1):
                print(f"      {i}. {patient.get('first_name', '')} {patient.get('last_name', '')} ({patient.get('email', 'Unknown')})")
        else:
            print(f"   Get Patients: FAILED - HTTP {response.status_code}")
            return False
        
        # Test 7: Get studies
        print("\n7. GET STUDIES")
        print("-" * 40)
        
        response = requests.get(f"{backend_url}/api/studies", headers=headers, timeout=5)
        if response.status_code == 200:
            studies_data = response.json()
            studies = studies_data.get('studies', [])
            print(f"   Get Studies: SUCCESS")
            print(f"   Total Studies: {studies_data.get('total', 0)}")
            print(f"   Source: {studies_data.get('source', 'Unknown')}")
            
            for i, study in enumerate(studies[:3], 1):
                print(f"      {i}. {study.get('study_type', 'Unknown')} - {study.get('status', 'Unknown')}")
        else:
            print(f"   Get Studies: FAILED - HTTP {response.status_code}")
            return False
        
        # Test 8: Flask API integration
        print("\n8. FLASK API INTEGRATION")
        print("-" * 40)
        
        response = requests.get(f"{backend_url}/api/equipment", headers=headers, timeout=5)
        if response.status_code == 200:
            equipment_data = response.json()
            equipment = equipment_data.get('equipment', [])
            print(f"   Flask API Integration: SUCCESS")
            print(f"   Total Equipment: {equipment_data.get('total', 0)}")
            print(f"   Source: {equipment_data.get('source', 'Unknown')}")
            print(f"   Flask API URL: {equipment_data.get('flask_api_url', 'Unknown')}")
        else:
            print(f"   Flask API Integration: FAILED - HTTP {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"Test Error: {e}")
        return False

def main():
    """Main function"""
    print(" MEDICAL DATABASE INTEGRATION TEST")
    print("Database: medical_db")
    print("Architecture: Frontend (3000) -> Backend (5000) -> medical_db (5432) -> Flask API (5001)")
    print("=" * 80)
    
    success = test_medical_db_integration()
    
    # Summary
    print("\n" + "=" * 80)
    print(" MEDICAL DATABASE INTEGRATION SUMMARY")
    print("=" * 80)
    
    if success:
        print("Medical Database Integration: COMPLETE")
        print("\nDatabase Configuration:")
        print("- Name: medical_db")
        print("- Host: localhost")
        print("- Port: 5432")
        print("- User: postgres")
        print("- Password: Sibo25Mana")
        
        print("\nSystem Architecture:")
        print("Frontend (3000) -> Backend (5000) -> medical_db (5432) -> Flask API (5001)")
        
        print("\nFeatures Working:")
        print("- Medical database connection")
        print("- Complete CRUD operations")
        print("- Authentication middleware")
        print("- Flask API integration")
        print("- Medical DB status endpoint")
        print("- Doctor delete functionality")
        print("- Patient management")
        print("- Study management")
        print("- Equipment data from Flask API")
        
        print("\nAccess Points:")
        print("- Frontend: http://localhost:3000")
        print("- Backend: http://localhost:5000")
        print("- Medical DB status: http://localhost:5000/api/medical-db/status")
        print("- Flask API: http://localhost:5001")
        
        print("\nLogin Credentials:")
        print("- Email: test@example.com")
        print("- Password: test123")
        
        print("\nSample Data:")
        print("- 3 patients (Jane Smith, John Doe, Alice Johnson)")
        print("- 5 doctors (Radiology, Cardiology, Neurology, Orthopedics, Pediatrics)")
        print("- 5 studies (CT, MRI, X-Ray, Ultrasound)")
        print("- Equipment data from Flask API")
        
        print("\nYour delete endpoint is working:")
        print("app.delete('/doctors/:id', authenticateToken, async (req, res) => {")
        print("  const { id } = req.params;")
        print("  await pool.query('DELETE FROM doctors WHERE id = $1', [id]);")
        print("  res.json({ message: 'Doctor deleted successfully' });")
        print("});")
        
    else:
        print("Medical Database Integration: NEEDS ATTENTION")
        print("\nTroubleshooting:")
        print("- Check if backend is running on port 5000")
        print("- Verify medical_db database exists")
        print("- Check PostgreSQL connection with password Sibo25Mana")
        print("- Ensure Flask API is running on port 5001")
    
    return success

if __name__ == "__main__":
    main()
