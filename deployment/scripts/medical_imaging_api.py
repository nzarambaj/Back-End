"""
Medical Imaging API Bridge
Connects Project_BackEnd with Calculus Medical Imaging System
"""

from flask import Flask, request, jsonify, send_file
import requests
import os
import sys
import json
from datetime import datetime
import tempfile

# Add medical imaging modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'medical_imaging'))

# Import medical imaging modules
try:
    from vessel_identifier import VesselIdentifier
    from bone_identifier import BoneIdentifier
    from nifti_processor import NIfTIProcessor
    MEDICAL_IMAGING_AVAILABLE = True
except ImportError as e:
    print(f"Medical imaging modules not available: {e}")
    MEDICAL_IMAGING_AVAILABLE = False

app = Flask(__name__)

# Configuration
CALCULUS_API_URL = "http://localhost:5001"
PROJECT_BACKEND_URL = "http://localhost:5002"  # Different port for Project_BackEnd

class MedicalImagingBridge:
    """Bridge between Project_BackEnd and Calculus Medical Imaging"""
    
    def __init__(self):
        self.vessel_id = VesselIdentifier() if MEDICAL_IMAGING_AVAILABLE else None
        self.bone_id = BoneIdentifier() if MEDICAL_IMAGING_AVAILABLE else None
        # NIfTIProcessor requires nifti_folder parameter
        nifti_folder = os.path.join(os.path.dirname(__file__), '..', 'Calculus', 'mni_colin27_1998_nifti')
        self.nifti_proc = NIfTIProcessor(nifti_folder) if MEDICAL_IMAGING_AVAILABLE and os.path.exists(nifti_folder) else None
    
    def check_calculus_health(self):
        """Check if Calculus API is running"""
        try:
            response = requests.get(f"{CALCULUS_API_URL}/api/health", timeout=5)
            return response.status_code == 200, response.json()
        except:
            return False, {"error": "Calculus API not accessible"}
    
    def proxy_to_calculus(self, endpoint, method='GET', data=None):
        """Proxy requests to Calculus API"""
        try:
            url = f"{CALCULUS_API_URL}{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, timeout=30)
            
            return response.status_code, response.json() if response.content else {}
        except Exception as e:
            return 500, {"error": f"Proxy failed: {str(e)}"}

# Initialize bridge
bridge = MedicalImagingBridge()

