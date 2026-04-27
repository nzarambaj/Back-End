"""
Medical Staff API Routes - Professional Medical Imaging Team
Radiologists, Referring Doctors, and Imaging Technicians
"""
from flask import Blueprint, request, jsonify
from app.models.medical_staff import MedicalStaff, Radiologist, ReferringDoctor, ImagingTechnician
from app.database import db
from datetime import datetime

medical_staff_bp = Blueprint("medical_staff", __name__, url_prefix="/api/medical-staff")

# ===== RADIOLOGISTS =====

@medical_staff_bp.route("/radiologists", methods=["GET"])
def list_radiologists():
    """List all radiologists"""
    radiologists = Radiologist.query.all()
    return jsonify({
        "radiologists": [radiologist.to_dict() for radiologist in radiologists]
    })

@medical_staff_bp.route("/radiologists", methods=["POST"])
def create_radiologist():
    """Create a new radiologist"""
    data = request.json
    
    # Check if license already exists
    if Radiologist.query.filter_by(license_number=data.get('licenseNumber')).first():
        return jsonify({"error": "License number already exists"}), 400
    
    # Check if email already exists
    if Radiologist.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Email already exists"}), 400
    
    radiologist = Radiologist.from_dict(data)
    db.session.add(radiologist)
    db.session.commit()
    
    return jsonify(radiologist.to_dict()), 201

@medical_staff_bp.route("/radiologists/<radiologist_id>", methods=["GET"])
def get_radiologist(radiologist_id):
    """Get radiologist by ID"""
    radiologist = Radiologist.query.get(radiologist_id)
    if not radiologist:
        return jsonify({"error": "Radiologist not found"}), 404
    
    return jsonify(radiologist.to_dict())

@medical_staff_bp.route("/radiologists/<radiologist_id>", methods=["PUT"])
def update_radiologist(radiologist_id):
    """Update radiologist"""
    radiologist = Radiologist.query.get(radiologist_id)
    if not radiologist:
        return jsonify({"error": "Radiologist not found"}), 404
    
    data = request.json
    
    # Update fields
    if 'firstName' in data:
        radiologist.first_name = data['firstName']
    if 'lastName' in data:
        radiologist.last_name = data['lastName']
    if 'email' in data:
        radiologist.email = data['email']
    if 'phone' in data:
        radiologist.phone = data['phone']
    if 'department' in data:
        radiologist.department = data['department']
    if 'specialty' in data:
        radiologist.specialty = data['specialty']
    if 'subspecialty' in data:
        radiologist.subspecialty = data['subspecialty']
    if 'boardCertification' in data:
        radiologist.board_certification = data['boardCertification']
    if 'fellowshipTraining' in data:
        radiologist.fellowship_training = data['fellowshipTraining']
    if 'yearsExperience' in data:
        radiologist.years_experience = data['yearsExperience']
    if 'academicTitle' in data:
        radiologist.academic_title = data['academicTitle']
    if 'hospital' in data:
        radiologist.hospital_id = data['hospital'].get('id')
    
    radiologist.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(radiologist.to_dict())

@medical_staff_bp.route("/radiologists/<radiologist_id>", methods=["DELETE"])
def delete_radiologist(radiologist_id):
    """Delete radiologist"""
    radiologist = Radiologist.query.get(radiologist_id)
    if not radiologist:
        return jsonify({"error": "Radiologist not found"}), 404
    
    db.session.delete(radiologist)
    db.session.commit()
    
    return jsonify({"message": "Radiologist deleted successfully"})

# ===== REFERRING DOCTORS =====

@medical_staff_bp.route("/referring-doctors", methods=["GET"])
def list_referring_doctors():
    """List all referring doctors"""
    doctors = ReferringDoctor.query.all()
    return jsonify({
        "referringDoctors": [doctor.to_dict() for doctor in doctors]
    })

@medical_staff_bp.route("/referring-doctors", methods=["POST"])
def create_referring_doctor():
    """Create a new referring doctor"""
    data = request.json
    
    # Check if medical license already exists
    if ReferringDoctor.query.filter_by(medical_license=data.get('medicalLicense')).first():
        return jsonify({"error": "Medical license already exists"}), 400
    
    # Check if email already exists
    if ReferringDoctor.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Email already exists"}), 400
    
    doctor = ReferringDoctor.from_dict(data)
    db.session.add(doctor)
    db.session.commit()
    
    return jsonify(doctor.to_dict()), 201

@medical_staff_bp.route("/referring-doctors/<doctor_id>", methods=["GET"])
def get_referring_doctor(doctor_id):
    """Get referring doctor by ID"""
    doctor = ReferringDoctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Referring doctor not found"}), 404
    
    return jsonify(doctor.to_dict())

@medical_staff_bp.route("/referring-doctors/<doctor_id>", methods=["PUT"])
def update_referring_doctor(doctor_id):
    """Update referring doctor"""
    doctor = ReferringDoctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Referring doctor not found"}), 404
    
    data = request.json
    
    # Update fields
    if 'firstName' in data:
        doctor.first_name = data['firstName']
    if 'lastName' in data:
        doctor.last_name = data['lastName']
    if 'email' in data:
        doctor.email = data['email']
    if 'phone' in data:
        doctor.phone = data['phone']
    if 'department' in data:
        doctor.department = data['department']
    if 'specialty' in data:
        doctor.specialty = data['specialty']
    if 'practiceName' in data:
        doctor.practice_name = data['practiceName']
    if 'npiNumber' in data:
        doctor.npi_number = data['npiNumber']
    if 'deaNumber' in data:
        doctor.dea_number = data['deaNumber']
    if 'hospital' in data:
        doctor.hospital_id = data['hospital'].get('id')
    
    doctor.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(doctor.to_dict())

