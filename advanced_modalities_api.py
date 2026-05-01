#!/usr/bin/env python3
"""
Advanced Medical Imaging Modalities API
Deep dive into medical imaging modalities with comprehensive endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Comprehensive modality data
MODALITIES_DATA = [
    {
        "id": 1,
        "modality_name": "Computed Tomography",
        "modality_code": "CT",
        "description": "Cross-sectional imaging using X-rays and computer processing",
        "category": "Cross-sectional",
        "radiation_type": "Ionizing",
        "contrast_agents": ["Iodinated", "Barium"],
        "clinical_applications": [
            "Trauma assessment",
            "Oncologic staging",
            "Vascular imaging",
            "Cardiac coronary CT",
            "Pulmonary embolism",
            "Abdominal/pelvic imaging"
        ],
        "advantages": [
            "Fast acquisition",
            "High spatial resolution",
            "3D reconstruction capability",
            "Wide availability"
        ],
        "limitations": [
            "Ionizing radiation exposure",
            "Limited soft tissue contrast",
            "Contrast nephrotoxicity risk"
        ],
        "typical_dose_range": "2-15 mSv",
        "acquisition_time": "1-30 seconds",
        "contraindications": [
            "Pregnancy (relative)",
            "Severe contrast allergy",
            "Renal insufficiency (for contrast)"
        ],
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 2,
        "modality_name": "Magnetic Resonance Imaging",
        "modality_code": "MRI",
        "description": "Non-invasive imaging using magnetic fields and radio waves",
        "category": "Cross-sectional",
        "radiation_type": "Non-ionizing",
        "contrast_agents": ["Gadolinium-based", "Manganese-based", "Iron oxide"],
        "clinical_applications": [
            "Neurological imaging",
            "Musculoskeletal imaging",
            "Oncologic staging",
            "Cardiac MRI",
            "Breast MRI",
            "Abdominal/pelvic imaging"
        ],
        "advantages": [
            "Excellent soft tissue contrast",
            "No ionizing radiation",
            "Multiplanar imaging",
            "Functional imaging capabilities"
        ],
        "limitations": [
            "Long acquisition times",
            "High cost",
            "Claustrophobia issues",
            "Metal implant contraindications"
        ],
        "typical_dose_range": "0 mSv (no ionizing radiation)",
        "acquisition_time": "15-60 minutes",
        "contraindications": [
            "Certain cardiac pacemakers",
            "Cochlear implants",
            "Metallic foreign bodies",
            "Severe claustrophobia"
        ],
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 3,
        "modality_name": "Ultrasound",
        "modality_code": "US",
        "description": "Real-time imaging using high-frequency sound waves",
        "category": "Real-time",
        "radiation_type": "Non-ionizing",
        "contrast_agents": ["Microbubbles (contrast-enhanced US)"],
        "clinical_applications": [
            "Abdominal imaging",
            "Obstetrics/gynecology",
            "Cardiac echocardiography",
            "Vascular duplex",
            "Breast imaging",
            "Musculoskeletal imaging"
        ],
        "advantages": [
            "Real-time imaging",
            "Portable and bedside",
            "No ionizing radiation",
            "Low cost",
            "Safe in pregnancy"
        ],
        "limitations": [
            "Operator dependent",
            "Limited by acoustic windows",
            "Poor visualization of bone/air",
            "Limited depth penetration"
        ],
        "typical_dose_range": "0 mSv (no ionizing radiation)",
        "acquisition_time": "Real-time",
        "contraindications": [
            "Very few absolute contraindications"
        ],
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 4,
        "modality_name": "X-Ray Radiography",
        "modality_code": "XR",
        "description": "Traditional 2D imaging using X-ray radiation",
        "category": "Projection",
        "radiation_type": "Ionizing",
        "contrast_agents": ["Barium", "Iodinated"],
        "clinical_applications": [
            "Chest radiography",
            "Bone imaging",
            "Abdominal plain films",
            "Contrast studies",
            "Mammography",
            "Dental radiography"
        ],
        "advantages": [
            "Fast and inexpensive",
            "Widely available",
            "Good for bone and chest imaging",
            "Low radiation dose"
        ],
        "limitations": [
            "2D projection only",
            "Limited soft tissue contrast",
            "Superimposition of structures",
            "Ionizing radiation"
        ],
        "typical_dose_range": "0.01-0.1 mSv",
        "acquisition_time": "Milliseconds",
        "contraindications": [
            "Pregnancy (relative)"
        ],
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 5,
        "modality_name": "Nuclear Medicine",
        "modality_code": "NM",
        "description": "Functional imaging using radioactive tracers",
        "category": "Functional",
        "radiation_type": "Ionizing",
        "contrast_agents": ["Radiopharmaceuticals"],
        "clinical_applications": [
            "PET imaging",
            "SPECT imaging",
            "Nuclear cardiology",
            "Thyroid imaging",
            "Bone scans",
            "Renal scans"
        ],
        "advantages": [
            "Functional information",
            "High sensitivity",
            "Molecular imaging capabilities",
            "Quantitative assessment"
        ],
        "limitations": [
            "Ionizing radiation",
            "Limited spatial resolution",
            "Radioactive tracer availability",
            "Long acquisition times"
        ],
        "typical_dose_range": "5-25 mSv",
        "acquisition_time": "15-60 minutes",
        "contraindications": [
            "Pregnancy",
            "Breastfeeding",
            "Severe allergic reactions to tracers"
        ],
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 6,
        "modality_name": "Mammography",
        "modality_code": "MG",
        "description": "Specialized X-ray imaging for breast tissue",
        "category": "Projection",
        "radiation_type": "Ionizing",
        "contrast_agents": ["Iodinated (for contrast-enhanced)"],
        "clinical_applications": [
            "Breast cancer screening",
            "Diagnostic breast imaging",
            "Breast biopsy guidance",
            "Implant assessment"
        ],
        "advantages": [
            "High sensitivity for breast cancer",
            "Low radiation dose",
            "Standardized imaging protocols",
            "Digital enhancement capabilities"
        ],
        "limitations": [
            "Limited to breast imaging",
            "Discomfort during compression",
            "Limited sensitivity in dense breasts",
            "Ionizing radiation"
        ],
        "typical_dose_range": "0.4 mSv (bilateral)",
        "acquisition_time": "10-15 minutes",
        "contraindications": [
            "Pregnancy",
            "Recent breast surgery"
        ],
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 7,
        "modality_name": "Fluoroscopy",
        "modality_code": "RF",
        "description": "Real-time X-ray imaging for dynamic studies",
        "category": "Real-time",
        "radiation_type": "Ionizing",
        "contrast_agents": ["Iodinated", "Barium"],
        "clinical_applications": [
            "Barium studies",
            "Angiography",
            "Interventional procedures",
            "Joint arthrography",
            "GI studies",
            "Urological studies"
        ],
        "advantages": [
            "Real-time visualization",
            "Guidance for procedures",
            "Dynamic assessment",
            "Widely available"
        ],
        "limitations": [
            "High radiation dose",
            "Limited soft tissue contrast",
            "2D projection",
            "Radiation exposure to staff"
        ],
        "typical_dose_range": "2-20 mSv (procedure dependent)",
        "acquisition_time": "Real-time (minutes to hours)",
        "contraindications": [
            "Pregnancy",
            "Contrast allergies"
        ],
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 8,
        "modality_name": "Positron Emission Tomography",
        "modality_code": "PET",
        "description": "Functional imaging using positron-emitting radiotracers",
        "category": "Functional",
        "radiation_type": "Ionizing",
        "contrast_agents": ["FDG and other PET tracers"],
        "clinical_applications": [
            "Oncologic imaging",
            "Neurological imaging",
            "Cardiac imaging",
            "Infection/inflammation imaging",
            "Brain metabolism studies"
        ],
        "advantages": [
            "High sensitivity",
            "Quantitative measurement",
            "Molecular imaging",
            "Early disease detection"
        ],
        "limitations": [
            "High cost",
            "Limited availability",
            "Ionizing radiation",
            "Requires cyclotron nearby"
        ],
        "typical_dose_range": "7-14 mSv",
        "acquisition_time": "15-30 minutes",
        "contraindications": [
            "Pregnancy",
            "Breastfeeding",
            "Severe diabetes (for FDG)"
        ],
        "created_at": "2024-01-01T00:00:00Z"
    }
]

# Modality-specific protocols
MODALITY_PROTOCOLS = [
    {
        "id": 1,
        "modality_code": "CT",
        "protocol_name": "CT Head Non-Contrast",
        "description": "Standard brain CT without contrast",
        "indications": ["Head trauma", "Stroke", "Intracranial hemorrhage"],
        "parameters": {
            "kv": "120",
            "ma": "300",
            "slice_thickness": "5mm",
            "pitch": "1.0",
            "reconstruction": "Standard",
            "coverage": "Base of skull to vertex"
        },
        "contrast_required": False,
        "estimated_dose": "2-3 mSv",
        "acquisition_time": "30 seconds"
    },
    {
        "id": 2,
        "modality_code": "CT",
        "protocol_name": "CT Chest Pulmonary Embolism",
        "description": "CT angiography for pulmonary embolism detection",
        "indications": ["Suspected PE", "Chest pain", "Shortness of breath"],
        "parameters": {
            "kv": "100",
            "ma": "400",
            "slice_thickness": "1mm",
            "pitch": "1.2",
            "reconstruction": "Sharp",
            "coverage": "Lung apices to adrenal glands"
        },
        "contrast_required": True,
        "contrast_type": "Iodinated",
        "estimated_dose": "5-8 mSv",
        "acquisition_time": "15 seconds"
    },
    {
        "id": 3,
        "modality_code": "MRI",
        "protocol_name": "MRI Brain Standard",
        "description": "Comprehensive brain MRI protocol",
        "indications": ["Headache", "Seizure", "Stroke", "Tumor"],
        "parameters": {
            "sequences": ["T1", "T2", "FLAIR", "DWI", "T1-contrast"],
            "field_strength": "1.5T/3T",
            "slice_thickness": "5mm",
            "fov": "22cm",
            "matrix": "256x256"
        },
        "contrast_required": True,
        "contrast_type": "Gadolinium",
        "estimated_dose": "0 mSv",
        "acquisition_time": "30-45 minutes"
    },
    {
        "id": 4,
        "modality_code": "MRI",
        "protocol_name": "MRI Knee",
        "description": "Comprehensive knee MRI for sports medicine",
        "indications": ["Joint pain", "Ligament injury", "Meniscal tear"],
        "parameters": {
            "sequences": ["T1", "T2", "PD", "STIR", "T2-contrast"],
            "field_strength": "1.5T/3T",
            "slice_thickness": "3mm",
            "fov": "16cm",
            "matrix": "256x256"
        },
        "contrast_required": False,
        "estimated_dose": "0 mSv",
        "acquisition_time": "25-35 minutes"
    },
    {
        "id": 5,
        "modality_code": "US",
        "protocol_name": "Abdominal Ultrasound",
        "description": "Complete abdominal ultrasound examination",
        "indications": ["Abdominal pain", "Liver disease", "Gallbladder disease"],
        "parameters": {
            "frequency": "2-5 MHz",
            "depth": "15-20 cm",
            "harmonics": "On",
            "compound": "On",
            "dynamic_range": "60-80 dB"
        },
        "contrast_required": False,
        "estimated_dose": "0 mSv",
        "acquisition_time": "20-30 minutes"
    },
    {
        "id": 6,
        "modality_code": "PET",
        "protocol_name": "FDG PET Whole Body",
        "description": "FDG PET for oncologic staging",
        "indications": ["Cancer staging", "Treatment response", "Recurrence"],
        "parameters": {
            "tracer": "FDG",
            "dose": "370 MBq",
            "uptake_time": "60 minutes",
            "acquisition_time": "15-20 minutes",
            "reconstruction": "OSEM"
        },
        "contrast_required": False,
        "estimated_dose": "7-10 mSv",
        "acquisition_time": "75-90 minutes (total)"
    }
]

# Modality-specific equipment
MODALITY_EQUIPMENT = [
    {
        "id": 1,
        "modality_code": "CT",
        "equipment_name": "Siemens SOMATOM Definition Edge",
        "manufacturer": "Siemens Healthineers",
        "model": "SOMATOM Definition Edge",
        "detector_rows": 64,
        "rotation_time": "0.28s",
        "spatial_resolution": "0.24 mm",
        "temporal_resolution": "75 ms",
        "coverage": "2.0 m",
        "advanced_features": ["Dual energy", "Iterative reconstruction", "Cardiac gating"],
        "clinical_strengths": ["Cardiac imaging", "Trauma", "Oncology"],
        "installation_date": "2023-01-15",
        "status": "Active"
    },
    {
        "id": 2,
        "modality_code": "MRI",
        "equipment_name": "GE Healthcare Signa Pioneer",
        "manufacturer": "GE Healthcare",
        "model": "Signa Pioneer",
        "field_strength": "3.0T",
        "gradient_system": "50 mT/m",
        "slew_rate": "200 T/m/s",
        "coil_system": "AIR coil technology",
        "advanced_features": ["Silent MRI", "Compressed sensing", "3D imaging"],
        "clinical_strengths": ["Neuroimaging", "Musculoskeletal", "Body imaging"],
        "installation_date": "2023-02-20",
        "status": "Active"
    },
    {
        "id": 3,
        "modality_code": "US",
        "equipment_name": "Canon Aplio i900",
        "manufacturer": "Canon Medical Systems",
        "model": "Aplio i900",
        "probe_types": ["Convex", "Linear", "Phased array", "Endocavity"],
        "frequency_range": "1-18 MHz",
        "doppler_capabilities": ["Color", "Power", "PW", "CW"],
        "advanced_features": ["Shear wave elastography", "Contrast-enhanced US", "3D/4D imaging"],
        "clinical_strengths": ["Abdominal", "Cardiac", "Vascular", "OB/GYN"],
        "installation_date": "2023-03-10",
        "status": "Active"
    },
    {
        "id": 4,
        "modality_code": "XR",
        "equipment_name": "Philips DigitalDiagnost",
        "manufacturer": "Philips Healthcare",
        "model": "DigitalDiagnost",
        "detector_type": "Flat panel digital",
        "dynamic_range": "16-bit",
        "spatial_resolution": "2.5 lp/mm",
        "advanced_features": ["Grid pulsing", "Dose management", "Digital tomosynthesis"],
        "clinical_strengths": ["General radiography", "Chest imaging", "Bone imaging"],
        "installation_date": "2023-01-05",
        "status": "Active"
    },
    {
        "id": 5,
        "modality_code": "PET",
        "equipment_name": "Siemens Biograph Horizon",
        "manufacturer": "Siemens Healthineers",
        "model": "Biograph Horizon",
        "pet_resolution": "4.1 mm",
        "ct_component": "64-slice CT",
        "acquisition_mode": "3D and 2D",
        "advanced_features": ["Time-of-flight", "Point spread function", "4D PET"],
        "clinical_strengths": ["Oncology", "Cardiology", "Neurology"],
        "installation_date": "2023-04-15",
        "status": "Active"
    }
]

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    """Root endpoint with comprehensive modality API information"""
    return jsonify({
        "message": "Advanced Medical Imaging Modalities API",
        "version": "3.0.0",
        "description": "Deep dive into medical imaging modalities with comprehensive endpoints",
        "base_url": "http://localhost:5001",
        "modalities_available": [m["modality_code"] for m in MODALITIES_DATA],
        "endpoints": {
            "modalities": {
                "list": "/api/modalities",
                "by_code": "/api/modalities/<modality_code>",
                "by_category": "/api/modalities/category/<category>",
                "by_radiation_type": "/api/modalities/radiation/<radiation_type>",
                "search": "/api/modalities/search"
            },
            "protocols": {
                "list": "/api/protocols",
                "by_modality": "/api/protocols/modality/<modality_code>",
                "by_id": "/api/protocols/<protocol_id>",
                "search": "/api/protocols/search"
            },
            "equipment": {
                "by_modality": "/api/equipment/modality/<modality_code>",
                "by_manufacturer": "/api/equipment/manufacturer/<manufacturer>",
                "advanced_features": "/api/equipment/features"
            },
            "applications": {
                "by_modality": "/api/applications/modality/<modality_code>",
                "by_clinical_area": "/api/applications/clinical/<area>",
                "comparison": "/api/applications/compare"
            },
            "safety": {
                "radiation_dose": "/api/safety/dose",
                "contraindications": "/api/safety/contraindications",
                "contrast_agents": "/api/safety/contrast"
            },
            "workflows": {
                "by_modality": "/api/workflows/modality/<modality_code>",
                "patient_preparation": "/api/workflows/preparation",
                "quality_control": "/api/workflows/quality"
            }
        },
        "timestamp": datetime.datetime.now().isoformat()
    })

# Modality endpoints
@app.route('/api/modalities', methods=['GET'])
def get_modalities():
    """Get all medical imaging modalities"""
    return jsonify({
        "modalities": MODALITIES_DATA,
        "total": len(MODALITIES_DATA),
        "categories": list(set(m["category"] for m in MODALITIES_DATA)),
        "radiation_types": list(set(m["radiation_type"] for m in MODALITIES_DATA)),
        "source": "Advanced Modalities API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/modalities/<modality_code>', methods=['GET'])
def get_modality_by_code(modality_code):
    """Get modality details by code"""
    modality = next((m for m in MODALITIES_DATA if m["modality_code"].upper() == modality_code.upper()), None)
    if modality:
        return jsonify({
            "modality": modality,
            "protocols": [p for p in MODALITY_PROTOCOLS if p["modality_code"] == modality["modality_code"]],
            "equipment": [e for e in MODALITY_EQUIPMENT if e["modality_code"] == modality["modality_code"]],
            "source": "Advanced Modalities API"
        })
    else:
        return jsonify({"error": f"Modality '{modality_code}' not found"}), 404

@app.route('/api/modalities/category/<category>', methods=['GET'])
def get_modalities_by_category(category):
    """Get modalities by category"""
    modalities = [m for m in MODALITIES_DATA if m["category"].lower() == category.lower()]
    return jsonify({
        "modalities": modalities,
        "total": len(modalities),
        "category": category,
        "source": "Advanced Modalities API"
    })

@app.route('/api/modalities/radiation/<radiation_type>', methods=['GET'])
def get_modalities_by_radiation_type(radiation_type):
    """Get modalities by radiation type"""
    modalities = [m for m in MODALITIES_DATA if m["radiation_type"].lower() == radiation_type.lower()]
    return jsonify({
        "modalities": modalities,
        "total": len(modalities),
        "radiation_type": radiation_type,
        "source": "Advanced Modalities API"
    })

@app.route('/api/modalities/search', methods=['GET'])
def search_modalities():
    """Search modalities"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = [m for m in MODALITIES_DATA if 
              query in m['modality_name'].lower() or 
              query in m['modality_code'].lower() or
              query in m['description'].lower() or
              any(query in app.lower() for app in m['clinical_applications'])]
    
    return jsonify({
        "modalities": results,
        "total": len(results),
        "query": query,
        "source": "Advanced Modalities API"
    })

