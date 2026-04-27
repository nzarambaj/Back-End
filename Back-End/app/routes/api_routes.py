"""
Pure JSON API Routes - No authentication required
"""
from flask import Blueprint, jsonify
from app.models.user import User
from app.models.patient import Patient
from app.models.worklist import Worklist
from app.models.dicom import Study, Series, Instance
from app.models.settings import ModalityConfig, WindowPreset

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/health", methods=["GET"])
def health_check():
    """API health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Medical Imaging System API",
        "version": "1.0.0"
    })

@api_bp.route("/stats", methods=["GET"])
def get_statistics():
    """Get system statistics as JSON"""
    try:
        stats = {
            "users": User.query.count(),
            "patients": Patient.query.count(),
            "worklists": Worklist.query.count(),
            "studies": Study.query.count(),
            "series": Series.query.count(),
            "instances": Instance.query.count(),
            "modalities": ModalityConfig.query.count(),
            "window_presets": WindowPreset.query.count()
        }
        
        # Get recent activity
        recent_patients = Patient.query.order_by(Patient.id.desc()).limit(3).all()
        recent_worklists = Worklist.query.order_by(Worklist.created_at.desc()).limit(3).all()
        
        return jsonify({
            "statistics": stats,
            "recent_patients": [p.to_dict() for p in recent_patients],
            "recent_worklists": [w.to_dict() for w in recent_worklists]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/dashboard", methods=["GET"])
def get_dashboard_data():
    """Get complete dashboard data as JSON"""
    try:
        # Get all data for dashboard
        users = User.query.all()
        patients = Patient.query.all()
        worklists = Worklist.query.all()
        studies = Study.query.all()
        modalities = ModalityConfig.query.all()
        
        return jsonify({
            "users": [u.to_dict() for u in users],
            "patients": [p.to_dict() for p in patients],
            "worklists": [w.to_dict() for w in worklists],
            "studies": [s.to_dict() for s in studies],
            "modalities": [m.to_dict() for m in modalities]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/info", methods=["GET"])
def api_info():
    """API information and available endpoints"""
    return jsonify({
        "name": "Medical Imaging System API",
        "version": "1.0.0",
        "description": "Pure JSON API for medical imaging system - No authentication required",
        "endpoints": {
            "authentication": {
                "POST /auth/login": "User authentication (optional)",
                "POST /auth/register": "User registration (optional)"
            },
            "patients": {
                "GET /mwl/patients": "Get all patients (no auth)",
                "POST /mwl/patients": "Create patient (no auth)"
            },
            "worklists": {
                "GET /mwl/worklists": "Get all worklists (no auth)",
                "POST /mwl/worklists": "Create worklist (no auth)"
            },
            "dicom": {
                "GET /dicom/studies": "Get DICOM studies (no auth)",
                "POST /dicom/upload": "Upload DICOM file (no auth)"
            },
            "settings": {
                "GET /settings/modalities": "Get modality configurations (no auth)",
                "GET /settings/window_presets": "Get window presets (no auth)"
            },
            "api": {
                "GET /api/health": "Health check (no auth)",
                "GET /api/stats": "System statistics (no auth)",
                "GET /api/dashboard": "Dashboard data (no auth)",
                "GET /api/info": "API information (no auth)"
            }
        }
    })