@medical_staff_bp.route("/referring-doctors/<doctor_id>", methods=["DELETE"])
def delete_referring_doctor(doctor_id):
    """Delete referring doctor"""
    doctor = ReferringDoctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Referring doctor not found"}), 404
    
    db.session.delete(doctor)
    db.session.commit()
    
    return jsonify({"message": "Referring doctor deleted successfully"})

# ===== IMAGING TECHNICIANS =====

@medical_staff_bp.route("/imaging-technicians", methods=["GET"])
def list_imaging_technicians():
    """List all imaging technicians"""
    technicians = ImagingTechnician.query.all()
    return jsonify({
        "imagingTechnicians": [technician.to_dict() for technician in technicians]
    })

@medical_staff_bp.route("/imaging-technicians", methods=["POST"])
def create_imaging_technician():
    """Create a new imaging technician"""
    data = request.json
    
    # Check if certification already exists
    if ImagingTechnician.query.filter_by(certification_number=data.get('certificationNumber')).first():
        return jsonify({"error": "Certification number already exists"}), 400
    
    # Check if email already exists
    if ImagingTechnician.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Email already exists"}), 400
    
    technician = ImagingTechnician.from_dict(data)
    db.session.add(technician)
    db.session.commit()
    
    return jsonify(technician.to_dict()), 201

@medical_staff_bp.route("/imaging-technicians/<technician_id>", methods=["GET"])
def get_imaging_technician(technician_id):
    """Get imaging technician by ID"""
    technician = ImagingTechnician.query.get(technician_id)
    if not technician:
        return jsonify({"error": "Imaging technician not found"}), 404
    
    return jsonify(technician.to_dict())

@medical_staff_bp.route("/imaging-technicians/<technician_id>", methods=["PUT"])
def update_imaging_technician(technician_id):
    """Update imaging technician"""
    technician = ImagingTechnician.query.get(technician_id)
    if not technician:
        return jsonify({"error": "Imaging technician not found"}), 404
    
    data = request.json
    
    # Update fields
    if 'firstName' in data:
        technician.first_name = data['firstName']
    if 'lastName' in data:
        technician.last_name = data['lastName']
    if 'email' in data:
        technician.email = data['email']
    if 'phone' in data:
        technician.phone = data['phone']
    if 'department' in data:
        technician.department = data['department']
    if 'certificationType' in data:
        technician.certification_type = data['certificationType']
    if 'modalities' in data:
        technician.modalities = ', '.join(data['modalities'])
    if 'certificationExpiry' in data:
        technician.certification_expiry = datetime.strptime(data['certificationExpiry'], '%Y-%m-%d').date()
    if 'advancedCertifications' in data:
        technician.advanced_certifications = ', '.join(data['advancedCertifications'])
    if 'shiftSchedule' in data:
        technician.shift_schedule = data['shiftSchedule']
    if 'supervisorId' in data:
        technician.supervisor_id = data['supervisorId']
    if 'hospital' in data:
        technician.hospital_id = data['hospital'].get('id')
    
    technician.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(technician.to_dict())

@medical_staff_bp.route("/imaging-technicians/<technician_id>", methods=["DELETE"])
def delete_imaging_technician(technician_id):
    """Delete imaging technician"""
    technician = ImagingTechnician.query.get(technician_id)
    if not technician:
        return jsonify({"error": "Imaging technician not found"}), 404
    
    db.session.delete(technician)
    db.session.commit()
    
    return jsonify({"message": "Imaging technician deleted successfully"})

# ===== COMBINED MEDICAL STAFF ENDPOINTS =====

@medical_staff_bp.route("/all", methods=["GET"])
def list_all_medical_staff():
    """List all medical staff with their types"""
    all_staff = MedicalStaff.query.all()
    
    staff_by_type = {
        "radiologists": [],
        "referringDoctors": [],
        "imagingTechnicians": []
    }
    
    for staff in all_staff:
        if staff.staff_type == 'radiologist':
            staff_by_type["radiologists"].append(staff.to_dict())
        elif staff.staff_type == 'doctor':
            staff_by_type["referringDoctors"].append(staff.to_dict())
        elif staff.staff_type == 'technician':
            staff_by_type["imagingTechnicians"].append(staff.to_dict())
    
    return jsonify(staff_by_type)

@medical_staff_bp.route("/search", methods=["GET"])
def search_medical_staff():
    """Search medical staff by name, specialty, or department"""
    query = request.args.get('q', '')
    staff_type = request.args.get('type', '')
    
    if not query:
        return jsonify({"error": "Search query is required"}), 400
    
    # Base query
    base_query = MedicalStaff.query
    
    # Filter by staff type if specified
    if staff_type:
        base_query = base_query.filter_by(staff_type=staff_type)
    
    # Search by name or email
    staff = base_query.filter(
        (MedicalStaff.first_name.ilike(f'%{query}%')) |
        (MedicalStaff.last_name.ilike(f'%{query}%')) |
        (MedicalStaff.email.ilike(f'%{query}%'))
    ).all()
    
    return jsonify({
        "results": [person.to_dict() for person in staff],
        "count": len(staff)
    })
