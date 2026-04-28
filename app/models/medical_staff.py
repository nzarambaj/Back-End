"""
Medical Staff Models - Professional Medical Imaging Team
Includes Radiologists, Doctors, and Imaging Technicians
"""
from app.database import db
from datetime import datetime
import uuid

class MedicalStaff(db.Model):
    """Base model for all medical staff"""
    __tablename__ = 'medical_staff'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    hospital_id = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Discriminator column for staff type
    staff_type = db.Column(db.String(50), nullable=False)  # 'radiologist', 'doctor', 'technician'
    
    __mapper_args__ = {
        'polymorphic_on': staff_type,
        'polymorphic_identity': 'medical_staff'
    }
    
    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "hospital": {
                "id": self.hospital_id,
                "name": "Hôpital Saint-Pierre"
            } if self.hospital_id else None,
            "isActive": self.is_active,
            "staffType": self.staff_type,
            "createdAt": self.created_at.isoformat() + 'Z' if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }

class Radiologist(MedicalStaff):
    """Radiologist - Medical imaging specialist"""
    __tablename__ = 'radiologists'
    
    id = db.Column(db.String, db.ForeignKey('medical_staff.id'), primary_key=True)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)  # e.g., Neuroradiology, Pediatric Radiology
    subspecialty = db.Column(db.String(100))  # e.g., Breast Imaging, Cardiac Imaging
    board_certification = db.Column(db.String(50))
    fellowship_training = db.Column(db.String(200))
    years_experience = db.Column(db.Integer)
    academic_title = db.Column(db.String(50))  # e.g., Professor, Assistant Professor
    
    __mapper_args__ = {
        'polymorphic_identity': 'radiologist',
        'inherit_condition': id == MedicalStaff.id
    }
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "licenseNumber": self.license_number,
            "specialty": self.specialty,
            "subspecialty": self.subspecialty,
            "boardCertification": self.board_certification,
            "fellowshipTraining": self.fellowship_training,
            "yearsExperience": self.years_experience,
            "academicTitle": self.academic_title
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            email=data.get('email'),
            phone=data.get('phone'),
            department=data.get('department', 'Radiology'),
            hospital_id=data.get('hospital', {}).get('id') if data.get('hospital') else None,
            license_number=data.get('licenseNumber'),
            specialty=data.get('specialty'),
            subspecialty=data.get('subspecialty'),
            board_certification=data.get('boardCertification'),
            fellowship_training=data.get('fellowshipTraining'),
            years_experience=data.get('yearsExperience'),
            academic_title=data.get('academicTitle')
        )

class ReferringDoctor(MedicalStaff):
    """Referring Doctor - Orders imaging studies"""
    __tablename__ = 'referring_doctors'
    
    id = db.Column(db.String, db.ForeignKey('medical_staff.id'), primary_key=True)
    medical_license = db.Column(db.String(50), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)  # e.g., Cardiology, Neurology, Orthopedics
    practice_name = db.Column(db.String(200))
    npi_number = db.Column(db.String(20))  # National Provider Identifier
    dea_number = db.Column(db.String(20))   # Drug Enforcement Administration number
    
    __mapper_args__ = {
        'polymorphic_identity': 'doctor',
        'inherit_condition': id == MedicalStaff.id
    }
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "medicalLicense": self.medical_license,
            "specialty": self.specialty,
            "practiceName": self.practice_name,
            "npiNumber": self.npi_number,
            "deaNumber": self.dea_number
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            email=data.get('email'),
            phone=data.get('phone'),
            department=data.get('department', 'Clinical'),
            hospital_id=data.get('hospital', {}).get('id') if data.get('hospital') else None,
            medical_license=data.get('medicalLicense'),
            specialty=data.get('specialty'),
            practice_name=data.get('practiceName'),
            npi_number=data.get('npiNumber'),
            dea_number=data.get('deaNumber')
        )

class ImagingTechnician(MedicalStaff):
    """Imaging Technician - Operates imaging equipment"""
    __tablename__ = 'imaging_technicians'
    
    id = db.Column(db.String, db.ForeignKey('medical_staff.id'), primary_key=True)
    certification_number = db.Column(db.String(50), unique=True, nullable=False)
    certification_type = db.Column(db.String(100), nullable=False)  # e.g., ARRT, CAMRT
    modalities = db.Column(db.String(200))  # e.g., "MRI, CT, X-Ray"
    certification_expiry = db.Column(db.Date)
    advanced_certifications = db.Column(db.String(200))  # e.g., "MRI Safety, CT Angiography"
    shift_schedule = db.Column(db.String(100))  # e.g., "Day, Night, Rotating"
    supervisor_id = db.Column(db.String, db.ForeignKey('radiologists.id'))
    
    __mapper_args__ = {
        'polymorphic_identity': 'technician',
        'inherit_condition': id == MedicalStaff.id
    }
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "certificationNumber": self.certification_number,
            "certificationType": self.certification_type,
            "modalities": self.modalities.split(', ') if self.modalities else [],
            "certificationExpiry": self.certification_expiry.isoformat() if self.certification_expiry else None,
            "advancedCertifications": self.advanced_certifications.split(', ') if self.advanced_certifications else [],
            "shiftSchedule": self.shift_schedule,
            "supervisorId": self.supervisor_id
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            email=data.get('email'),
            phone=data.get('phone'),
            department=data.get('department', 'Imaging'),
            hospital_id=data.get('hospital', {}).get('id') if data.get('hospital') else None,
            certification_number=data.get('certificationNumber'),
            certification_type=data.get('certificationType'),
            modalities=', '.join(data.get('modalities', [])),
            certification_expiry=datetime.strptime(data.get('certificationExpiry'), '%Y-%m-%d').date() if data.get('certificationExpiry') else None,
            advanced_certifications=', '.join(data.get('advancedCertifications', [])),
            shift_schedule=data.get('shiftSchedule'),
            supervisor_id=data.get('supervisorId')
        )
