# app/models/worklist.py
import enum
from datetime import datetime, timezone
from app.database import db


class ModalityType(str, enum.Enum):
    US  = "US"    # Ultrasound
    XR  = "XR"    # X-Ray
    CT  = "CT"    # Computed Tomography
    MRI = "MRI"   # Magnetic Resonance Imaging


class WorklistStatus(str, enum.Enum):
    SCHEDULED  = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED  = "completed"
    CANCELLED  = "cancelled"


class Worklist(db.Model):
    __tablename__ = "worklists"

    id               = db.Column(db.Integer, primary_key=True)
    accession_number = db.Column(db.String(64), unique=True, nullable=False)
    patient_id       = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    assigned_to_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    modality         = db.Column(db.Enum(ModalityType), nullable=False)
    status           = db.Column(db.Enum(WorklistStatus), default=WorklistStatus.SCHEDULED)
    scheduled_at     = db.Column(db.DateTime, nullable=True)
    description      = db.Column(db.Text, nullable=True)
    priority         = db.Column(db.String(20), default="routine")  # routine / urgent / stat
    referring_physician = db.Column(db.String(120), nullable=True)
    notes            = db.Column(db.Text, nullable=True)
    created_at       = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at       = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                 onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    patient     = db.relationship("Patient",  back_populates="worklists")
    assigned_to = db.relationship("User",     foreign_keys=[assigned_to_id])
    studies     = db.relationship("Study",    back_populates="worklist", lazy="dynamic")

    def to_dict(self):
        return {
            "id":                   self.id,
            "accession_number":     self.accession_number,
            "patient":              self.patient.to_dict() if self.patient else None,
            "modality":             self.modality.value,
            "status":               self.status.value,
            "priority":             self.priority,
            "scheduled_at":         self.scheduled_at.isoformat() if self.scheduled_at else None,
            "description":          self.description,
            "referring_physician":  self.referring_physician,
            "notes":                self.notes,
            "assigned_to":          self.assigned_to.username if self.assigned_to else None,
            "created_at":           self.created_at.isoformat(),
        }