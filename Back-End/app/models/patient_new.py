"""
Patient Model - Professional Patient Management
"""
from app.database import db
from datetime import datetime
import uuid

class PatientNew(db.Model):
    __tablename__ = 'patients_new'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    medical_record_number = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    studies = db.relationship('MRIStudy', backref='patient', lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "dateOfBirth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "address": {
                "street": self.street,
                "city": self.city,
                "postalCode": self.postal_code,
                "country": self.country
            } if any([self.street, self.city, self.postal_code, self.country]) else None,
            "medicalRecordNumber": self.medical_record_number,
            "createdAt": self.created_at.isoformat() + 'Z' if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        address = data.get('address', {})
        return cls(
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            date_of_birth=datetime.strptime(data.get('dateOfBirth'), '%Y-%m-%d').date() if data.get('dateOfBirth') else None,
            gender=data.get('gender'),
            phone=data.get('phone'),
            email=data.get('email'),
            street=address.get('street'),
            city=address.get('city'),
            postal_code=address.get('postalCode'),
            country=address.get('country'),
            medical_record_number=data.get('medicalRecordNumber')
        )
