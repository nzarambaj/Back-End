from flask import Blueprint, jsonify

mwl_bp = Blueprint("mwl", __name__, url_prefix="/mwl")

@mwl_bp.route("/patients")
def get_patients():

    return jsonify({
        "message": "MWL Patients endpoint working"
    })
