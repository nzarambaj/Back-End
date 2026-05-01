#!/usr/bin/env python3
"""
Enhanced Equipment API from Calculus Folder
Comprehensive medical equipment data with detailed specifications
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

# Comprehensive equipment data from Calculus folder
EQUIPMENT_DATA = {
    "equipment": [
        {
            "id": "ct_001",
            "name": "Siemens SOMATOM Definition Edge",
            "type": "CT",
            "category": "Computed Tomography",
            "manufacturer": "Siemens Healthineers",
            "model": "SOMATOM Definition Edge",
            "status": "active",
            "location": "Radiology Department - Room 101",
            "description": "128-slice dual-source CT scanner with advanced cardiac imaging capabilities",
            "specifications": {
                "detector_rows": 128,
                "slice_thickness": "0.6mm",
                "rotation_time": "0.28s",
                "spatial_resolution": "24 lp/cm",
                "temporal_resolution": "75ms",
                "tube_voltage": "80-140kV",
                "tube_current": "500-800mA"
            },
            "capabilities": [
                "High-resolution CT imaging",
                "Cardiac CT angiography",
                "Neuro CT perfusion",
                "Body CT angiography",
                "Lung nodule detection",
                "Bone mineral density",
                "Virtual colonoscopy"
            ],
            "clinical_applications": [
                "Cardiac imaging",
                "Neuro imaging", 
                "Oncologic imaging",
                "Trauma assessment",
                "Vascular imaging"
            ],
            "maintenance": {
                "last_maintenance": "2024-06-15",
                "next_maintenance": "2024-09-15",
                "maintenance_interval": "3 months",
                "service_hours": "15,000 hours"
            },
            "software": {
                "version": "VA44A",
                "reconstruction_engine": "Iterative Reconstruction",
                "ai_features": ["AI-Rad Companion", "Automated lesion detection"]
            },
            "connectivity": {
                "dicom": "3.0 compliant",
                "hl7": "2.5 compliant",
                "network": "Gigabit Ethernet",
                "storage": "PACS integrated"
            },
            "image_url": "/images/ct-scanner.jpg",
            "manual_url": "/manuals/somatom-edge.pdf",
            "training_required": "Yes - 40 hours certification",
            "cost_per_scan": "$150-300",
            "patient_throughput": "30-40 patients/day"
        },
        {
            "id": "mri_001",
            "name": "GE Signa Pioneer",
            "type": "MRI",
            "category": "Magnetic Resonance Imaging",
            "manufacturer": "GE Healthcare",
            "model": "Signa Pioneer 3.0T",
            "status": "active",
            "location": "Radiology Department - Room 102",
            "description": "3.0T MRI scanner with advanced imaging capabilities and AI-powered workflows",
            "specifications": {
                "field_strength": "3.0 Tesla",
                "gradient_system": "Superconducting",
                "gradient_amplitude": "50 mT/m",
                "slew_rate": "200 T/m/s",
                "bore_diameter": "70cm",
                "patient_weight_limit": "250kg",
                "rf_channels": "48 channel"
            },
            "capabilities": [
                "Neuro MRI with DTI",
                "Body MRI with diffusion",
                "Musculoskeletal MRI",
                "Cardiac MRI with stress",
                "Breast MRI with contrast",
                "Prostate MRI",
                "Functional MRI (fMRI)",
                "MR spectroscopy"
            ],
            "clinical_applications": [
                "Neurological disorders",
                "Oncologic imaging",
                "Musculoskeletal injuries",
                "Cardiac assessment",
                "Breast cancer screening",
                "Prostate cancer detection"
            ],
            "maintenance": {
                "last_maintenance": "2024-05-20",
                "next_maintenance": "2024-08-20",
                "maintenance_interval": "3 months",
                "cryogen_refill": "Every 6 months"
            },
            "software": {
                "version": "27.0",
                "sequences": ["FSE", "EPI", "GRE", "SSFP"],
                "ai_features": ["AIR Recon", "Deep Learning Reconstruction"]
            },
            "connectivity": {
                "dicom": "3.0 compliant",
                "hl7": "2.5 compliant",
                "network": "Gigabit Ethernet",
                "storage": "PACS integrated"
            },
            "image_url": "/images/mri-scanner.jpg",
            "manual_url": "/manuals/signa-pioneer.pdf",
            "training_required": "Yes - 60 hours certification",
            "cost_per_scan": "$500-1500",
            "patient_throughput": "15-20 patients/day"
        },
        {
            "id": "us_001",
            "name": "Philips Epiq 7",
            "type": "Ultrasound",
            "category": "Diagnostic Ultrasound",
            "manufacturer": "Philips Medical Systems",
            "model": "Epiq 7",
            "status": "active",
            "location": "Obstetrics Department - Room 201",
            "description": "Premium ultrasound system with 3D/4D imaging and advanced quantification",
            "specifications": {
                "transducer_types": ["Linear", "Curved", "Phased Array", "3D/4D"],
                "frequency_range": "1-18 MHz",
                "imaging_modes": ["B-mode", "M-mode", "Color Doppler", "Power Doppler", "PW Doppler"],
                "display": "21.5 inch high-resolution LCD",
                "ports": "4 transducer ports",
                "battery_backup": "Yes - 2 hours"
            },
            "capabilities": [
                "Obstetric ultrasound",
                "Vascular ultrasound",
                "Cardiac ultrasound",
                "Abdominal ultrasound",
                "3D/4D imaging",
                "Contrast-enhanced ultrasound",
                "Elastography",
                "Shear wave imaging"
            ],
            "clinical_applications": [
                "Pregnancy monitoring",
                "Vascular disease assessment",
                "Cardiac function evaluation",
                "Abdominal organ assessment",
                "Breast imaging",
                "Musculoskeletal imaging"
            ],
            "maintenance": {
                "last_maintenance": "2024-07-01",
                "next_maintenance": "2024-10-01",
                "maintenance_interval": "3 months",
                "transducer_replacement": "Every 2-3 years"
            },
            "software": {
                "version": "5.0",
                "features": ["AutoSCAN", "SonoCT", "XRES"],
                "ai_features": ["AI-based measurements", "Auto-ROI"]
            },
            "connectivity": {
                "dicom": "3.0 compliant",
                "network": "Wireless and Ethernet",
                "storage": "PACS and cloud"
            },
            "image_url": "/images/ultrasound.jpg",
            "manual_url": "/manuals/epiq-7.pdf",
            "training_required": "Yes - 30 hours certification",
            "cost_per_scan": "$50-200",
            "patient_throughput": "40-50 patients/day"
        },
        {
            "id": "xr_001",
            "name": "Canon CXDI-700C",
            "type": "X-Ray",
            "category": "Digital Radiography",
            "manufacturer": "Canon Medical Systems",
            "model": "CXDI-700C",
            "status": "active",
            "location": "Emergency Department - Room 301",
            "description": "Digital radiography system with wireless detector and advanced image processing",
            "specifications": {
                "detector_type": "CsI Flat Panel Detector",
                "detector_size": "17x17 inches",
                "pixel_size": "100 microns",
                "spatial_resolution": "5.0 lp/mm",
                "dynamic_range": "16-bit",
                "exposure_time": "1ms - 1s",
                "tube_voltage": "40-150kV"
            },
            "capabilities": [
                "Chest X-ray",
                "Bone X-ray",
                "Abdominal X-ray",
                "Extremity imaging",
                "Portable imaging",
                "Digital subtraction",
                "Image stitching",
                "Low-dose imaging"
            ],
            "clinical_applications": [
                "Chest pathology",
                "Fracture detection",
                "Abdominal assessment",
                "Emergency imaging",
                "ICU bedside imaging",
                "Operating room imaging"
            ],
            "maintenance": {
                "last_maintenance": "2024-06-10",
                "next_maintenance": "2024-09-10",
                "maintenance_interval": "3 months",
                "detector_calibration": "Monthly"
            },
            "software": {
                "version": "2.1",
                "features": ["Dynamic Range Optimizer", "Noise Reduction"],
                "ai_features": ["Auto-exposure", "Image quality assessment"]
            },
            "connectivity": {
                "dicom": "3.0 compliant",
                "network": "Wireless 802.11n",
                "storage": "PACS and cloud"
            },
            "image_url": "/images/xray.jpg",
            "manual_url": "/manuals/cxdi-700c.pdf",
            "training_required": "Yes - 20 hours certification",
            "cost_per_scan": "$30-100",
            "patient_throughput": "60-80 patients/day"
        },
        {
            "id": "mammo_001",
            "name": "Hologic Selenia Dimensions",
            "type": "Mammography",
            "category": "Digital Mammography",
            "manufacturer": "Hologic",
            "model": "Selenia Dimensions with 3D tomosynthesis",
            "status": "active",
            "location": "Women's Health Center - Room 401",
            "description": "Digital mammography system with breast tomosynthesis and biopsy guidance",
            "specifications": {
                "detector_type": "Direct Capture Selenium",
                "detector_size": "24x29 cm",
                "pixel_size": "70 microns",
                "spatial_resolution": "7.0 lp/mm",
                "compression_force": "0-200N",
                "tube_voltage": "25-35kV",
                "tomography_angles": "15 degrees"
            },
            "capabilities": [
                "Digital mammography",
                "Breast tomosynthesis",
                "Biopsy guidance",
                "Stereotactic biopsy",
                "Contrast-enhanced mammography",
                "CAD (Computer-Aided Detection)",
                "Density assessment",
                "Risk stratification"
            ],
            "clinical_applications": [
                "Breast cancer screening",
                "Diagnostic mammography",
                "High-risk patient monitoring",
                "Breast biopsy guidance",
                "Implant imaging",
                "Dense breast assessment"
            ],
            "maintenance": {
                "last_maintenance": "2024-05-15",
                "next_maintenance": "2024-08-15",
                "maintenance_interval": "3 months",
                "quality_assurance": "Daily"
            },
            "software": {
                "version": "3.2",
                "features": ["Intelligent 2D", "Quantra", "C-View"],
                "ai_features": ["AI-based detection", "Risk assessment"]
            },
            "connectivity": {
                "dicom": "3.0 compliant",
                "network": "Gigabit Ethernet",
                "storage": "PACS and cloud"
            },
            "image_url": "/images/mammography.jpg",
            "manual_url": "/manuals/selenia-dimensions.pdf",
            "training_required": "Yes - 40 hours certification",
            "cost_per_scan": "$100-300",
            "patient_throughput": "25-35 patients/day"
        }
    ],
    "metadata": {
        "total_equipment": 5,
        "active_equipment": 5,
        "categories": ["CT", "MRI", "Ultrasound", "X-Ray", "Mammography"],
        "manufacturers": ["Siemens", "GE", "Philips", "Canon", "Hologic"],
        "locations": ["Radiology", "Obstetrics", "Emergency", "Women's Health"],
        "last_updated": datetime.now().isoformat()
    }
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    metadata = EQUIPMENT_DATA['metadata']
    return jsonify({
        'status': 'healthy',
        'service': 'Enhanced Calculus Equipment API',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'equipment_count': metadata['total_equipment'],
        'categories': metadata['categories'],
        'manufacturers': metadata['manufacturers']
    })

@app.route('/api/equipment', methods=['GET'])
def get_all_equipment():
    """Get all medical equipment with comprehensive details"""
    return jsonify(EQUIPMENT_DATA)

@app.route('/api/equipment/<equipment_type>', methods=['GET'])
def get_equipment_by_type(equipment_type):
    """Get equipment by type with full details"""
    type_mapping = {
        'ct': 'CT',
        'mri': 'MRI', 
        'xray': 'X-Ray',
        'ultrasound': 'Ultrasound',
        'mammo': 'Mammography',
        'mammography': 'Mammography'
    }
    
    mapped_type = type_mapping.get(equipment_type.lower(), equipment_type.title())
    
    filtered_equipment = [
        eq for eq in EQUIPMENT_DATA['equipment'] 
        if eq['type'].lower() == mapped_type.lower()
    ]
    
    if not filtered_equipment:
        return jsonify({'error': f'Equipment type {equipment_type} not found'}), 404
    
    return jsonify({'equipment': filtered_equipment, 'count': len(filtered_equipment)})

@app.route('/api/equipment/<equipment_type>/<equipment_id>', methods=['GET'])
def get_equipment_details(equipment_type, equipment_id):
    """Get specific equipment details"""
    type_mapping = {
        'ct': 'CT',
        'mri': 'MRI',
        'xray': 'X-Ray', 
        'ultrasound': 'Ultrasound',
        'mammo': 'Mammography',
        'mammography': 'Mammography'
    }
    
    mapped_type = type_mapping.get(equipment_type.lower(), equipment_type.title())
    
    equipment = next(
        (eq for eq in EQUIPMENT_DATA['equipment'] 
         if eq['type'].lower() == mapped_type.lower() and eq['id'] == equipment_id),
        None
    )
    
    if not equipment:
        return jsonify({'error': f'Equipment {equipment_id} of type {equipment_type} not found'}), 404
    
    return jsonify(equipment)

@app.route('/api/equipment/specifications/<equipment_type>', methods=['GET'])
def get_equipment_specifications(equipment_type):
    """Get equipment specifications only"""
    type_mapping = {
        'ct': 'CT',
        'mri': 'MRI',
        'xray': 'X-Ray', 
        'ultrasound': 'Ultrasound',
        'mammo': 'Mammography',
        'mammography': 'Mammography'
    }
    
    mapped_type = type_mapping.get(equipment_type.lower(), equipment_type.title())
    
    equipment = next(
        (eq for eq in EQUIPMENT_DATA['equipment'] 
         if eq['type'].lower() == mapped_type.lower()),
        None
    )
    
    if not equipment:
        return jsonify({'error': f'Equipment type {equipment_type} not found'}), 404
    
    return jsonify({
        'id': equipment['id'],
        'name': equipment['name'],
        'type': equipment['type'],
        'specifications': equipment['specifications']
    })

@app.route('/api/equipment/capabilities/<equipment_type>', methods=['GET'])
def get_equipment_capabilities(equipment_type):
    """Get equipment capabilities"""
    type_mapping = {
        'ct': 'CT',
        'mri': 'MRI',
        'xray': 'X-Ray', 
        'ultrasound': 'Ultrasound',
        'mammo': 'Mammography',
        'mammography': 'Mammography'
    }
    
    mapped_type = type_mapping.get(equipment_type.lower(), equipment_type.title())
    
    equipment = next(
        (eq for eq in EQUIPMENT_DATA['equipment'] 
         if eq['type'].lower() == mapped_type.lower()),
        None
    )
    
    if not equipment:
        return jsonify({'error': f'Equipment type {equipment_type} not found'}), 404
    
    return jsonify({
        'id': equipment['id'],
        'name': equipment['name'],
        'type': equipment['type'],
        'capabilities': equipment['capabilities'],
        'clinical_applications': equipment['clinical_applications']
    })

@app.route('/api/equipment/maintenance/<equipment_type>', methods=['GET'])
def get_equipment_maintenance(equipment_type):
    """Get equipment maintenance information"""
    type_mapping = {
        'ct': 'CT',
        'mri': 'MRI',
        'xray': 'X-Ray', 
        'ultrasound': 'Ultrasound',
        'mammo': 'Mammography',
        'mammography': 'Mammography'
    }
    
    mapped_type = type_mapping.get(equipment_type.lower(), equipment_type.title())
    
    equipment = next(
        (eq for eq in EQUIPMENT_DATA['equipment'] 
         if eq['type'].lower() == mapped_type.lower()),
        None
    )
    
    if not equipment:
        return jsonify({'error': f'Equipment type {equipment_type} not found'}), 404
    
    return jsonify({
        'id': equipment['id'],
        'name': equipment['name'],
        'type': equipment['type'],
        'maintenance': equipment['maintenance']
    })

@app.route('/api/equipment/cost/<equipment_type>', methods=['GET'])
def get_equipment_cost(equipment_type):
    """Get equipment cost information"""
    type_mapping = {
        'ct': 'CT',
        'mri': 'MRI',
        'xray': 'X-Ray', 
        'ultrasound': 'Ultrasound',
        'mammo': 'Mammography',
        'mammography': 'Mammography'
    }
    
    mapped_type = type_mapping.get(equipment_type.lower(), equipment_type.title())
    
    equipment = next(
        (eq for eq in EQUIPMENT_DATA['equipment'] 
         if eq['type'].lower() == mapped_type.lower()),
        None
    )
    
    if not equipment:
        return jsonify({'error': f'Equipment type {equipment_type} not found'}), 404
    
    return jsonify({
        'id': equipment['id'],
        'name': equipment['name'],
        'type': equipment['type'],
        'cost_per_scan': equipment['cost_per_scan'],
        'patient_throughput': equipment['patient_throughput']
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all equipment categories"""
    metadata = EQUIPMENT_DATA['metadata']
    return jsonify({
        'categories': metadata['categories'],
        'total': len(metadata['categories'])
    })

