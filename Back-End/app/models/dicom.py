# app/models/dicom.py
from datetime import datetime, timezone
from app.database import db


class Study(db.Model):
    __tablename__ = "studies"

    id           = db.Column(db.Integer, primary_key=True)
    study_uid    = db.Column(db.String(128), unique=True, nullable=False)   # DICOM StudyInstanceUID
    patient_id   = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    worklist_id  = db.Column(db.Integer, db.ForeignKey("worklists.id"), nullable=True)
    modality     = db.Column(db.String(10), nullable=True)                  # US/XR/CT/MRI
    study_date   = db.Column(db.Date, nullable=True)
    description  = db.Column(db.String(255), nullable=True)
    created_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    patient  = db.relationship("Patient",  back_populates="studies")
    worklist = db.relationship("Worklist", back_populates="studies")
    series   = db.relationship("Series",   back_populates="study", lazy="dynamic",
                                cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id":          self.id,
            "study_uid":   self.study_uid,
            "patient_id":  self.patient_id,
            "modality":    self.modality,
            "study_date":  self.study_date.isoformat() if self.study_date else None,
            "description": self.description,
            "series_count": self.series.count(),
            "created_at":  self.created_at.isoformat(),
        }


class Series(db.Model):
    __tablename__ = "series"

    id          = db.Column(db.Integer, primary_key=True)
    series_uid  = db.Column(db.String(128), unique=True, nullable=False)    # DICOM SeriesInstanceUID
    study_id    = db.Column(db.Integer, db.ForeignKey("studies.id"), nullable=False)
    modality    = db.Column(db.String(10), nullable=True)
    series_number = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    study     = db.relationship("Study",    back_populates="series")
    instances = db.relationship("Instance", back_populates="series", lazy="dynamic",
                                cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id":              self.id,
            "series_uid":      self.series_uid,
            "study_id":        self.study_id,
            "modality":        self.modality,
            "series_number":   self.series_number,
            "description":     self.description,
            "instance_count":  self.instances.count(),
            "created_at":      self.created_at.isoformat(),
        }


class Instance(db.Model):
    __tablename__ = "instances"

    id            = db.Column(db.Integer, primary_key=True)
    instance_uid  = db.Column(db.String(128), unique=True, nullable=False)  # DICOM SOPInstanceUID
    series_id     = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=False)
    instance_number = db.Column(db.Integer, nullable=True)
    file_path     = db.Column(db.String(512), nullable=False)               # local filesystem path
    file_size     = db.Column(db.Integer, nullable=True)                    # bytes
    rows          = db.Column(db.Integer, nullable=True)
    columns       = db.Column(db.Integer, nullable=True)
    bits_allocated = db.Column(db.Integer, nullable=True)
    window_center  = db.Column(db.Float, nullable=True)
    window_width   = db.Column(db.Float, nullable=True)
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    series = db.relationship("Series", back_populates="instances")

    def to_dict(self):
        return {
            "id":               self.id,
            "instance_uid":     self.instance_uid,
            "series_id":        self.series_id,
            "instance_number":  self.instance_number,
            "file_path":        self.file_path,
            "file_size":        self.file_size,
            "rows":             self.rows,
            "columns":          self.columns,
            "bits_allocated":   self.bits_allocated,
            "window_center":    self.window_center,
            "window_width":     self.window_width,
            "created_at":       self.created_at.isoformat(),
        }