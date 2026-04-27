"""
Study Model - MRI/IRM Medical Studies
"""
from app.database import db
from datetime import datetime
import uuid

class MRIStudy(db.Model):
    __tablename__ = 'mri_studies'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey('patients_new.id'), nullable=False)
    doctor_id = db.Column(db.String, db.ForeignKey('doctors.id'), nullable=False)
    study_date = db.Column(db.DateTime, nullable=False)
    modality = db.Column(db.String(50), nullable=False)
    body_part = db.Column(db.String(100))
    status = db.Column(db.String(50), default='scheduled')
    clinical_indication = db.Column(db.Text)
    report_status = db.Column(db.String(50), default='pending')
    report_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('MRIImage', backref='study', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            "id": self.id,
            "patientId": self.patient_id,
            "doctorId": self.doctor_id,
            "studyDate": self.study_date.isoformat() + 'Z' if self.study_date else None,
            "modality": self.modality,
            "bodyPart": self.body_part,
            "status": self.status,
            "clinicalIndication": self.clinical_indication,
            "report": {
                "status": self.report_status,
                "summary": self.report_summary
            } if self.report_status or self.report_summary else None,
            "createdAt": self.created_at.isoformat() + 'Z' if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        report = data.get('report', {})
        return cls(
            patient_id=data.get('patientId'),
            doctor_id=data.get('doctorId'),
            study_date=datetime.strptime(data.get('studyDate'), '%Y-%m-%dT%H:%M:%SZ') if data.get('studyDate') else datetime.utcnow(),
            modality=data.get('modality'),
            body_part=data.get('bodyPart'),
            status=data.get('status', 'scheduled'),
            clinical_indication=data.get('clinicalIndication'),
            report_status=report.get('status') if report else 'pending',
            report_summary=report.get('summary') if report else None
        )
