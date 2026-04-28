"""
Root route - JSON API only
"""
from flask import Blueprint, jsonify

root_bp = Blueprint("root", __name__)

@root_bp.route("/", methods=["GET"])
def root():
    """Main endpoint - Complete API overview"""
    return jsonify({
        "name": "Professional Medical Imaging System API",
        "status": "running",
        "type": "JSON API Backend",
        "version": "2.0.0",
        "description": "Complete medical imaging management system with professional staff, patients, studies, and image processing",
        "server": {
            "mode": "development",
            "database": "SQLite",
            "host": "127.0.0.1:8000"
        },
        "endpoints": {
            "health": "/health",
            "authentication": {
                "login": "/auth/login",
                "register": "/auth/register",
                "refresh": "/auth/refresh"
            },
            "medical_staff": {
                "radiologists": "/api/medical-staff/radiologists",
                "referring_doctors": "/api/medical-staff/referring-doctors", 
                "imaging_technicians": "/api/medical-staff/imaging-technicians",
                "search": "/api/medical-staff/search"
            },
            "patients": {
                "list": "/mwl/patients",
                "create": "/mwl/patients",
                "details": "/mwl/patients/{id}"
            },
            "worklists": {
                "list": "/mwl/worklists",
                "create": "/mwl/worklists",
                "details": "/mwl/worklists/{id}"
            },
            "studies": {
                "list": "/api/studies",
                "create": "/api/studies",
                "details": "/api/studies/{id}",
                "images": "/api/studies/{id}/images"
            },
            "images": {
                "details": "/api/images/{id}",
                "upload": "/api/studies/{id}/images"
            },
            "dicom": {
                "studies": "/dicom/studies",
                "series": "/dicom/series",
                "instances": "/dicom/instances",
                "upload": "/dicom/upload"
            },
            "settings": {
                "modalities": "/settings/modalities",
                "presets": "/settings/presets"
            },
            "professional_api": {
                "doctors": "/api/doctors",
                "patients_new": "/api/patients", 
                "studies": "/api/studies",
                "images": "/api/images"
            }
        },
        "features": [
            "Professional Medical Staff Management",
            "Patient Management", 
            "Worklist Management",
            "DICOM Processing",
            "Image Processing & Analysis",
            "Study Management",
            "Settings Configuration",
            "RESTful API Design",
            "JSON Responses",
            "Authentication & Authorization"
        ],
        "statistics": {
            "total_endpoints": 25,
            "authenticated_endpoints": 8,
            "public_endpoints": 17,
            "professional_features": 8
        },
        "documentation": {
            "postman_guide": "/POSTMAN_API_GUIDE.md",
            "medical_staff_guide": "/MEDICAL_STAFF_POSTMAN_GUIDE.md",
            "professional_api_guide": "/PROFESSIONAL_API_POSTMAN_GUIDE.md",
            "quick_reference": "/API_QUICK_REFERENCE.md"
        }
    })

@root_bp.route("/health", methods=["GET"])
def health():
    """Simple health check"""
    return jsonify({
        "status": "healthy",
        "service": "Medical Imaging System API"
    })
