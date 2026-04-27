"""
Doctor Model - Professional Medical Staff
"""
from app.database import db
from datetime import datetime
import uuid

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    hospital_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    studies = db.relationship('MRIStudy', backref='doctor', lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "specialty": self.specialty,
            "licenseNumber": self.license_number,
            "phone": self.phone,
            "email": self.email,
            "hospital": {
                "id": self.hospital_id,
                "name": "Hôpital Saint-Pierre"  # Default hospital name
            } if self.hospital_id else None,
            "createdAt": self.created_at.isoformat() + 'Z' if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            specialty=data.get('specialty'),
            license_number=data.get('licenseNumber'),
            phone=data.get('phone'),
            email=data.get('email'),
            hospital_id=data.get('hospital', {}).get('id') if data.get('hospital') else None
        )