@app.route('/')
def home():
    """Project_BackEnd Medical Imaging API Home"""
    return jsonify({
        "api_name": "Project_BackEnd Medical Imaging Bridge",
        "version": "1.0",
        "status": "running",
        "calculus_api": CALCULUS_API_URL,
        "medical_imaging": MEDICAL_IMAGING_AVAILABLE,
        "endpoints": {
            "health": "/api/health",
            "vessels": "/api/vessels/*",
            "bones": "/api/bones/*",
            "nifti": "/api/nifti/*",
            "dicom": "/api/dicom/*"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health')
def health_check():
    """Comprehensive health check"""
    calculus_status, calculus_data = bridge.check_calculus_health()
    
    return jsonify({
        "project_backend": "running",
        "calculus_api": "connected" if calculus_status else "disconnected",
        "medical_imaging": "available" if MEDICAL_IMAGING_AVAILABLE else "not_available",
        "services": {
            "vessel_identification": bool(bridge.vessel_id),
            "bone_identification": bool(bridge.bone_id),
            "nifti_processing": bool(bridge.nifti_proc)
        },
        "calculus_health": calculus_data if calculus_status else {"error": "Not connected"},
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/vessels/identify', methods=['GET', 'POST'])
def identify_vessels():
    """Identify vessels using local processing or Calculus API"""
    if request.method == 'POST':
        data = request.get_json() or {}
    else:
        data = request.args.to_dict()
    
    image_path = data.get('image_path', '')
    method = data.get('method', 'threshold')
    
    # Try local processing first
    if MEDICAL_IMAGING_AVAILABLE and bridge.vessel_id:
        try:
            results = bridge.vessel_id.identify_vessels(image_path, method)
            return jsonify({
                "status": "success",
                "processing": "local",
                "results": results,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            # Fallback to Calculus API
            pass
    
    # Proxy to Calculus API
    status, response = bridge.proxy_to_calculus('/api/vessels/identify', 'POST', data)
    return jsonify(response), status

@app.route('/api/bones/identify', methods=['GET', 'POST'])
def identify_bones():
    """Identify bones using local processing or Calculus API"""
    if request.method == 'POST':
        data = request.get_json() or {}
    else:
        data = request.args.to_dict()
    
    image_path = data.get('image_path', '')
    method = data.get('method', 'threshold')
    
    # Try local processing first
    if MEDICAL_IMAGING_AVAILABLE and bridge.bone_id:
        try:
            results = bridge.bone_id.identify_bones(image_path, method)
            return jsonify({
                "status": "success",
                "processing": "local",
                "results": results,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            # Fallback to Calculus API
            pass
    
    # Proxy to Calculus API
    status, response = bridge.proxy_to_calculus('/api/bones/identify', 'POST', data)
    return jsonify(response), status

@app.route('/api/nifti/process', methods=['GET', 'POST'])
def process_nifti():
    """Process NIfTI files using local processing or Calculus API"""
    if request.method == 'POST':
        data = request.get_json() or {}
    else:
        data = request.args.to_dict()
    
    nifti_path = data.get('nifti_path', '')
    
    # Try local processing first
    if MEDICAL_IMAGING_AVAILABLE and bridge.nifti_proc:
        try:
            results = bridge.nifti_proc.process_nifti_file(nifti_path)
            return jsonify({
                "status": "success",
                "processing": "local",
                "results": results,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            # Fallback to Calculus API
            pass
    
    # Proxy to Calculus API
    status, response = bridge.proxy_to_calculus('/api/nifti/process', 'POST', data)
    return jsonify(response), status

@app.route('/api/dicom/viewer', methods=['GET', 'POST'])
def dicom_viewer():
    """DICOM viewer functionality"""
    if request.method == 'POST':
        data = request.get_json() or {}
    else:
        data = request.args.to_dict()
    
    dicom_path = data.get('dicom_path', '')
    
    # Proxy to Calculus API
    status, response = bridge.proxy_to_calculus('/api/dicom/viewer', 'POST', data)
    return jsonify(response), status

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads for medical imaging"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Save uploaded file
    upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    return jsonify({
        "status": "success",
        "filename": filename,
        "filepath": filepath,
        "size": os.path.getsize(filepath),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/status')
def system_status():
    """Complete system status"""
    calculus_status, calculus_data = bridge.check_calculus_health()
    
    return jsonify({
        "project_backend": {
            "status": "running",
            "medical_imaging": MEDICAL_IMAGING_AVAILABLE,
            "modules": {
                "vessel_identifier": bool(bridge.vessel_id),
                "bone_identifier": bool(bridge.bone_id),
                "nifti_processor": bool(bridge.nifti_proc)
            }
        },
        "calculus_api": {
            "status": "connected" if calculus_status else "disconnected",
            "url": CALCULUS_API_URL,
            "health": calculus_data if calculus_status else {"error": "Not connected"}
        },
        "integration": {
            "status": "fully_operational" if calculus_status and MEDICAL_IMAGING_AVAILABLE else "partial",
            "features": [
                "local_processing" if MEDICAL_IMAGING_AVAILABLE else None,
                "calculus_proxy" if calculus_status else None,
                "file_upload",
                "api_bridge"
            ],
            "timestamp": datetime.now().isoformat()
        }
    })

if __name__ == '__main__':
    print("Starting Project_BackEnd Medical Imaging Bridge...")
    print(f"Calculus API: {CALCULUS_API_URL}")
    print(f"Medical Imaging: {'Available' if MEDICAL_IMAGING_AVAILABLE else 'Not Available'}")
    print(f"Project_BackEnd will run on: {PROJECT_BACKEND_URL}")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
