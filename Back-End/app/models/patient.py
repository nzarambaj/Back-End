from app.database import db

class Patient(db.Model):
    __tablename__ = "patients"
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(120))
    birth_date = db.Column(db.String(20))
    sex = db.Column(db.String(10))
    
    # Relationships
    worklists = db.relationship("Worklist", back_populates="patient")
    studies = db.relationship("Study", back_populates="patient")
    
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "name": self.name,
            "birth_date": self.birth_date,
            "sex": self.sex
        }