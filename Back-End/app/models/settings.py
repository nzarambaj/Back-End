# app/models/settings.py
from datetime import datetime, timezone
from app.database import db


class ModalityConfig(db.Model):
    """Per-modality global configuration (admin-managed)."""
    __tablename__ = "modality_configs"

    id                     = db.Column(db.Integer, primary_key=True)
    modality               = db.Column(db.String(10), unique=True, nullable=False)  # US/XR/CT/MRI
    display_name           = db.Column(db.String(60), nullable=True)
    default_window_center  = db.Column(db.Float, nullable=True)
    default_window_width   = db.Column(db.Float, nullable=True)
    bits_allocated         = db.Column(db.Integer, default=16)
    color_map              = db.Column(db.String(30), default="gray")  # gray / hot / bone
    is_active              = db.Column(db.Boolean, default=True)
    notes                  = db.Column(db.Text, nullable=True)
    updated_at             = db.Column(db.DateTime,
                                       default=lambda: datetime.now(timezone.utc),
                                       onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id":                    self.id,
            "modality":              self.modality,
            "display_name":          self.display_name,
            "default_window_center": self.default_window_center,
            "default_window_width":  self.default_window_width,
            "bits_allocated":        self.bits_allocated,
            "color_map":             self.color_map,
            "is_active":             self.is_active,
            "notes":                 self.notes,
            "updated_at":            self.updated_at.isoformat() if self.updated_at else None,
        }


class WindowPreset(db.Model):
    """Named W/L presets per modality (e.g. CT Brain, CT Lung, CT Bone)."""
    __tablename__ = "window_presets"

    id             = db.Column(db.Integer, primary_key=True)
    modality       = db.Column(db.String(10), nullable=False)
    name           = db.Column(db.String(60), nullable=False)   # e.g. "Brain", "Lung", "Bone"
    window_center  = db.Column(db.Float, nullable=False)
    window_width   = db.Column(db.Float, nullable=False)
    description    = db.Column(db.String(255), nullable=True)
    created_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint("modality", "name", name="uq_modality_preset_name"),
    )

    def to_dict(self):
        return {
            "id":            self.id,
            "modality":      self.modality,
            "name":          self.name,
            "window_center": self.window_center,
            "window_width":  self.window_width,
            "description":   self.description,
            "created_at":    self.created_at.isoformat(),
        }