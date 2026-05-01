#!/usr/bin/env python3
"""
Comprehensive Flask API for Medical Imaging System
Deep folder structure with extensive API endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import uuid
import json

app = Flask(__name__)
CORS(app)

# Sample data for comprehensive API
PATIENTS_DATA = [
    {
        "id": 1,
        "patient_id": "PAT001",
        "first_name": "Jane",
        "last_name": "Smith",
        "date_of_birth": "1990-05-15",
        "gender": "F",
        "email": "jane.smith@example.com",
        "phone": "555-0101",
        "address": "456 Oak Ave",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62701",
        "blood_type": "O+",
        "emergency_contact": "John Smith",
        "emergency_phone": "555-0102",
        "insurance_id": "INS001",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    {
        "id": 2,
        "patient_id": "PAT002",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1985-03-20",
        "gender": "M",
        "email": "john.doe@example.com",
        "phone": "555-0103",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345",
        "blood_type": "A+",
        "emergency_contact": "Jane Doe",
        "emergency_phone": "555-0104",
        "insurance_id": "INS002",
        "created_at": "2024-01-02T11:00:00Z",
        "updated_at": "2024-01-02T11:00:00Z"
    }
]

DOCTORS_DATA = [
    {
        "id": 1,
        "doctor_id": "DOC001",
        "first_name": "John",
        "last_name": "Wilson",
        "specialization": "Radiology",
        "license_number": "LIC001",
        "phone": "555-0201",
        "email": "john.wilson@medical.com",
        "department": "Radiology",
        "experience_years": 15,
        "education": "MD - Harvard Medical School",
        "certifications": ["ABR", "FACR"],
        "created_at": "2024-01-01T09:00:00Z",
        "updated_at": "2024-01-01T09:00:00Z"
    },
    {
        "id": 2,
        "doctor_id": "DOC002",
        "first_name": "Sarah",
        "last_name": "Johnson",
        "specialization": "Cardiology",
        "license_number": "LIC002",
        "phone": "555-0202",
        "email": "sarah.johnson@medical.com",
        "department": "Cardiology",
        "experience_years": 12,
        "education": "MD - Johns Hopkins",
        "certifications": ["ABIM", "FACC"],
        "created_at": "2024-01-01T09:30:00Z",
        "updated_at": "2024-01-01T09:30:00Z"
    }
]

STUDIES_DATA = [
    {
        "id": 1,
        "study_id": "STU001",
        "patient_id": "PAT001",
        "doctor_id": "DOC001",
        "study_type": "CT",
        "study_date": "2024-01-15",
        "description": "Chest CT scan",
        "status": "completed",
        "priority": "routine",
        "clinical_indication": "Chest pain evaluation",
        "contrast_used": True,
        "radiation_dose": "2.5 mSv",
        "technician": "Tech001",
        "report_status": "final",
        "created_at": "2024-01-15T14:00:00Z",
        "updated_at": "2024-01-15T16:30:00Z"
    },
    {
        "id": 2,
        "study_id": "STU002",
        "patient_id": "PAT002",
        "doctor_id": "DOC002",
        "study_type": "MRI",
        "study_date": "2024-01-20",
        "description": "Brain MRI",
        "status": "completed",
        "priority": "urgent",
        "clinical_indication": "Headache evaluation",
        "contrast_used": False,
        "radiation_dose": "0 mSv",
        "technician": "Tech002",
        "report_status": "preliminary",
        "created_at": "2024-01-20T10:00:00Z",
        "updated_at": "2024-01-20T15:00:00Z"
    }
]

IMAGES_DATA = [
    {
        "id": 1,
        "image_id": "IMG001",
        "study_id": "STU001",
        "patient_id": "PAT001",
        "image_type": "CT",
        "series_number": 1,
        "slice_thickness": "1.0mm",
        "pixel_spacing": "0.5mm",
        "acquisition_date": "2024-01-15T14:30:00Z",
        "file_size": 524288,
        "file_format": "DICOM",
        "storage_path": "/images/2024/01/15/IMG001.dcm",
        "compression": "lossless",
        "quality_score": 95,
        "created_at": "2024-01-15T14:30:00Z"
    },
    {
        "id": 2,
        "image_id": "IMG002",
        "study_id": "STU002",
        "patient_id": "PAT002",
        "image_type": "MRI",
        "series_number": 1,
        "slice_thickness": "3.0mm",
        "pixel_spacing": "1.0mm",
        "acquisition_date": "2024-01-20T10:30:00Z",
        "file_size": 1048576,
        "file_format": "DICOM",
        "storage_path": "/images/2024/01/20/IMG002.dcm",
        "compression": "lossless",
        "quality_score": 92,
        "created_at": "2024-01-20T10:30:00Z"
    }
]

EQUIPMENT_DATA = [
    {
        "id": 1,
        "equipment_id": "EQ001",
        "name": "CT Scanner",
        "type": "Imaging",
        "model": "SOMATOM Definition Edge",
        "manufacturer": "Siemens",
        "serial_number": "SN001",
        "installation_date": "2023-01-15",
        "status": "Active",
        "location": "Radiology Department",
        "room": "CT-001",
        "maintenance_schedule": "monthly",
        "last_maintenance": "2024-01-01",
        "next_maintenance": "2024-02-01",
        "operator": "Tech001",
        "software_version": "VA30",
        "created_at": "2023-01-15T09:00:00Z"
    },
    {
        "id": 2,
        "equipment_id": "EQ002",
        "name": "MRI Machine",
        "type": "Imaging",
        "model": "Signa Pioneer",
        "manufacturer": "GE Healthcare",
        "serial_number": "SN002",
        "installation_date": "2023-02-20",
        "status": "Active",
        "location": "Radiology Department",
        "room": "MRI-001",
        "maintenance_schedule": "quarterly",
        "last_maintenance": "2024-01-10",
        "next_maintenance": "2024-04-10",
        "operator": "Tech002",
        "software_version": "28.0",
        "created_at": "2023-02-20T10:00:00Z"
    }
]

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Comprehensive Medical Imaging API",
        "version": "2.0.0",
        "description": "Deep folder structure with extensive medical imaging endpoints",
        "base_url": "http://localhost:5001",
        "endpoints": {
            "health": "/api/health",
            "patients": {
                "list": "/api/patients",
                "by_id": "/api/patients/<id>",
                "by_patient_id": "/api/patients/patient_id/<patient_id>",
                "search": "/api/patients/search"
            },
            "doctors": {
                "list": "/api/doctors",
                "by_id": "/api/doctors/<id>",
                "by_specialization": "/api/doctors/specialization/<specialization>",
                "search": "/api/doctors/search"
            },
            "studies": {
                "list": "/api/studies",
                "by_id": "/api/studies/<id>",
                "by_patient": "/api/studies/patient/<patient_id>",
                "by_doctor": "/api/studies/doctor/<doctor_id>",
                "by_type": "/api/studies/type/<study_type>",
                "search": "/api/studies/search"
            },
            "images": {
                "list": "/api/images",
                "by_id": "/api/images/<id>",
                "by_study": "/api/images/study/<study_id>",
                "by_patient": "/api/images/patient/<patient_id>",
                "by_type": "/api/images/type/<image_type>",
                "search": "/api/images/search"
            },
            "equipment": {
                "list": "/api/equipment",
                "by_id": "/api/equipment/<id>",
                "by_type": "/api/equipment/type/<equipment_type>",
                "by_status": "/api/equipment/status/<status>",
                "search": "/api/equipment/search"
            },
            "reports": {
                "list": "/api/reports",
                "by_study": "/api/reports/study/<study_id>",
                "by_patient": "/api/reports/patient/<patient_id>",
                "by_doctor": "/api/reports/doctor/<doctor_id>"
            },
            "analytics": {
                "statistics": "/api/analytics/statistics",
                "usage": "/api/analytics/usage",
                "performance": "/api/analytics/performance"
            }
        },
        "timestamp": datetime.datetime.now().isoformat()
    })

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Comprehensive Medical Imaging API",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "2.0.0",
        "port": 5001,
        "database_status": "connected",
        "memory_usage": "normal",
        "cpu_usage": "low"
    })

# Patient endpoints
@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients"""
    return jsonify({
        "patients": PATIENTS_DATA,
        "total": len(PATIENTS_DATA),
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    """Get patient by ID"""
    patient = next((p for p in PATIENTS_DATA if p["id"] == patient_id), None)
    if patient:
        return jsonify({
            "patient": patient,
            "source": "Flask API"
        })
    else:
        return jsonify({"error": "Patient not found"}), 404

@app.route('/api/patients/patient_id/<patient_id>', methods=['GET'])
def get_patient_by_patient_id(patient_id):
    """Get patient by patient_id"""
    patient = next((p for p in PATIENTS_DATA if p["patient_id"] == patient_id), None)
    if patient:
        return jsonify({
            "patient": patient,
            "source": "Flask API"
        })
    else:
        return jsonify({"error": "Patient not found"}), 404

@app.route('/api/patients/search', methods=['GET'])
def search_patients():
    """Search patients"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = [p for p in PATIENTS_DATA if 
              query in p['first_name'].lower() or 
              query in p['last_name'].lower() or
              query in p['email'].lower()]
    
    return jsonify({
        "patients": results,
        "total": len(results),
        "query": query,
        "source": "Flask API"
    })

# Doctor endpoints
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get all doctors"""
    return jsonify({
        "doctors": DOCTORS_DATA,
        "total": len(DOCTORS_DATA),
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    """Get doctor by ID"""
    doctor = next((d for d in DOCTORS_DATA if d["id"] == doctor_id), None)
    if doctor:
        return jsonify({
            "doctor": doctor,
            "source": "Flask API"
        })
    else:
        return jsonify({"error": "Doctor not found"}), 404

@app.route('/api/doctors/specialization/<specialization>', methods=['GET'])
def get_doctors_by_specialization(specialization):
    """Get doctors by specialization"""
    doctors = [d for d in DOCTORS_DATA if d["specialization"].lower() == specialization.lower()]
    return jsonify({
        "doctors": doctors,
        "total": len(doctors),
        "specialization": specialization,
        "source": "Flask API"
    })

@app.route('/api/doctors/search', methods=['GET'])
def search_doctors():
    """Search doctors"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = [d for d in DOCTORS_DATA if 
              query in d['first_name'].lower() or 
              query in d['last_name'].lower() or
              query in d['specialization'].lower()]
    
    return jsonify({
        "doctors": results,
        "total": len(results),
        "query": query,
        "source": "Flask API"
    })

# Study endpoints
@app.route('/api/studies', methods=['GET'])
def get_studies():
    """Get all studies"""
    return jsonify({
        "studies": STUDIES_DATA,
        "total": len(STUDIES_DATA),
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/studies/<int:study_id>', methods=['GET'])
def get_study_by_id(study_id):
    """Get study by ID"""
    study = next((s for s in STUDIES_DATA if s["id"] == study_id), None)
    if study:
        return jsonify({
            "study": study,
            "source": "Flask API"
        })
    else:
        return jsonify({"error": "Study not found"}), 404

@app.route('/api/studies/patient/<patient_id>', methods=['GET'])
def get_studies_by_patient(patient_id):
    """Get studies by patient_id"""
    studies = [s for s in STUDIES_DATA if s["patient_id"] == patient_id]
    return jsonify({
        "studies": studies,
        "total": len(studies),
        "patient_id": patient_id,
        "source": "Flask API"
    })

@app.route('/api/studies/doctor/<doctor_id>', methods=['GET'])
def get_studies_by_doctor(doctor_id):
    """Get studies by doctor_id"""
    studies = [s for s in STUDIES_DATA if s["doctor_id"] == doctor_id]
    return jsonify({
        "studies": studies,
        "total": len(studies),
        "doctor_id": doctor_id,
        "source": "Flask API"
    })

@app.route('/api/studies/type/<study_type>', methods=['GET'])
def get_studies_by_type(study_type):
    """Get studies by type"""
    studies = [s for s in STUDIES_DATA if s["study_type"].lower() == study_type.lower()]
    return jsonify({
        "studies": studies,
        "total": len(studies),
        "study_type": study_type,
        "source": "Flask API"
    })

@app.route('/api/studies/search', methods=['GET'])
def search_studies():
    """Search studies"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = [s for s in STUDIES_DATA if 
              query in s['study_type'].lower() or 
              query in s['description'].lower() or
              query in s['status'].lower()]
    
    return jsonify({
        "studies": results,
        "total": len(results),
        "query": query,
        "source": "Flask API"
    })

# Image endpoints
@app.route('/api/images', methods=['GET'])
def get_images():
    """Get all images"""
    return jsonify({
        "images": IMAGES_DATA,
        "total": len(IMAGES_DATA),
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/images/<int:image_id>', methods=['GET'])
def get_image_by_id(image_id):
    """Get image by ID"""
    image = next((img for img in IMAGES_DATA if img["id"] == image_id), None)
    if image:
        return jsonify({
            "image": image,
            "source": "Flask API"
        })
    else:
        return jsonify({"error": "Image not found"}), 404

@app.route('/api/images/study/<study_id>', methods=['GET'])
def get_images_by_study(study_id):
    """Get images by study_id"""
    images = [img for img in IMAGES_DATA if img["study_id"] == study_id]
    return jsonify({
        "images": images,
        "total": len(images),
        "study_id": study_id,
        "source": "Flask API"
    })

@app.route('/api/images/patient/<patient_id>', methods=['GET'])
def get_images_by_patient(patient_id):
    """Get images by patient_id"""
    images = [img for img in IMAGES_DATA if img["patient_id"] == patient_id]
    return jsonify({
        "images": images,
        "total": len(images),
        "patient_id": patient_id,
        "source": "Flask API"
    })

@app.route('/api/images/type/<image_type>', methods=['GET'])
def get_images_by_type(image_type):
    """Get images by type"""
    images = [img for img in IMAGES_DATA if img["image_type"].lower() == image_type.lower()]
    return jsonify({
        "images": images,
        "total": len(images),
        "image_type": image_type,
        "source": "Flask API"
    })

@app.route('/api/images/search', methods=['GET'])
def search_images():
    """Search images"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = [img for img in IMAGES_DATA if 
              query in img['image_type'].lower() or 
              query in img['file_format'].lower()]
    
    return jsonify({
        "images": results,
        "total": len(results),
        "query": query,
        "source": "Flask API"
    })

# Equipment endpoints
@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    """Get all equipment"""
    return jsonify({
        "equipment": EQUIPMENT_DATA,
        "total": len(EQUIPMENT_DATA),
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """Get equipment by ID"""
    equipment = next((eq for eq in EQUIPMENT_DATA if eq["id"] == equipment_id), None)
    if equipment:
        return jsonify({
            "equipment": equipment,
            "source": "Flask API"
        })
    else:
        return jsonify({"error": "Equipment not found"}), 404

@app.route('/api/equipment/type/<equipment_type>', methods=['GET'])
def get_equipment_by_type(equipment_type):
    """Get equipment by type"""
    equipment = [eq for eq in EQUIPMENT_DATA if eq["type"].lower() == equipment_type.lower()]
    return jsonify({
        "equipment": equipment,
        "total": len(equipment),
        "equipment_type": equipment_type,
        "source": "Flask API"
    })

@app.route('/api/equipment/status/<status>', methods=['GET'])
def get_equipment_by_status(status):
    """Get equipment by status"""
    equipment = [eq for eq in EQUIPMENT_DATA if eq["status"].lower() == status.lower()]
    return jsonify({
        "equipment": equipment,
        "total": len(equipment),
        "status": status,
        "source": "Flask API"
    })

@app.route('/api/equipment/search', methods=['GET'])
def search_equipment():
    """Search equipment"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = [eq for eq in EQUIPMENT_DATA if 
              query in eq['name'].lower() or 
              query in eq['manufacturer'].lower() or
              query in eq['model'].lower()]
    
    return jsonify({
        "equipment": results,
        "total": len(results),
        "query": query,
        "source": "Flask API"
    })

# Report endpoints
@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get all reports"""
    # Generate sample reports based on studies
    reports = []
    for study in STUDIES_DATA:
        report = {
            "id": study["id"],
            "report_id": f"RPT{study['id']:03d}",
            "study_id": study["study_id"],
            "patient_id": study["patient_id"],
            "doctor_id": study["doctor_id"],
            "report_type": study["study_type"],
            "findings": f"Normal {study['study_type']} findings" if study["status"] == "completed" else "Study in progress",
            "impression": "No acute pathology detected" if study["status"] == "completed" else "Awaiting completion",
            "recommendations": "Follow up as needed" if study["status"] == "completed" else "Complete study first",
            "report_status": study["report_status"],
            "radiologist": f"Dr. {DOCTORS_DATA[0]['first_name']} {DOCTORS_DATA[0]['last_name']}",
            "report_date": study["updated_at"],
            "created_at": study["created_at"],
            "updated_at": study["updated_at"]
        }
        reports.append(report)
    
    return jsonify({
        "reports": reports,
        "total": len(reports),
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/reports/study/<study_id>', methods=['GET'])
def get_reports_by_study(study_id):
    """Get reports by study_id"""
    reports_response = get_reports()
    all_reports = reports_response.get_json()["reports"]
    reports = [r for r in all_reports if r["study_id"] == study_id]
    
    return jsonify({
        "reports": reports,
        "total": len(reports),
        "study_id": study_id,
        "source": "Flask API"
    })

@app.route('/api/reports/patient/<patient_id>', methods=['GET'])
def get_reports_by_patient(patient_id):
    """Get reports by patient_id"""
    reports_response = get_reports()
    all_reports = reports_response.get_json()["reports"]
    reports = [r for r in all_reports if r["patient_id"] == patient_id]
    
    return jsonify({
        "reports": reports,
        "total": len(reports),
        "patient_id": patient_id,
        "source": "Flask API"
    })

@app.route('/api/reports/doctor/<doctor_id>', methods=['GET'])
def get_reports_by_doctor(doctor_id):
    """Get reports by doctor_id"""
    reports_response = get_reports()
    all_reports = reports_response.get_json()["reports"]
    reports = [r for r in all_reports if r["doctor_id"] == doctor_id]
    
    return jsonify({
        "reports": reports,
        "total": len(reports),
        "doctor_id": doctor_id,
        "source": "Flask API"
    })

# Analytics endpoints
@app.route('/api/analytics/statistics', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    return jsonify({
        "statistics": {
            "total_patients": len(PATIENTS_DATA),
            "total_doctors": len(DOCTORS_DATA),
            "total_studies": len(STUDIES_DATA),
            "total_images": len(IMAGES_DATA),
            "total_equipment": len(EQUIPMENT_DATA),
            "studies_by_type": {
                "CT": len([s for s in STUDIES_DATA if s["study_type"] == "CT"]),
                "MRI": len([s for s in STUDIES_DATA if s["study_type"] == "MRI"]),
                "X-Ray": len([s for s in STUDIES_DATA if s["study_type"] == "X-Ray"]),
                "Ultrasound": len([s for s in STUDIES_DATA if s["study_type"] == "Ultrasound"])
            },
            "equipment_by_status": {
                "Active": len([eq for eq in EQUIPMENT_DATA if eq["status"] == "Active"]),
                "Maintenance": len([eq for eq in EQUIPMENT_DATA if eq["status"] == "Maintenance"]),
                "Inactive": len([eq for eq in EQUIPMENT_DATA if eq["status"] == "Inactive"])
            }
        },
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/analytics/usage', methods=['GET'])
def get_usage_analytics():
    """Get usage analytics"""
    return jsonify({
        "usage": {
            "daily_studies": 15,
            "weekly_studies": 85,
            "monthly_studies": 320,
            "average_study_duration": "45 minutes",
            "peak_hours": "09:00-17:00",
            "busiest_day": "Monday",
            "equipment_utilization": {
                "CT Scanner": 78,
                "MRI Machine": 65,
                "X-Ray Machine": 82,
                "Ultrasound Machine": 71
            }
        },
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/analytics/performance', methods=['GET'])
def get_performance_metrics():
    """Get performance metrics"""
    return jsonify({
        "performance": {
            "api_response_time": "45ms",
            "database_query_time": "12ms",
            "image_processing_time": "2.3s",
            "system_uptime": "99.8%",
            "error_rate": "0.2%",
            "concurrent_users": 45,
            "memory_usage": "68%",
            "cpu_usage": "23%",
            "storage_usage": "45%",
            "network_bandwidth": "125 Mbps"
        },
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Comprehensive Medical Imaging API...")
    print("Port: 5001")
    print("Health: http://localhost:5001/api/health")
    print("Equipment: http://localhost:5001/api/equipment")
    print("Patients: http://localhost:5001/api/patients")
    print("Doctors: http://localhost:5001/api/doctors")
    print("Studies: http://localhost:5001/api/studies")
    print("Images: http://localhost:5001/api/images")
    print("Reports: http://localhost:5001/api/reports")
    print("Analytics: http://localhost:5001/api/analytics/statistics")
    app.run(host='0.0.0.0', port=5001, debug=True)
