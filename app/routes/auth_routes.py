from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    result, status_code = register_user(data)
    return jsonify(result), status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    result, status_code = login_user(data)
    return jsonify(result), status_code