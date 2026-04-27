from flask import Blueprint, request, jsonify
from app.models.patient import Patient
from app.models.worklist import Worklist, ModalityType, WorklistStatus
from app.database import db

mwl_bp = Blueprint("mwl", __name__, url_prefix="/mwl")

@mwl_bp.route("/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify({
        "patients": [p.to_dict() for p in patients]
    })

@mwl_bp.route("/patients/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        return jsonify({
            "patient": patient.to_dict()
        })
    return jsonify({"error": "Patient not found"}), 404

@mwl_bp.route("/patients", methods=["POST"])
def create_patient():
    data = request.json
    
    patient = Patient(
        patient_id=data.get("patient_id"),
        name=data.get("name"),
        birth_date=data.get("birth_date"),
        sex=data.get("sex")
    )
    
    db.session.add(patient)
    db.session.commit()
    
    return jsonify(patient.to_dict()), 201

@mwl_bp.route("/worklists", methods=["GET"])
def get_worklists():
    worklists = Worklist.query.all()
    return jsonify({
        "worklists": [w.to_dict() for w in worklists]
    })

@mwl_bp.route("/worklists/<int:worklist_id>", methods=["GET"])
def get_worklist(worklist_id):
    worklist = Worklist.query.get(worklist_id)
    if worklist:
        return jsonify({
            "worklist": worklist.to_dict()
        })
    return jsonify({"error": "Worklist not found"}), 404

@mwl_bp.route("/worklists", methods=["POST"])
def create_worklist():
    data = request.json
    
    worklist = Worklist(
        accession_number=data.get("accession_number"),
        patient_id=data.get("patient_id"),
        modality=ModalityType(data.get("modality")),
        description=data.get("description"),
        priority=data.get("priority", "routine"),
        referring_physician=data.get("referring_physician")
    )
    
    db.session.add(worklist)
    db.session.commit()
    
    return jsonify(worklist.to_dict()), 201