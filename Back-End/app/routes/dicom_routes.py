from flask import Blueprint, request, jsonify
from app.services.dicom_service import save_dicom_file, get_studies, get_series_for_study, get_instances_for_series

dicom_bp = Blueprint("dicom", __name__, url_prefix="/dicom")

@dicom_bp.route("/upload", methods=["POST"])
def upload_dicom():
    file = request.files.get("file")
    patient_id = request.form.get("patient_id", type=int)
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    if not patient_id:
        return jsonify({"error": "Patient ID required"}), 400
    
    instance, error = save_dicom_file(file, patient_id)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({
        "message": "DICOM uploaded successfully",
        "instance": instance.to_dict()
    }), 201

@dicom_bp.route("/studies", methods=["GET"])
def list_studies():
    patient_id = request.args.get("patient_id", type=int)
    modality = request.args.get("modality")
    page = request.args.get("page", 1, type=int)
    
    studies = get_studies(patient_id=patient_id, modality=modality, page=page)
    
    return jsonify({
        "studies": [study.to_dict() for study in studies.items],
        "pagination": {
            "total": studies.total,
            "pages": studies.pages,
            "current_page": studies.page,
            "has_next": studies.has_next,
            "has_prev": studies.has_prev
        }
    })

@dicom_bp.route("/studies/<int:study_id>/series", methods=["GET"])
def get_series(study_id):
    series = get_series_for_study(study_id)
    return jsonify({
        "series": [s.to_dict() for s in series]
    })

@dicom_bp.route("/series/<int:series_id>/instances", methods=["GET"])
def get_instances(series_id):
    instances = get_instances_for_series(series_id)
    return jsonify({
        "instances": [i.to_dict() for i in instances]
    })