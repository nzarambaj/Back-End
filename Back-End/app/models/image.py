"""
Image Model - MRI/IRM Medical Images
"""
from app.database import db
from datetime import datetime
import uuid

class MRIImage(db.Model):
    __tablename__ = 'mri_images'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    study_id = db.Column(db.String, db.ForeignKey('mri_studies.id'), nullable=False)
    series_number = db.Column(db.Integer)
    instance_number = db.Column(db.Integer)
    sequence_type = db.Column(db.String(50))
    file_url = db.Column(db.Text, nullable=False)
    thumbnail_url = db.Column(db.Text)
    format = db.Column(db.String(20))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    slice_thickness = db.Column(db.String(20))
    orientation = db.Column(db.String(20))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "studyId": self.study_id,
            "seriesNumber": self.series_number,
            "instanceNumber": self.instance_number,
            "sequenceType": self.sequence_type,
            "fileUrl": self.file_url,
            "thumbnailUrl": self.thumbnail_url,
            "format": self.format,
            "resolution": {
                "width": self.width,
                "height": self.height
            } if self.width and self.height else None,
            "metadata": {
                "sliceThickness": self.slice_thickness,
                "orientation": self.orientation
            } if self.slice_thickness or self.orientation else None,
            "uploadedAt": self.uploaded_at.isoformat() + 'Z' if self.uploaded_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        resolution = data.get('resolution', {})
        metadata = data.get('metadata', {})
        return cls(
            study_id=data.get('studyId'),
            series_number=data.get('seriesNumber'),
            instance_number=data.get('instanceNumber'),
            sequence_type=data.get('sequenceType'),
            file_url=data.get('fileUrl'),
            thumbnail_url=data.get('thumbnailUrl'),
            format=data.get('format'),
            width=resolution.get('width'),
            height=resolution.get('height'),
            slice_thickness=metadata.get('sliceThickness'),
            orientation=metadata.get('orientation')
        )
