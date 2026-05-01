#!/usr/bin/env python3
"""
Simple Flask API for Medical Imaging System
Provides equipment data for backend integration
"""

from flask import Flask, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# Sample equipment data
EQUIPMENT_DATA = [
    {
        "id": 1,
        "name": "CT Scanner",
        "type": "Imaging",
        "status": "Active",
        "location": "Radiology Department",
        "manufacturer": "Siemens",
        "model": "SOMATOM Definition Edge"
    },
    {
        "id": 2,
        "name": "MRI Machine",
        "type": "Imaging",
        "status": "Active",
        "location": "Radiology Department",
        "manufacturer": "GE Healthcare",
        "model": "Signa Pioneer"
    },
    {
        "id": 3,
        "name": "X-Ray Machine",
        "type": "Imaging",
        "status": "Active",
        "location": "Emergency Department",
        "manufacturer": "Philips",
        "model": "DigitalDiagnost"
    },
    {
        "id": 4,
        "name": "Ultrasound Machine",
        "type": "Imaging",
        "status": "Active",
        "location": "Cardiology Department",
        "manufacturer": "Canon",
        "model": "Aplio i900"
    },
    {
        "id": 5,
        "name": "PET Scanner",
        "type": "Imaging",
        "status": "Maintenance",
        "location": "Nuclear Medicine",
        "manufacturer": "Siemens",
        "model": "Biograph Horizon"
    }
]

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Flask API for Medical Imaging",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "port": 5001
    })

@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    """Get all equipment"""
    return jsonify({
        "equipment": EQUIPMENT_DATA,
        "total": len(EQUIPMENT_DATA),
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """Get equipment by ID"""
    equipment = next((eq for eq in EQUIPMENT_DATA if eq["id"] == equipment_id), None)
    if equipment:
        return jsonify({
            "equipment": equipment,
            "source": "Flask API"
        })
    else:
        return jsonify({"error": "Equipment not found"}), 404

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "message": "Flask API for Medical Imaging System",
        "endpoints": {
            "health": "/api/health",
            "equipment": "/api/equipment",
            "equipment_by_id": "/api/equipment/<id>"
        },
        "port": 5001
    })

if __name__ == '__main__':
    print("Starting Flask API for Medical Imaging System...")
    print("Port: 5001")
    print("Health: http://localhost:5001/api/health")
    print("Equipment: http://localhost:5001/api/equipment")
    app.run(host='0.0.0.0', port=5001, debug=True)
