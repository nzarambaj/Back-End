"""
Professional Medical Imaging API v2
Strong JSON API with proper REST endpoints
"""
from flask import Blueprint, request, jsonify
from app.models.doctor import Doctor
from app.models.patient_new import PatientNew
from app.models.study import MRIStudy
from app.models.image import MRIImage
from app.database import db
from datetime import datetime

api_v2_bp = Blueprint("api_v2", __name__, url_prefix="/api")

# ===== DOCTORS ENDPOINTS =====

@api_v2_bp.route("/doctors", methods=["GET"])
def list_doctors():
    """List all doctors"""
    doctors = Doctor.query.all()
    return jsonify({
        "doctors": [doctor.to_dict() for doctor in doctors]
    })

@api_v2_bp.route("/doctors", methods=["POST"])
def create_doctor():
    """Create a new doctor"""
    data = request.json
    
    # Check if license number already exists
    if Doctor.query.filter_by(license_number=data.get('licenseNumber')).first():
        return jsonify({"error": "License number already exists"}), 400
    
    doctor = Doctor.from_dict(data)
    db.session.add(doctor)
    db.session.commit()
    
    return jsonify(doctor.to_dict()), 201

@api_v2_bp.route("/doctors/<doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    """Get doctor by ID"""
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    
    return jsonify(doctor.to_dict())

@api_v2_bp.route("/doctors/<doctor_id>", methods=["PUT"])
def update_doctor(doctor_id):
    """Update doctor"""
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    
    data = request.json
    
    # Update fields
    if 'firstName' in data:
        doctor.first_name = data['firstName']
    if 'lastName' in data:
        doctor.last_name = data['lastName']
    if 'specialty' in data:
        doctor.specialty = data['specialty']
    if 'licenseNumber' in data:
        doctor.license_number = data['licenseNumber']
    if 'phone' in data:
        doctor.phone = data['phone']
    if 'email' in data:
        doctor.email = data['email']
    if 'hospital' in data and data['hospital']:
        doctor.hospital_id = data['hospital'].get('id')
    
    doctor.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(doctor.to_dict())

@api_v2_bp.route("/doctors/<doctor_id>", methods=["DELETE"])
def delete_doctor(doctor_id):
    """Delete doctor"""
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    
    db.session.delete(doctor)
    db.session.commit()
    
    return jsonify({"message": "Doctor deleted successfully"})

# ===== PATIENTS ENDPOINTS =====

@api_v2_bp.route("/patients", methods=["GET"])
def list_patients():
    """List all patients"""
    patients = PatientNew.query.all()
    return jsonify({
        "patients": [patient.to_dict() for patient in patients]
    })

@api_v2_bp.route("/patients", methods=["POST"])
def create_patient():
    """Create a new patient"""
    data = request.json
    
    # Check if medical record number already exists
    if PatientNew.query.filter_by(medical_record_number=data.get('medicalRecordNumber')).first():
        return jsonify({"error": "Medical record number already exists"}), 400
    
    patient = PatientNew.from_dict(data)
    db.session.add(patient)
    db.session.commit()
    
    return jsonify(patient.to_dict()), 201

@api_v2_bp.route("/patients/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    """Get patient by ID"""
    patient = PatientNew.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    return jsonify(patient.to_dict())

@api_v2_bp.route("/patients/<patient_id>", methods=["PUT"])
def update_patient(patient_id):
    """Update patient"""
    patient = PatientNew.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    data = request.json
    
    # Update fields
    if 'firstName' in data:
        patient.first_name = data['firstName']
    if 'lastName' in data:
        patient.last_name = data['lastName']
    if 'dateOfBirth' in data:
        patient.date_of_birth = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
    if 'gender' in data:
        patient.gender = data['gender']
    if 'phone' in data:
        patient.phone = data['phone']
    if 'email' in data:
        patient.email = data['email']
    if 'address' in data:
        address = data['address']
        if 'street' in address:
            patient.street = address['street']
        if 'city' in address:
            patient.city = address['city']
        if 'postalCode' in address:
            patient.postal_code = address['postalCode']
        if 'country' in address:
            patient.country = address['country']
    if 'medicalRecordNumber' in data:
        patient.medical_record_number = data['medicalRecordNumber']
    
    patient.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(patient.to_dict())

@api_v2_bp.route("/patients/<patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    """Delete patient"""
    patient = PatientNew.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    db.session.delete(patient)
    db.session.commit()
    
    return jsonify({"message": "Patient deleted successfully"})

# ===== STUDIES ENDPOINTS =====

@api_v2_bp.route("/studies", methods=["GET"])
def list_studies():
    """List all MRI studies"""
    studies = MRIStudy.query.all()
    return jsonify({
        "studies": [study.to_dict() for study in studies]
    })

@api_v2_bp.route("/studies", methods=["POST"])
def create_study():
    """Create a new MRI study"""
    data = request.json
    
    # Validate patient and doctor exist
    if not PatientNew.query.get(data.get('patientId')):
        return jsonify({"error": "Patient not found"}), 400
    if not Doctor.query.get(data.get('doctorId')):
        return jsonify({"error": "Doctor not found"}), 400
    
    study = MRIStudy.from_dict(data)
    db.session.add(study)
    db.session.commit()
    
    return jsonify(study.to_dict()), 201

@api_v2_bp.route("/studies/<study_id>", methods=["GET"])
def get_study(study_id):
    """Get study by ID"""
    study = MRIStudy.query.get(study_id)
    if not study:
        return jsonify({"error": "MRIStudy not found"}), 404
    
    return jsonify(study.to_dict())

@api_v2_bp.route("/studies/<study_id>", methods=["PUT"])
def update_study(study_id):
    """Update study"""
    study = MRIStudy.query.get(study_id)
    if not study:
        return jsonify({"error": "MRIStudy not found"}), 404
    
    data = request.json
    
    # Update fields
    if 'studyDate' in data:
        study.study_date = datetime.strptime(data['studyDate'], '%Y-%m-%dT%H:%M:%SZ')
    if 'modality' in data:
        study.modality = data['modality']
    if 'bodyPart' in data:
        study.body_part = data['bodyPart']
    if 'status' in data:
        study.status = data['status']
    if 'clinicalIndication' in data:
        study.clinical_indication = data['clinicalIndication']
    if 'report' in data:
        report = data['report']
        if 'status' in report:
            study.report_status = report['status']
        if 'summary' in report:
            study.report_summary = report['summary']
    
    study.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(study.to_dict())

@api_v2_bp.route("/studies/<study_id>", methods=["DELETE"])
def delete_study(study_id):
    """Delete study"""
    study = MRIStudy.query.get(study_id)
    if not study:
        return jsonify({"error": "MRIStudy not found"}), 404
    
    db.session.delete(study)
    db.session.commit()
    
    return jsonify({"message": "MRIStudy deleted successfully"})

# ===== IMAGES ENDPOINTS =====

@api_v2_bp.route("/studies/<study_id>/images", methods=["GET"])
def list_study_images(study_id):
    """List images for a study"""
    study = MRIStudy.query.get(study_id)
    if not study:
        return jsonify({"error": "MRIStudy not found"}), 404
    
    images = MRIImage.query.filter_by(study_id=study_id).all()
    return jsonify({
        "images": [image.to_dict() for image in images]
    })

@api_v2_bp.route("/studies/<study_id>/images", methods=["POST"])
def upload_image(study_id):
    """Upload image to study"""
    study = MRIStudy.query.get(study_id)
    if not study:
        return jsonify({"error": "MRIStudy not found"}), 404
    
    data = request.json
    data['studyId'] = study_id
    
    image = MRIImage.from_dict(data)
    db.session.add(image)
    db.session.commit()
    
    return jsonify(image.to_dict()), 201

@api_v2_bp.route("/images/<image_id>", methods=["GET"])
def get_image(image_id):
    """Get image by ID"""
    image = MRIImage.query.get(image_id)
    if not image:
        return jsonify({"error": "MRIImage not found"}), 404
    
    return jsonify(image.to_dict())

@api_v2_bp.route("/images/<image_id>", methods=["DELETE"])
def delete_image(image_id):
    """Delete image"""
    image = MRIImage.query.get(image_id)
    if not image:
        return jsonify({"error": "MRIImage not found"}), 404
    
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({"message": "MRIImage deleted successfully"})
