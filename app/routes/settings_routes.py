from flask import Blueprint, request, jsonify
from app.services.settings_service import (
    get_all_modality_configs, get_modality_config, upsert_modality_config,
    get_presets, create_preset, update_preset, delete_preset
)

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@settings_bp.route("/modalities", methods=["GET"])
def list_modalities():
    configs = get_all_modality_configs()
    return jsonify({
        "modalities": [c.to_dict() for c in configs]
    })

@settings_bp.route("/modalities/<string:modality>", methods=["GET"])
def get_modality(modality):
    config = get_modality_config(modality)
    if not config:
        return jsonify({"error": "Modality not found"}), 404
    return jsonify(config.to_dict())

@settings_bp.route("/modalities/<string:modality>", methods=["PUT"])
def update_modality(modality):
    data = request.json
    config, error = upsert_modality_config(modality, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(config.to_dict())

@settings_bp.route("/presets", methods=["GET"])
def list_presets():
    modality = request.args.get("modality")
    presets = get_presets(modality)
    return jsonify({
        "presets": [p.to_dict() for p in presets]
    })

@settings_bp.route("/presets", methods=["POST"])
def create_preset():
    data = request.json
    preset, error = create_preset(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(preset.to_dict()), 201

@settings_bp.route("/presets/<int:preset_id>", methods=["PUT"])
def update_preset_route(preset_id):
    data = request.json
    preset, error = update_preset(preset_id, data)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(preset.to_dict())

@settings_bp.route("/presets/<int:preset_id>", methods=["DELETE"])
def delete_preset_route(preset_id):
    success, error = delete_preset(preset_id)
    if not success:
        return jsonify({"error": error}), 404
    return jsonify({"message": "Preset deleted"})