# Protocol endpoints
@app.route('/api/protocols', methods=['GET'])
def get_protocols():
    """Get all modality protocols"""
    return jsonify({
        "protocols": MODALITY_PROTOCOLS,
        "total": len(MODALITY_PROTOCOLS),
        "modalities": list(set(p["modality_code"] for p in MODALITY_PROTOCOLS)),
        "source": "Advanced Modalities API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/protocols/modality/<modality_code>', methods=['GET'])
def get_protocols_by_modality(modality_code):
    """Get protocols by modality"""
    protocols = [p for p in MODALITY_PROTOCOLS if p["modality_code"].upper() == modality_code.upper()]
    return jsonify({
        "protocols": protocols,
        "total": len(protocols),
        "modality_code": modality_code,
        "source": "Advanced Modalities API"
    })

@app.route('/api/protocols/<int:protocol_id>', methods=['GET'])
def get_protocol_by_id(protocol_id):
    """Get protocol by ID"""
    protocol = next((p for p in MODALITY_PROTOCOLS if p["id"] == protocol_id), None)
    if protocol:
        return jsonify({
            "protocol": protocol,
            "source": "Advanced Modalities API"
        })
    else:
        return jsonify({"error": f"Protocol ID '{protocol_id}' not found"}), 404

@app.route('/api/protocols/search', methods=['GET'])
def search_protocols():
    """Search protocols"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = [p for p in MODALITY_PROTOCOLS if 
              query in p['protocol_name'].lower() or 
              query in p['description'].lower() or
              any(query in ind.lower() for ind in p['indications'])]
    
    return jsonify({
        "protocols": results,
        "total": len(results),
        "query": query,
        "source": "Advanced Modalities API"
    })

# Equipment endpoints
@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    """Get all equipment across all modalities"""
    return jsonify({
        "equipment": MODALITY_EQUIPMENT,
        "total": len(MODALITY_EQUIPMENT),
        "modalities": list(set(e["modality_code"] for e in MODALITY_EQUIPMENT)),
        "manufacturers": list(set(e["manufacturer"] for e in MODALITY_EQUIPMENT)),
        "source": "Advanced Modalities API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """Get equipment by ID"""
    equipment = next((e for e in MODALITY_EQUIPMENT if e["id"] == equipment_id), None)
    if equipment:
        return jsonify({
            "equipment": equipment,
            "source": "Advanced Modalities API"
        })
    else:
        return jsonify({"error": f"Equipment ID '{equipment_id}' not found"}), 404

@app.route('/api/equipment/modality/<modality_code>', methods=['GET'])
def get_equipment_by_modality(modality_code):
    """Get equipment by modality"""
    equipment = [e for e in MODALITY_EQUIPMENT if e["modality_code"].upper() == modality_code.upper()]
    return jsonify({
        "equipment": equipment,
        "total": len(equipment),
        "modality_code": modality_code,
        "source": "Advanced Modalities API"
    })

@app.route('/api/equipment/manufacturer/<manufacturer>', methods=['GET'])
def get_equipment_by_manufacturer(manufacturer):
    """Get equipment by manufacturer"""
    equipment = [e for e in MODALITY_EQUIPMENT if manufacturer.lower() in e["manufacturer"].lower()]
    return jsonify({
        "equipment": equipment,
        "total": len(equipment),
        "manufacturer": manufacturer,
        "source": "Advanced Modalities API"
    })

@app.route('/api/equipment/features', methods=['GET'])
def get_equipment_advanced_features():
    """Get equipment with advanced features"""
    features = request.args.get('feature', '').lower()
    
    if features:
        equipment = [e for e in MODALITY_EQUIPMENT 
                    if any(features.lower() in f.lower() for f in e["advanced_features"])]
    else:
        equipment = MODALITY_EQUIPMENT
    
    return jsonify({
        "equipment": equipment,
        "total": len(equipment),
        "feature_filter": features if features else "all",
        "source": "Advanced Modalities API"
    })

# Clinical applications endpoints
@app.route('/api/applications/modality/<modality_code>', methods=['GET'])
def get_applications_by_modality(modality_code):
    """Get clinical applications by modality"""
    modality = next((m for m in MODALITIES_DATA if m["modality_code"].upper() == modality_code.upper()), None)
    if modality:
        return jsonify({
            "modality": modality["modality_name"],
            "modality_code": modality["modality_code"],
            "clinical_applications": modality["clinical_applications"],
            "advantages": modality["advantages"],
            "limitations": modality["limitations"],
            "source": "Advanced Modalities API"
        })
    else:
        return jsonify({"error": f"Modality '{modality_code}' not found"}), 404

@app.route('/api/applications/clinical/<area>', methods=['GET'])
def get_modalities_by_clinical_area(area):
    """Get modalities suitable for clinical area"""
    area = area.lower()
    suitable_modalities = []
    
    for modality in MODALITIES_DATA:
        if any(area in app.lower() for app in modality["clinical_applications"]):
            suitable_modalities.append({
                "modality_name": modality["modality_name"],
                "modality_code": modality["modality_code"],
                "relevant_applications": [app for app in modality["clinical_applications"] 
                                        if area in app.lower()]
            })
    
    return jsonify({
        "clinical_area": area,
        "suitable_modalities": suitable_modalities,
        "total": len(suitable_modalities),
        "source": "Advanced Modalities API"
    })

@app.route('/api/applications/compare', methods=['GET'])
def compare_modalities():
    """Compare multiple modalities"""
    codes = request.args.get('codes', '').split(',')
    if len(codes) < 2:
        return jsonify({"error": "At least 2 modality codes required for comparison"}), 400
    
    comparison_modalities = []
    for code in codes:
        modality = next((m for m in MODALITIES_DATA if m["modality_code"].upper() == code.strip().upper()), None)
        if modality:
            comparison_modalities.append(modality)
    
    if len(comparison_modalities) < 2:
        return jsonify({"error": "Valid modality codes not found"}), 400
    
    # Create comparison matrix
    comparison = {
        "modalities": comparison_modalities,
        "comparison_matrix": {
            "radiation_type": {m["modality_code"]: m["radiation_type"] for m in comparison_modalities},
            "typical_dose": {m["modality_code"]: m["typical_dose_range"] for m in comparison_modalities},
            "acquisition_time": {m["modality_code"]: m["acquisition_time"] for m in comparison_modalities},
            "advantages_count": {m["modality_code"]: len(m["advantages"]) for m in comparison_modalities},
            "limitations_count": {m["modality_code"]: len(m["limitations"]) for m in comparison_modalities}
        },
        "source": "Advanced Modalities API"
    }
    
    return jsonify(comparison)

# Safety endpoints
@app.route('/api/safety/dose', methods=['GET'])
def get_radiation_dose_info():
    """Get radiation dose information by modality"""
    dose_info = []
    for modality in MODALITIES_DATA:
        if modality["radiation_type"] == "Ionizing":
            dose_info.append({
                "modality_name": modality["modality_name"],
                "modality_code": modality["modality_code"],
                "typical_dose_range": modality["typical_dose_range"],
                "acquisition_time": modality["acquisition_time"],
                "radiation_type": modality["radiation_type"]
            })
    
    # Sort by dose range (approximate)
    dose_order = {"XR": 1, "MG": 2, "CT": 3, "RF": 4, "PET": 5, "NM": 6}
    dose_info.sort(key=lambda x: dose_order.get(x["modality_code"], 999))
    
    return jsonify({
        "radiation_dose_info": dose_info,
        "total": len(dose_info),
        "non_ionizing_modalities": [m["modality_name"] for m in MODALITIES_DATA if m["radiation_type"] == "Non-ionizing"],
        "source": "Advanced Modalities API"
    })

@app.route('/api/safety/contraindications', methods=['GET'])
def get_contraindications():
    """Get contraindications by modality"""
    contraindications = {}
    for modality in MODALITIES_DATA:
        contraindications[modality["modality_code"]] = {
            "modality_name": modality["modality_name"],
            "contraindications": modality["contraindications"],
            "radiation_type": modality["radiation_type"]
        }
    
    return jsonify({
        "contraindications": contraindications,
        "source": "Advanced Modalities API"
    })

@app.route('/api/safety/contrast', methods=['GET'])
def get_contrast_agents():
    """Get contrast agents information by modality"""
    contrast_info = {}
    for modality in MODALITIES_DATA:
        contrast_info[modality["modality_code"]] = {
            "modality_name": modality["modality_name"],
            "contrast_agents": modality["contrast_agents"],
            "radiation_type": modality["radiation_type"]
        }
    
    return jsonify({
        "contrast_agents": contrast_info,
        "all_contrast_types": list(set(agent for m in MODALITIES_DATA for agent in m["contrast_agents"])),
        "source": "Advanced Modalities API"
    })

# Workflow endpoints
@app.route('/api/workflows/modality/<modality_code>', methods=['GET'])
def get_workflow_by_modality(modality_code):
    """Get workflow information by modality"""
    modality = next((m for m in MODALITIES_DATA if m["modality_code"].upper() == modality_code.upper()), None)
    if modality:
        protocols = [p for p in MODALITY_PROTOCOLS if p["modality_code"] == modality["modality_code"]]
        equipment = [e for e in MODALITY_EQUIPMENT if e["modality_code"] == modality["modality_code"]]
        
        workflow = {
            "modality": modality,
            "protocols": protocols,
            "equipment": equipment,
            "workflow_steps": [
                "Patient scheduling",
                "Patient preparation",
                "Protocol selection",
                "Equipment setup",
                "Image acquisition",
                "Image processing",
                "Quality control",
                "Report generation",
                "Result communication"
            ],
            "source": "Advanced Modalities API"
        }
        
        return jsonify(workflow)
    else:
        return jsonify({"error": f"Modality '{modality_code}' not found"}), 404

@app.route('/api/workflows/preparation', methods=['GET'])
def get_patient_preparation():
    """Get patient preparation guidelines"""
    modality = request.args.get('modality', '')
    
    if modality:
        mod_data = next((m for m in MODALITIES_DATA if m["modality_code"].upper() == modality.upper()), None)
        if mod_data:
            # Generate preparation guidelines based on modality
            preparation = {
                "modality": mod_data["modality_name"],
                "modality_code": mod_data["modality_code"],
                "general_preparation": [
                    "Verify patient identity",
                    "Check for contraindications",
                    "Explain procedure to patient",
                    "Obtain informed consent"
                ],
                "specific_preparation": [],
                "dietary_restrictions": [],
                "medication_instructions": []
            }
            
            if mod_data["modality_code"] == "CT":
                preparation["specific_preparation"] = [
                    "Remove metallic objects",
                    "Check for contrast allergies",
                    "Assess renal function if contrast needed"
                ]
                preparation["dietary_restrictions"] = [
                    "NPO 4 hours if contrast planned",
                    "Clear liquids allowed"
                ]
            elif mod_data["modality_code"] == "MRI":
                preparation["specific_preparation"] = [
                    "Screen for metallic implants",
                    "Remove all metallic objects",
                    "Check for claustrophobia"
                ]
                preparation["dietary_restrictions"] = [
                    "NPO 4 hours if sedation planned",
                    "No specific restrictions otherwise"
                ]
            elif mod_data["modality_code"] == "US":
                preparation["specific_preparation"] = [
                    "Apply coupling gel",
                    "Position patient appropriately"
                ]
                preparation["dietary_restrictions"] = [
                    "May require fasting for abdominal studies"
                ]
            
            return jsonify(preparation)
        else:
            return jsonify({"error": f"Modality '{modality}' not found"}), 404
    else:
        return jsonify({"error": "Modality parameter required"}), 400

@app.route('/api/workflows/quality', methods=['GET'])
def get_quality_control():
    """Get quality control guidelines"""
    modality = request.args.get('modality', '')
    
    if modality:
        mod_data = next((m for m in MODALITIES_DATA if m["modality_code"].upper() == modality.upper()), None)
        if mod_data:
            qc = {
                "modality": mod_data["modality_name"],
                "modality_code": mod_data["modality_code"],
                "quality_control_measures": [
                    "Daily equipment calibration",
                    "Phantom imaging for quality assurance",
                    "Dose monitoring and optimization",
                    "Image quality assessment",
                    "Protocol adherence verification"
                ],
                "acceptance_criteria": {
                    "image_quality": "Diagnostic quality maintained",
                    "artifacts": "Minimal artifacts not affecting diagnosis",
                    "dose": "Within acceptable reference levels",
                    "coverage": "Complete anatomical coverage"
                },
                "frequency": {
                    "daily": ["Visual inspection", "Basic function checks"],
                    "weekly": ["Phantom imaging", "Dose measurements"],
                    "monthly": ["Comprehensive calibration", "Safety checks"],
                    "annually": ["Full service maintenance", "Physics review"]
                }
            }
            
            return jsonify(qc)
        else:
            return jsonify({"error": f"Modality '{modality}' not found"}), 404
    else:
        return jsonify({"error": "Modality parameter required"}), 400

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Advanced Medical Imaging Modalities API",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "3.0.0",
        "port": 5001,
        "modalities_count": len(MODALITIES_DATA),
        "protocols_count": len(MODALITY_PROTOCOLS),
        "equipment_count": len(MODALITY_EQUIPMENT)
    })

if __name__ == '__main__':
    print("Starting Advanced Medical Imaging Modalities API...")
    print("Port: 5001")
    print("Health: http://localhost:5001/api/health")
    print("Modalities: http://localhost:5001/api/modalities")
    print("Protocols: http://localhost:5001/api/protocols")
    print("Equipment: http://localhost:5001/api/equipment/modality/CT")
    print("Applications: http://localhost:5001/api/applications/clinical/neurology")
    print("Safety: http://localhost:5001/api/safety/dose")
    print("Workflows: http://localhost:5001/api/workflows/modality/MRI")
    app.run(host='0.0.0.0', port=5001, debug=True)