@app.route('/api/manufacturers', methods=['GET'])
def get_manufacturers():
    """Get all equipment manufacturers"""
    metadata = EQUIPMENT_DATA['metadata']
    return jsonify({
        'manufacturers': metadata['manufacturers'],
        'total': len(metadata['manufacturers'])
    })

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get all equipment locations"""
    metadata = EQUIPMENT_DATA['metadata']
    return jsonify({
        'locations': metadata['locations'],
        'total': len(metadata['locations'])
    })

@app.route('/api/equipment/search', methods=['POST'])
def search_equipment():
    """Search equipment by various criteria"""
    try:
        search_data = request.get_json() if request.is_json else {}
        query = search_data.get('query', '').lower()
        category = search_data.get('category', '')
        manufacturer = search_data.get('manufacturer', '')
        
        filtered_equipment = EQUIPMENT_DATA['equipment']
        
        if query:
            filtered_equipment = [
                eq for eq in filtered_equipment
                if query in eq['name'].lower() or 
                   query in eq['description'].lower() or
                   query in ' '.join(eq['capabilities']).lower()
            ]
        
        if category:
            filtered_equipment = [
                eq for eq in filtered_equipment
                if eq['type'].lower() == category.lower()
            ]
        
        if manufacturer:
            filtered_equipment = [
                eq for eq in filtered_equipment
                if manufacturer.lower() in eq['manufacturer'].lower()
            ]
        
        return jsonify({
            'equipment': filtered_equipment,
            'count': len(filtered_equipment),
            'query': search_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Search error: {str(e)}'}), 500

if __name__ == '__main__':
    print("Enhanced Equipment API from Calculus Folder Starting...")
    print("Available endpoints:")
    print("- GET /api/health")
    print("- GET /api/equipment")
    print("- GET /api/equipment/<type>")
    print("- GET /api/equipment/<type>/<id>")
    print("- GET /api/equipment/specifications/<type>")
    print("- GET /api/equipment/capabilities/<type>")
    print("- GET /api/equipment/maintenance/<type>")
    print("- GET /api/equipment/cost/<type>")
    print("- GET /api/categories")
    print("- GET /api/manufacturers")
    print("- GET /api/locations")
    print("- POST /api/equipment/search")
    print("\nStarting on http://localhost:5001")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
