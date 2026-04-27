#!/usr/bin/env python3
"""
Sample data population script for Medical Imaging System
Run this to add test data to the database for API testing
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def create_sample_data():
    print("Creating sample data for Medical Imaging System API...")

    # Sample Radiologist
    radiologist_data = {
        "firstName": "Dr. Michael",
        "lastName": "Rodriguez",
        "email": "michael.rodriguez@hospital.com",
        "phone": "+1-555-0101",
        "licenseNumber": "RAD123456",
        "department": "Radiology",
        "specialty": "Diagnostic Radiology",
        "subspecialty": "Abdominal Imaging",
        "boardCertification": "ABR Certified",
        "fellowshipTraining": "Abdominal Imaging Fellowship",
        "yearsExperience": 12,
        "academicTitle": "Assistant Professor"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/medical-staff/radiologists", json=radiologist_data)
        if response.status_code == 201:
            radiologist = response.json()
            radiologist_id = radiologist['id']
            print(f"✅ Created radiologist: {radiologist['firstName']} {radiologist['lastName']} (ID: {radiologist_id})")
        else:
            print(f"❌ Failed to create radiologist: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating radiologist: {e}")
        return

    # Sample Referring Doctor
    doctor_data = {
        "firstName": "Dr. Jennifer",
        "lastName": "Williams",
        "email": "jennifer.williams@clinic.com",
        "phone": "+1-555-0202",
        "medicalLicense": "MD789012",
        "department": "Internal Medicine",
        "specialty": "Gastroenterology",
        "practiceName": "Williams GI Clinic",
        "npiNumber": "1234567890",
        "deaNumber": "JW1234567"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/medical-staff/referring-doctors", json=doctor_data)
        if response.status_code == 201:
            doctor = response.json()
            doctor_id = doctor['id']
            print(f"✅ Created referring doctor: {doctor['firstName']} {doctor['lastName']} (ID: {doctor_id})")
        else:
            print(f"❌ Failed to create referring doctor: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating referring doctor: {e}")
        return

    # Sample Imaging Technician
    technician_data = {
        "firstName": "Lisa",
        "lastName": "Thompson",
        "email": "lisa.thompson@hospital.com",
        "phone": "+1-555-0303",
        "certificationNumber": "TECH456789",
        "department": "Radiology",
        "certificationType": "ARRT",
        "modalities": ["CT", "MRI", "X-Ray"],
        "certificationExpiry": "2026-12-31",
        "advancedCertifications": ["CT Certified", "MRI Certified"],
        "shiftSchedule": "Day Shift"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/medical-staff/imaging-technicians", json=technician_data)
        if response.status_code == 201:
            technician = response.json()
            technician_id = technician['id']
            print(f"✅ Created imaging technician: {technician['firstName']} {technician['lastName']} (ID: {technician_id})")
        else:
            print(f"❌ Failed to create imaging technician: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating imaging technician: {e}")
        return

    # Sample Patient
    patient_data = {
        "firstName": "Robert",
        "lastName": "Johnson",
        "dateOfBirth": "1975-08-15",
        "gender": "M",
        "phone": "+1-555-0404",
        "email": "robert.johnson@email.com",
        "address": {
            "street": "456 Oak Avenue",
            "city": "Springfield",
            "postalCode": "62701",
            "country": "USA"
        },
        "medicalRecordNumber": "MRN001"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/patients", json=patient_data)
        if response.status_code == 201:
            patient = response.json()
            patient_id = patient['id']
            print(f"✅ Created patient: {patient['firstName']} {patient['lastName']} (ID: {patient_id})")
        else:
            print(f"❌ Failed to create patient: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating patient: {e}")
        return

    # Sample Doctor (Professional API)
    pro_doctor_data = {
        "firstName": "Dr. David",
        "lastName": "Lee",
        "specialty": "Radiology",
        "licenseNumber": "DOC789012",
        "email": "david.lee@hospital.com",
        "phone": "+1-555-0505"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/doctors", json=pro_doctor_data)
        if response.status_code == 201:
            pro_doctor = response.json()
            pro_doctor_id = pro_doctor['id']
            print(f"✅ Created professional doctor: {pro_doctor['firstName']} {pro_doctor['lastName']} (ID: {pro_doctor_id})")
        else:
            print(f"❌ Failed to create professional doctor: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating professional doctor: {e}")
        return

    # Sample Study
    study_data = {
        "patientId": str(patient_id),
        "doctorId": str(pro_doctor_id),
        "studyDate": "2024-01-15T14:30:00Z",
        "modality": "CT",
        "bodyPart": "Abdomen",
        "status": "completed",
        "clinicalIndication": "Abdominal pain evaluation",
        "report": {
            "status": "finalized",
            "summary": "CT abdomen shows no acute abnormalities"
        }
    }

    try:
        response = requests.post(f"{BASE_URL}/api/studies", json=study_data)
        if response.status_code == 201:
            study = response.json()
            study_id = study['id']
            print(f"✅ Created study: {study['modality']} {study['bodyPart']} (ID: {study_id})")
        else:
            print(f"❌ Failed to create study: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating study: {e}")
        return

    # Sample Window Preset
    preset_data = {
        "modality": "CT",
        "name": "Abdomen Window",
        "windowCenter": 40,
        "windowWidth": 400,
        "description": "Standard abdominal CT window settings"
    }

    try:
        response = requests.post(f"{BASE_URL}/settings/presets", json=preset_data)
        if response.status_code == 201:
            preset = response.json()
            print(f"✅ Created window preset: {preset['name']}")
        else:
            print(f"❌ Failed to create preset: {response.text}")
    except Exception as e:
        print(f"❌ Error creating preset: {e}")

    # Sample MWL Patient
    mwl_patient_data = {
        "patient_id": "MWL001",
        "name": "Test Patient",
        "birth_date": "1980-05-10",
        "sex": "M"
    }

    try:
        response = requests.post(f"{BASE_URL}/mwl/patients", json=mwl_patient_data)
        if response.status_code == 201:
            mwl_patient = response.json()
            print(f"✅ Created MWL patient: {mwl_patient['name']} (ID: {mwl_patient['id']})")
        else:
            print(f"❌ Failed to create MWL patient: {response.text}")
    except Exception as e:
        print(f"❌ Error creating MWL patient: {e}")

    print("\n🎉 Sample data creation completed!")
    print("You can now test all API endpoints with Postman using the collection file.")
    print("The API is running at: http://localhost:5000")

if __name__ == "__main__":
    create_sample_data()