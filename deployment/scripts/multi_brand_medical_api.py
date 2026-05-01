#!/usr/bin/env python3
"""
Multi-Brand Medical Imaging API
Comprehensive system with GE, Philips, Siemens, Mindray and other manufacturers
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Multi-brand equipment database
MULTI_BRAND_EQUIPMENT = [
    # GE Healthcare Equipment
    {
        "id": 1,
        "manufacturer": "GE Healthcare",
        "brand": "GE",
        "modality_code": "CT",
        "modality_name": "Computed Tomography",
        "equipment_name": "GE Revolution Apex",
        "model": "Revolution Apex",
        "series": "Revolution",
        "detector_rows": 256,
        "rotation_time": "0.28s",
        "spatial_resolution": "0.24 mm",
        "temporal_resolution": "29 ms",
        "coverage": "2.0 m",
        "advanced_features": ["Deep Learning Reconstruction", "Spectral CT", "Cardiac CT", "Perfusion CT"],
        "clinical_strengths": ["Cardiac imaging", "Oncology", "Trauma", "Neurology"],
        "installation_date": "2023-01-15",
        "status": "Active",
        "location": "CT Suite 1",
        "software_version": "AW Server 3.2",
        "contrast_compatibility": ["Iodinated", "Gadolinium"],
        "dose_reduction": "ASiR-V 70%"
    },
    {
        "id": 2,
        "manufacturer": "GE Healthcare",
        "brand": "GE",
        "modality_code": "MRI",
        "modality_name": "Magnetic Resonance Imaging",
        "equipment_name": "GE SIGNA Premier",
        "model": "SIGNA Premier",
        "series": "SIGNA",
        "field_strength": "3.0T",
        "gradient_system": "80 mT/m",
        "slew_rate": "200 T/m/s",
        "coil_system": "AIR Coil Technology",
        "advanced_features": ["Deep Learning Reconstruction", "Silent MRI", "Compressed Sensing", "3D Imaging"],
        "clinical_strengths": ["Neuroimaging", "Musculoskeletal", "Body imaging", "Cardiac MRI"],
        "installation_date": "2023-02-20",
        "status": "Active",
        "location": "MRI Suite 1",
        "software_version": "MP27A",
        "contrast_compatibility": ["Gadolinium-based"],
        "patient_comfort": "70cm bore"
    },
    {
        "id": 3,
        "manufacturer": "GE Healthcare",
        "brand": "GE",
        "modality_code": "US",
        "modality_name": "Ultrasound",
        "equipment_name": "GE Voluson E10",
        "model": "Voluson E10",
        "series": "Voluson",
        "probe_types": ["Convex", "Linear", "Phased array", "Endocavity", "Volume"],
        "frequency_range": "2-18 MHz",
        "doppler_capabilities": ["Color", "Power", "PW", "CW", "M-Mode"],
        "advanced_features": ["HDlive", "RadiantFlow", "SonoCNS", "Contrast-enhanced US"],
        "clinical_strengths": ["OB/GYN", "Radiology", "Vascular", "Breast"],
        "installation_date": "2023-03-10",
        "status": "Active",
        "location": "Ultrasound Room 1",
        "software_version": "M10",
        "contrast_compatibility": ["Microbubbles"],
        "portability": "Mobile cart"
    },
    {
        "id": 4,
        "manufacturer": "GE Healthcare",
        "brand": "GE",
        "modality_code": "XR",
        "modality_name": "X-Ray Radiography",
        "equipment_name": "GE Definium 85",
        "model": "Definium 85",
        "series": "Definium",
        "detector_type": "Flat panel digital",
        "dynamic_range": "16-bit",
        "spatial_resolution": "2.5 lp/mm",
        "advanced_features": ["Grid pulsing", "Dose management", "Digital tomosynthesis", "Auto image stitching"],
        "clinical_strengths": ["General radiography", "Chest imaging", "Bone imaging", "Pediatric"],
        "installation_date": "2023-01-05",
        "status": "Active",
        "location": "X-Ray Room 1",
        "software_version": "RapidView 2.0",
        "contrast_compatibility": ["Iodinated", "Barium"],
        "dose_optimization": "ASiR"
    },
    {
        "id": 5,
        "manufacturer": "GE Healthcare",
        "brand": "GE",
        "modality_code": "RF",
        "modality_name": "Fluoroscopy",
        "equipment_name": "GE OEC Elite C-Arm",
        "model": "OEC Elite",
        "series": "OEC",
        "detector_type": "CMOS flat panel",
        "dynamic_range": "14-bit",
        "spatial_resolution": "2.0 lp/mm",
        "advanced_features": ["Real-time image processing", "Dose reduction", "3D C-arm", "Roadmapping"],
        "clinical_strengths": ["Orthopedic surgery", "Cardiovascular", "Interventional radiology", "Pain management"],
        "installation_date": "2023-04-15",
        "status": "Active",
        "location": "OR Suite 1",
        "software_version": "1.5",
        "contrast_compatibility": ["Iodinated"],
        "mobility": "Mobile C-arm"
    },
    
    # Siemens Healthineers Equipment
    {
        "id": 6,
        "manufacturer": "Siemens Healthineers",
        "brand": "Siemens",
        "modality_code": "CT",
        "modality_name": "Computed Tomography",
        "equipment_name": "Siemens SOMATOM Force",
        "model": "SOMATOM Force",
        "series": "SOMATOM",
        "detector_rows": 192,
        "rotation_time": "0.25s",
        "spatial_resolution": "0.24 mm",
        "temporal_resolution": "66 ms",
        "coverage": "2.0 m",
        "advanced_features": ["Dual Source", "Turbo Flash", "Iterative Reconstruction", "Photon-counting (optional)"],
        "clinical_strengths": ["Cardiac imaging", "Oncology", "Trauma", "Pediatric"],
        "installation_date": "2023-05-10",
        "status": "Active",
        "location": "CT Suite 2",
        "software_version": "Syngo CT VA40",
        "contrast_compatibility": ["Iodinated"],
        "dose_reduction": "ADMIRE 70%"
    },
    {
        "id": 7,
        "manufacturer": "Siemens Healthineers",
        "brand": "Siemens",
        "modality_code": "MRI",
        "modality_name": "Magnetic Resonance Imaging",
        "equipment_name": "Siemens MAGNETOM Vida",
        "model": "MAGNETOM Vida",
        "series": "MAGNETOM",
        "field_strength": "3.0T",
        "gradient_system": "80 mT/m",
        "slew_rate": "200 T/m/s",
        "coil_system": "Tim 4G",
        "advanced_features": ["Deep Learning Reconstruction", "BioMatrix", "Compressed Sensing", "Simultaneous Multi-Slice"],
        "clinical_strengths": ["Neuroimaging", "Musculoskeletal", "Body imaging", "Cardiac MRI"],
        "installation_date": "2023-06-15",
        "status": "Active",
        "location": "MRI Suite 2",
        "software_version": "VE11C",
        "contrast_compatibility": ["Gadolinium-based"],
        "patient_comfort": "70cm bore"
    },
    {
        "id": 8,
        "manufacturer": "Siemens Healthineers",
        "brand": "Siemens",
        "modality_code": "US",
        "modality_name": "Ultrasound",
        "equipment_name": "Siemens Acuson Sequoia",
        "model": "Acuson Sequoia",
        "series": "Acuson",
        "probe_types": ["Convex", "Linear", "Phased array", "Transesophageal", "Intracavity"],
        "frequency_range": "1-18 MHz",
        "doppler_capabilities": ["Color", "Power", "PW", "CW", "M-Mode", "Tissue Doppler"],
        "advanced_features": ["Deep Learning", "Contrast-enhanced US", "Elastography", "3D/4D imaging"],
        "clinical_strengths": ["Cardiology", "Radiology", "Vascular", "OB/GYN"],
        "installation_date": "2023-07-20",
        "status": "Active",
        "location": "Ultrasound Room 2",
        "software_version": "6.0",
        "contrast_compatibility": ["Microbubbles"],
        "portability": "Mobile cart"
    },
    {
        "id": 9,
        "manufacturer": "Siemens Healthineers",
        "brand": "Siemens",
        "modality_code": "XR",
        "modality_name": "X-Ray Radiography",
        "equipment_name": "Siemens YSIO",
        "model": "YSIO",
        "series": "YSIO",
        "detector_type": "Wireless flat panel",
        "dynamic_range": "16-bit",
        "spatial_resolution": "2.5 lp/mm",
        "advanced_features": ["Wireless detectors", "Dose management", "Digital tomosynthesis", "Auto positioning"],
        "clinical_strengths": ["General radiography", "Chest imaging", "Bone imaging", "ICU"],
        "installation_date": "2023-08-25",
        "status": "Active",
        "location": "X-Ray Room 2",
        "software_version": "Syngo Dynamics 10",
        "contrast_compatibility": ["Iodinated", "Barium"],
        "dose_optimization": "CARE Dose4D"
    },
    {
        "id": 10,
        "manufacturer": "Siemens Healthineers",
        "brand": "Siemens",
        "modality_code": "RF",
        "modality_name": "Fluoroscopy",
        "equipment_name": "Siemens Artis zee",
        "model": "Artis zee",
        "series": "Artis",
        "detector_type": "Flat panel",
        "dynamic_range": "14-bit",
        "spatial_resolution": "2.0 lp/mm",
        "advanced_features": ["3D Rotational Angiography", "Dose reduction", "Roadmapping", "Syngo DynaCT"],
        "clinical_strengths": ["Interventional radiology", "Cardiology", "Neurointervention", "Surgery"],
        "installation_date": "2023-09-30",
        "status": "Active",
        "location": "CathLab 1",
        "software_version": "Syngo X-Workplace",
        "contrast_compatibility": ["Iodinated"],
        "mobility": "Fixed ceiling-mounted"
    },
    
    # Philips Healthcare Equipment
    {
        "id": 11,
        "manufacturer": "Philips Healthcare",
        "brand": "Philips",
        "modality_code": "CT",
        "modality_name": "Computed Tomography",
        "equipment_name": "Philips Incisive CT",
        "model": "Incisive CT",
        "series": "Incisive",
        "detector_rows": 128,
        "rotation_time": "0.27s",
        "spatial_resolution": "0.24 mm",
        "temporal_resolution": "45 ms",
        "coverage": "2.0 m",
        "advanced_features": ["iDose4", "Spectral CT", "Cardiac CT", "Iterative reconstruction"],
        "clinical_strengths": ["Oncology", "Cardiology", "Trauma", "Neurology"],
        "installation_date": "2023-10-15",
        "status": "Active",
        "location": "CT Suite 3",
        "software_version": "Portal 9.0",
        "contrast_compatibility": ["Iodinated"],
        "dose_reduction": "iDose4 60%"
    },
    {
        "id": 12,
        "manufacturer": "Philips Healthcare",
        "brand": "Philips",
        "modality_code": "MRI",
        "modality_name": "Magnetic Resonance Imaging",
        "equipment_name": "Philips Ingenia Ambition",
        "model": "Ingenia Ambition",
        "series": "Ingenia",
        "field_strength": "1.5T",
        "gradient_system": "45 mT/m",
        "slew_rate": "200 T/m/s",
        "coil_system": "dStream",
        "advanced_features": ["Compressed SENSE", "3D APT", "MultiTransmit", "SmartExam"],
        "clinical_strengths": ["Neuroimaging", "Musculoskeletal", "Body imaging", "Cardiac MRI"],
        "installation_date": "2023-11-20",
        "status": "Active",
        "location": "MRI Suite 3",
        "software_version": "5.4.0",
        "contrast_compatibility": ["Gadolinium-based"],
        "patient_comfort": "70cm bore"
    },
    {
        "id": 13,
        "manufacturer": "Philips Healthcare",
        "brand": "Philips",
        "modality_code": "US",
        "modality_name": "Ultrasound",
        "equipment_name": "Philips Epiq 7",
        "model": "Epiq 7",
        "series": "Epiq",
        "probe_types": ["Convex", "Linear", "Phased array", "Transesophageal", "Intracavity"],
        "frequency_range": "1-18 MHz",
        "doppler_capabilities": ["Color", "Power", "PW", "CW", "M-Mode", "Tissue Doppler"],
        "advanced_features": ["PureWave", "Anatomical Intelligence", "Contrast-enhanced US", "3D/4D imaging"],
        "clinical_strengths": ["Cardiology", "Radiology", "Vascular", "OB/GYN"],
        "installation_date": "2023-12-25",
        "status": "Active",
        "location": "Ultrasound Room 3",
        "software_version": "5.0",
        "contrast_compatibility": ["Microbubbles"],
        "portability": "Mobile cart"
    },
    {
        "id": 14,
        "manufacturer": "Philips Healthcare",
        "brand": "Philips",
        "modality_code": "XR",
        "modality_name": "X-Ray Radiography",
        "equipment_name": "Philips DigitalDiagnost C90",
        "model": "DigitalDiagnost C90",
        "series": "DigitalDiagnost",
        "detector_type": "Flat panel digital",
        "dynamic_range": "16-bit",
        "spatial_resolution": "2.5 lp/mm",
        "advanced_features": ["Grid pulsing", "Dose management", "Digital tomosynthesis", "Auto stitching"],
        "clinical_strengths": ["General radiography", "Chest imaging", "Bone imaging", "Pediatric"],
        "installation_date": "2024-01-30",
        "status": "Active",
        "location": "X-Ray Room 3",
        "software_version": "R4.1",
        "contrast_compatibility": ["Iodinated", "Barium"],
        "dose_optimization": "DoseWise"
    },
    {
        "id": 15,
        "manufacturer": "Philips Healthcare",
        "brand": "Philips",
        "modality_code": "RF",
        "modality_name": "Fluoroscopy",
        "equipment_name": "Philips Zenition",
        "model": "Zenition",
        "series": "Zenition",
        "detector_type": "Flat panel",
        "dynamic_range": "14-bit",
        "spatial_resolution": "2.0 lp/mm",
        "advanced_features": ["3D C-arm", "Dose reduction", "Roadmapping", "Dynamic range optimization"],
        "clinical_strengths": ["Orthopedic surgery", "Cardiovascular", "Interventional radiology", "Pain management"],
        "installation_date": "2024-02-28",
        "status": "Active",
        "location": "OR Suite 2",
        "software_version": "2.0",
        "contrast_compatibility": ["Iodinated"],
        "mobility": "Mobile C-arm"
    },
    
    # Mindray Equipment
    {
        "id": 16,
        "manufacturer": "Mindray",
        "brand": "Mindray",
        "modality_code": "US",
        "modality_name": "Ultrasound",
        "equipment_name": "Mindray Resona 7",
        "model": "Resona 7",
        "series": "Resona",
        "probe_types": ["Convex", "Linear", "Phased array", "Endocavity", "Intracavity"],
        "frequency_range": "1-18 MHz",
        "doppler_capabilities": ["Color", "Power", "PW", "CW", "M-Mode"],
        "advanced_features": ["Acoustic structure quantification", "Contrast-enhanced US", "Elastography", "3D/4D imaging"],
        "clinical_strengths": ["Radiology", "Cardiology", "OB/GYN", "Vascular"],
        "installation_date": "2024-03-15",
        "status": "Active",
        "location": "Ultrasound Room 4",
        "software_version": "V3.0",
        "contrast_compatibility": ["Microbubbles"],
        "portability": "Mobile cart"
    },
    {
        "id": 17,
        "manufacturer": "Mindray",
        "brand": "Mindray",
        "modality_code": "XR",
        "modality_name": "X-Ray Radiography",
        "equipment_name": "Mindray DigiEye 760",
        "model": "DigiEye 760",
        "series": "DigiEye",
        "detector_type": "Flat panel digital",
        "dynamic_range": "16-bit",
        "spatial_resolution": "2.5 lp/mm",
        "advanced_features": ["Grid pulsing", "Dose management", "Digital tomosynthesis", "Auto exposure"],
        "clinical_strengths": ["General radiography", "Chest imaging", "Bone imaging", "Emergency"],
        "installation_date": "2024-04-20",
        "status": "Active",
        "location": "X-Ray Room 4",
        "software_version": "2.1",
        "contrast_compatibility": ["Iodinated", "Barium"],
        "dose_optimization": "AEC"
    },
    
    # Other Brands (Canon, Fujifilm, etc.)
    {
        "id": 18,
        "manufacturer": "Canon Medical Systems",
        "brand": "Canon",
        "modality_code": "CT",
        "modality_name": "Computed Tomography",
        "equipment_name": "Canon Aquilion Prime SP",
        "model": "Aquilion Prime SP",
        "series": "Aquilion",
        "detector_rows": 160,
        "rotation_time": "0.275s",
        "spatial_resolution": "0.24 mm",
        "temporal_resolution": "35 ms",
        "coverage": "2.0 m",
        "advanced_features": ["Deep Learning Reconstruction", "Spectral CT", "Cardiac CT", "Iterative reconstruction"],
        "clinical_strengths": ["Oncology", "Cardiology", "Trauma", "Neurology"],
        "installation_date": "2024-05-25",
        "status": "Active",
        "location": "CT Suite 4",
        "software_version": "v6.0",
        "contrast_compatibility": ["Iodinated"],
        "dose_reduction": "AIDR 3D 70%"
    },
    {
        "id": 19,
        "manufacturer": "Canon Medical Systems",
        "brand": "Canon",
        "modality_code": "MRI",
        "modality_name": "Magnetic Resonance Imaging",
        "equipment_name": "Canon Vantage Orian",
        "model": "Vantage Orian",
        "series": "Vantage",
        "field_strength": "1.5T",
        "gradient_system": "45 mT/m",
        "slew_rate": "200 T/m/s",
        "coil_system": "Atlas",
        "advanced_features": ["Deep Learning Reconstruction", "Compressed Sensing", "4D MRI", "Silent MRI"],
        "clinical_strengths": ["Neuroimaging", "Musculoskeletal", "Body imaging", "Cardiac MRI"],
        "installation_date": "2024-06-30",
        "status": "Active",
        "location": "MRI Suite 4",
        "software_version": "v7.0",
        "contrast_compatibility": ["Gadolinium-based"],
        "patient_comfort": "70cm bore"
    },
    {
        "id": 20,
        "manufacturer": "Fujifilm Healthcare",
        "brand": "Fujifilm",
        "modality_code": "XR",
        "modality_name": "X-Ray Radiography",
        "equipment_name": "Fujifilm FDR Go",
        "model": "FDR Go",
        "series": "FDR",
        "detector_type": "Wireless flat panel",
        "dynamic_range": "16-bit",
        "spatial_resolution": "2.5 lp/mm",
        "advanced_features": ["Wireless detectors", "Dose management", "Digital tomosynthesis", "Mobile DR"],
        "clinical_strengths": ["General radiography", "Chest imaging", "Bone imaging", "Mobile imaging"],
        "installation_date": "2024-07-15",
        "status": "Active",
        "location": "X-Ray Room 5",
        "software_version": "v2.0",
        "contrast_compatibility": ["Iodinated", "Barium"],
        "dose_optimization": "DRI"
    },
    {
        "id": 21,
        "manufacturer": "Shimadzu",
        "brand": "Shimadzu",
        "modality_code": "XR",
        "modality_name": "X-Ray Radiography",
        "equipment_name": "Shimadzu RADspeed Pro",
        "model": "RADspeed Pro",
        "series": "RADspeed",
        "detector_type": "Flat panel digital",
        "dynamic_range": "16-bit",
        "spatial_resolution": "2.5 lp/mm",
        "advanced_features": ["Grid pulsing", "Dose management", "Digital tomosynthesis", "Auto positioning"],
        "clinical_strengths": ["General radiography", "Chest imaging", "Bone imaging", "ICU"],
        "installation_date": "2024-08-20",
        "status": "Active",
        "location": "X-Ray Room 6",
        "software_version": "v3.0",
        "contrast_compatibility": ["Iodinated", "Barium"],
        "dose_optimization": "AEC"
    }
]

# Manufacturer-specific protocols
MANUFACTURER_PROTOCOLS = [
    # GE Healthcare Protocols
    {
        "id": 1,
        "manufacturer": "GE Healthcare",
        "modality_code": "CT",
        "protocol_name": "GE Revolution Apex Cardiac CT",
        "description": "Cardiac CT with deep learning reconstruction",
        "indications": ["Coronary artery disease", "Cardiac anomalies", "Pre-operative assessment"],
        "parameters": {
            "kv": "120",
            "ma": "400",
            "slice_thickness": "0.625mm",
            "pitch": "0.99",
            "reconstruction": "DLIR (Deep Learning)",
            "coverage": "Cardiac coverage",
            "ecg_gating": "Retrospective",
            "contrast_protocol": "70ml @ 4ml/s"
        },
        "contrast_required": True,
        "contrast_type": "Iodinated",
        "estimated_dose": "5-8 mSv",
        "acquisition_time": "5-10 seconds",
        "equipment_compatibility": ["GE Revolution Apex", "GE Revolution CT"],
        "advanced_features": ["Deep Learning Reconstruction", "Spectral CT"]
    },
    {
        "id": 2,
        "manufacturer": "GE Healthcare",
        "modality_code": "MRI",
        "protocol_name": "GE SIGNA Premier Brain Protocol",
        "description": "Comprehensive brain MRI with deep learning",
        "indications": ["Stroke", "Tumor", "Dementia", "Multiple sclerosis"],
        "parameters": {
            "sequences": ["T1", "T2", "FLAIR", "DWI", "SWI", "T1-contrast"],
            "field_strength": "3.0T",
            "slice_thickness": "5mm",
            "fov": "22cm",
            "matrix": "256x256",
            "reconstruction": "Deep Learning"
        },
        "contrast_required": True,
        "contrast_type": "Gadolinium",
        "estimated_dose": "0 mSv",
        "acquisition_time": "30-45 minutes",
        "equipment_compatibility": ["GE SIGNA Premier", "GE SIGNA Architect"],
        "advanced_features": ["Deep Learning Reconstruction", "Silent MRI"]
    },
    
    # Siemens Healthineers Protocols
    {
        "id": 3,
        "manufacturer": "Siemens Healthineers",
        "modality_code": "CT",
        "protocol_name": "Siemens SOMATOM Force Dual Energy",
        "description": "Dual source dual energy CT",
        "indications": ["Pulmonary embolism", "Material characterization", "Virtual non-contrast"],
        "parameters": {
            "kv": "80/140Sn",
            "ma": "200/150",
            "slice_thickness": "0.6mm",
            "pitch": "1.2",
            "reconstruction": "ADMIRE",
            "coverage": "Chest to pelvis",
            "dual_energy": "True",
            "contrast_protocol": "80ml @ 3ml/s"
        },
        "contrast_required": True,
        "contrast_type": "Iodinated",
        "estimated_dose": "6-10 mSv",
        "acquisition_time": "3-5 seconds",
        "equipment_compatibility": ["Siemens SOMATOM Force", "Siemens SOMATOM Definition"],
        "advanced_features": ["Dual Source", "Turbo Flash", "Dual Energy"]
    },
    {
        "id": 4,
        "manufacturer": "Siemens Healthineers",
        "modality_code": "MRI",
        "protocol_name": "Siemens MAGNETOM Vida Neuro Protocol",
        "description": "Advanced neuroimaging with BioMatrix",
        "indications": ["Brain tumors", "Stroke", "Neurodegeneration", "Epilepsy"],
        "parameters": {
            "sequences": ["T1", "T2", "FLAIR", "DWI", "SWI", "T1-contrast", "Perfusion"],
            "field_strength": "3.0T",
            "slice_thickness": "5mm",
            "fov": "22cm",
            "matrix": "256x256",
            "reconstruction": "Deep Learning"
        },
        "contrast_required": True,
        "contrast_type": "Gadolinium",
        "estimated_dose": "0 mSv",
        "acquisition_time": "35-50 minutes",
        "equipment_compatibility": ["Siemens MAGNETOM Vida", "Siemens MAGNETOM Prisma"],
        "advanced_features": ["BioMatrix", "Deep Learning Reconstruction", "Perfusion MRI"]
    },
    
    # Philips Healthcare Protocols
    {
        "id": 5,
        "manufacturer": "Philips Healthcare",
        "modality_code": "CT",
        "protocol_name": "Philips Incisive CT Oncology Protocol",
        "description": "Oncology imaging with iDose4",
        "indications": ["Tumor staging", "Treatment response", "Metastasis detection"],
        "parameters": {
            "kv": "120",
            "ma": "250",
            "slice_thickness": "1mm",
            "pitch": "1.0",
            "reconstruction": "iDose4",
            "coverage": "Chest to pelvis",
            "contrast_protocol": "100ml @ 3ml/s"
        },
        "contrast_required": True,
        "contrast_type": "Iodinated",
        "estimated_dose": "8-12 mSv",
        "acquisition_time": "10-15 seconds",
        "equipment_compatibility": ["Philips Incisive CT", "Philips Brilliance CT"],
        "advanced_features": ["iDose4", "Spectral CT", "Iterative reconstruction"]
    },
    {
        "id": 6,
        "manufacturer": "Philips Healthcare",
        "modality_code": "MRI",
        "protocol_name": "Philips Ingenia Ambition MSK Protocol",
        "description": "Musculoskeletal imaging with Compressed SENSE",
        "indications": ["Joint pain", "Sports injuries", "Ligament tears", "Meniscal injuries"],
        "parameters": {
            "sequences": ["T1", "T2", "PD", "STIR", "T2-contrast"],
            "field_strength": "1.5T",
            "slice_thickness": "3mm",
            "fov": "16cm",
            "matrix": "256x256",
            "reconstruction": "Compressed SENSE"
        },
        "contrast_required": False,
        "estimated_dose": "0 mSv",
        "acquisition_time": "25-35 minutes",
        "equipment_compatibility": ["Philips Ingenia Ambition", "Philips Achieva"],
        "advanced_features": ["Compressed SENSE", "MultiTransmit", "SmartExam"]
    },
    
    # Mindray Protocols
    {
        "id": 7,
        "manufacturer": "Mindray",
        "modality_code": "US",
        "protocol_name": "Mindray Resona 7 Abdominal Protocol",
        "description": "Comprehensive abdominal ultrasound",
        "indications": ["Abdominal pain", "Liver disease", "Gallbladder disease", "Kidney evaluation"],
        "parameters": {
            "frequency": "2-5 MHz",
            "depth": "15-20 cm",
            "harmonics": "On",
            "compound": "On",
            "dynamic_range": "60-80 dB",
            "contrast_mode": "Optional"
        },
        "contrast_required": False,
        "estimated_dose": "0 mSv",
        "acquisition_time": "20-30 minutes",
        "equipment_compatibility": ["Mindray Resona 7", "Mindray DC-80"],
        "advanced_features": ["Acoustic structure quantification", "Contrast-enhanced US"]
    },
    
    # Other Manufacturer Protocols
    {
        "id": 8,
        "manufacturer": "Canon Medical Systems",
        "modality_code": "CT",
        "protocol_name": "Canon Aquilion Prime SP Cardiac Protocol",
        "description": "Cardiac CT with deep learning reconstruction",
        "indications": ["Coronary artery disease", "Cardiac anomalies", "Pre-operative assessment"],
        "parameters": {
            "kv": "120",
            "ma": "350",
            "slice_thickness": "0.5mm",
            "pitch": "0.99",
            "reconstruction": "AIDR 3D",
            "coverage": "Cardiac coverage",
            "ecg_gating": "Retrospective",
            "contrast_protocol": "70ml @ 4ml/s"
        },
        "contrast_required": True,
        "contrast_type": "Iodinated",
        "estimated_dose": "5-8 mSv",
        "acquisition_time": "5-10 seconds",
        "equipment_compatibility": ["Canon Aquilion Prime SP", "Canon Aquilion One"],
        "advanced_features": ["Deep Learning Reconstruction", "Spectral CT"]
    }
]

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    """Root endpoint with multi-brand API information"""
    return jsonify({
        "message": "Multi-Brand Medical Imaging API",
        "version": "4.0.0",
        "description": "Comprehensive system with GE, Philips, Siemens, Mindray and other manufacturers",
        "base_url": "http://localhost:5001",
        "manufacturers": list(set(e["manufacturer"] for e in MULTI_BRAND_EQUIPMENT)),
        "brands": list(set(e["brand"] for e in MULTI_BRAND_EQUIPMENT)),
        "modalities": list(set(e["modality_code"] for e in MULTI_BRAND_EQUIPMENT)),
        "total_equipment": len(MULTI_BRAND_EQUIPMENT),
        "total_protocols": len(MANUFACTURER_PROTOCOLS),
        "endpoints": {
            "equipment": {
                "all": "/api/equipment",
                "by_manufacturer": "/api/equipment/manufacturer/<manufacturer>",
                "by_brand": "/api/equipment/brand/<brand>",
                "by_modality": "/api/equipment/modality/<modality_code>",
                "by_id": "/api/equipment/<id>",
                "compare": "/api/equipment/compare",
                "features": "/api/equipment/features"
            },
            "protocols": {
                "all": "/api/protocols",
                "by_manufacturer": "/api/protocols/manufacturer/<manufacturer>",
                "by_modality": "/api/protocols/modality/<modality_code>",
                "by_equipment": "/api/protocols/equipment/<equipment_name>",
                "by_id": "/api/protocols/<id>",
                "search": "/api/protocols/search"
            },
            "manufacturers": {
                "list": "/api/manufacturers",
                "by_name": "/api/manufacturers/<manufacturer>",
                "comparison": "/api/manufacturers/compare",
                "market_share": "/api/manufacturers/market_share"
            },
            "modalities": {
                "by_manufacturer": "/api/modalities/manufacturer/<manufacturer>",
                "comparison": "/api/modalities/compare",
                "market_analysis": "/api/modalities/market_analysis"
            }
        },
        "timestamp": datetime.datetime.now().isoformat()
    })

# Equipment endpoints
@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    """Get all multi-brand equipment"""
    return jsonify({
        "equipment": MULTI_BRAND_EQUIPMENT,
        "total": len(MULTI_BRAND_EQUIPMENT),
        "manufacturers": list(set(e["manufacturer"] for e in MULTI_BRAND_EQUIPMENT)),
        "brands": list(set(e["brand"] for e in MULTI_BRAND_EQUIPMENT)),
        "modalities": list(set(e["modality_code"] for e in MULTI_BRAND_EQUIPMENT)),
        "source": "Multi-Brand Medical Imaging API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/equipment/manufacturer/<manufacturer>', methods=['GET'])
def get_equipment_by_manufacturer(manufacturer):
    """Get equipment by manufacturer"""
    equipment = [e for e in MULTI_BRAND_EQUIPMENT if manufacturer.lower() in e["manufacturer"].lower()]
    return jsonify({
        "equipment": equipment,
        "total": len(equipment),
        "manufacturer": manufacturer,
        "modalities": list(set(e["modality_code"] for e in equipment)),
        "source": "Multi-Brand Medical Imaging API"
    })

@app.route('/api/equipment/brand/<brand>', methods=['GET'])
def get_equipment_by_brand(brand):
    """Get equipment by brand"""
    equipment = [e for e in MULTI_BRAND_EQUIPMENT if e["brand"].lower() == brand.lower()]
    return jsonify({
        "equipment": equipment,
        "total": len(equipment),
        "brand": brand,
        "modalities": list(set(e["modality_code"] for e in equipment)),
        "source": "Multi-Brand Medical Imaging API"
    })

@app.route('/api/equipment/modality/<modality_code>', methods=['GET'])
def get_equipment_by_modality(modality_code):
    """Get equipment by modality"""
    equipment = [e for e in MULTI_BRAND_EQUIPMENT if e["modality_code"].upper() == modality_code.upper()]
    return jsonify({
        "equipment": equipment,
        "total": len(equipment),
        "modality_code": modality_code,
        "manufacturers": list(set(e["manufacturer"] for e in equipment)),
        "source": "Multi-Brand Medical Imaging API"
    })

@app.route('/api/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """Get equipment by ID"""
    equipment = next((e for e in MULTI_BRAND_EQUIPMENT if e["id"] == equipment_id), None)
    if equipment:
        return jsonify({
            "equipment": equipment,
            "source": "Multi-Brand Medical Imaging API"
        })
    else:
        return jsonify({"error": f"Equipment ID '{equipment_id}' not found"}), 404

@app.route('/api/equipment/compare', methods=['GET'])
def compare_equipment():
    """Compare equipment from different manufacturers"""
    manufacturers = request.args.get('manufacturers', '').split(',')
    modality = request.args.get('modality', '')
    
    if not manufacturers:
        return jsonify({"error": "Manufacturers parameter required"}), 400
    
    comparison_equipment = []
    for manufacturer in manufacturers:
        equipment_list = [e for e in MULTI_BRAND_EQUIPMENT 
                        if manufacturer.lower() in e["manufacturer"].lower()]
        if modality:
            equipment_list = [e for e in equipment_list if e["modality_code"].upper() == modality.upper()]
        comparison_equipment.extend(equipment_list)
    
    if len(comparison_equipment) < 2:
        return jsonify({"error": "Need at least 2 equipment items for comparison"}), 400
    
    # Create comparison matrix
    comparison = {
        "equipment": comparison_equipment,
        "comparison_matrix": {
            "manufacturers": [e["manufacturer"] for e in comparison_equipment],
            "models": [e["model"] for e in comparison_equipment],
            "modality": [e["modality_name"] for e in comparison_equipment],
            "advanced_features_count": [len(e["advanced_features"]) for e in comparison_equipment],
            "clinical_strengths_count": [len(e["clinical_strengths"]) for e in comparison_equipment]
        },
        "source": "Multi-Brand Medical Imaging API"
    }
    
    return jsonify(comparison)

@app.route('/api/equipment/features', methods=['GET'])
def get_equipment_by_features():
    """Get equipment by advanced features"""
    feature = request.args.get('feature', '').lower()
    
    if feature:
        equipment = [e for e in MULTI_BRAND_EQUIPMENT 
                    if any(feature.lower() in f.lower() for f in e["advanced_features"])]
    else:
        equipment = MULTI_BRAND_EQUIPMENT
    
    return jsonify({
        "equipment": equipment,
        "total": len(equipment),
        "feature_filter": feature if feature else "all",
        "source": "Multi-Brand Medical Imaging API"
    })

# Protocol endpoints
@app.route('/api/protocols', methods=['GET'])
def get_protocols():
    """Get all manufacturer-specific protocols"""
    return jsonify({
        "protocols": MANUFACTURER_PROTOCOLS,
        "total": len(MANUFACTURER_PROTOCOLS),
        "manufacturers": list(set(p["manufacturer"] for p in MANUFACTURER_PROTOCOLS)),
        "modalities": list(set(p["modality_code"] for p in MANUFACTURER_PROTOCOLS)),
        "source": "Multi-Brand Medical Imaging API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/protocols/manufacturer/<manufacturer>', methods=['GET'])
def get_protocols_by_manufacturer(manufacturer):
    """Get protocols by manufacturer"""
    protocols = [p for p in MANUFACTURER_PROTOCOLS if manufacturer.lower() in p["manufacturer"].lower()]
    return jsonify({
        "protocols": protocols,
        "total": len(protocols),
        "manufacturer": manufacturer,
        "modalities": list(set(p["modality_code"] for p in protocols)),
        "source": "Multi-Brand Medical Imaging API"
    })

@app.route('/api/protocols/modality/<modality_code>', methods=['GET'])
def get_protocols_by_modality(modality_code):
    """Get protocols by modality"""
    protocols = [p for p in MANUFACTURER_PROTOCOLS if p["modality_code"].upper() == modality_code.upper()]
    return jsonify({
        "protocols": protocols,
        "total": len(protocols),
        "modality_code": modality_code,
        "manufacturers": list(set(p["manufacturer"] for p in protocols)),
        "source": "Multi-Brand Medical Imaging API"
    })

@app.route('/api/protocols/equipment/<equipment_name>', methods=['GET'])
def get_protocols_by_equipment(equipment_name):
    """Get protocols compatible with specific equipment"""
    protocols = [p for p in MANUFACTURER_PROTOCOLS 
                if equipment_name.lower() in str(p["equipment_compatibility"]).lower()]
    return jsonify({
        "protocols": protocols,
        "total": len(protocols),
        "equipment_name": equipment_name,
        "manufacturers": list(set(p["manufacturer"] for p in protocols)),
        "source": "Multi-Brand Medical Imaging API"
    })

@app.route('/api/protocols/<int:protocol_id>', methods=['GET'])
def get_protocol_by_id(protocol_id):
    """Get protocol by ID"""
    protocol = next((p for p in MANUFACTURER_PROTOCOLS if p["id"] == protocol_id), None)
    if protocol:
        return jsonify({
            "protocol": protocol,
            "source": "Multi-Brand Medical Imaging API"
        })
    else:
        return jsonify({"error": f"Protocol ID '{protocol_id}' not found"}), 404

@app.route('/api/protocols/search', methods=['GET'])
def search_protocols():
    """Search protocols"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = [p for p in MANUFACTURER_PROTOCOLS if 
              query in p['protocol_name'].lower() or 
              query in p['description'].lower() or
              any(query in ind.lower() for ind in p['indications'])]
    
    return jsonify({
        "protocols": results,
        "total": len(results),
        "query": query,
        "source": "Multi-Brand Medical Imaging API"
    })

# Manufacturer endpoints
@app.route('/api/manufacturers', methods=['GET'])
def get_manufacturers():
    """Get all manufacturers with statistics"""
    manufacturer_stats = {}
    
    for equipment in MULTI_BRAND_EQUIPMENT:
        manufacturer = equipment["manufacturer"]
        if manufacturer not in manufacturer_stats:
            manufacturer_stats[manufacturer] = {
                "manufacturer": manufacturer,
                "brand": equipment["brand"],
                "equipment_count": 0,
                "modalities": [],
                "advanced_features": [],
                "total_protocols": 0
            }
        
        manufacturer_stats[manufacturer]["equipment_count"] += 1
        if equipment["modality_code"] not in manufacturer_stats[manufacturer]["modalities"]:
            manufacturer_stats[manufacturer]["modalities"].append(equipment["modality_code"])
        manufacturer_stats[manufacturer]["advanced_features"].extend(equipment["advanced_features"])
    
    # Count protocols for each manufacturer
    for protocol in MANUFACTURER_PROTOCOLS:
        manufacturer = protocol["manufacturer"]
        if manufacturer in manufacturer_stats:
            manufacturer_stats[manufacturer]["total_protocols"] += 1
    
    # Remove duplicate advanced features
    for manufacturer in manufacturer_stats:
        manufacturer_stats[manufacturer]["advanced_features"] = list(set(manufacturer_stats[manufacturer]["advanced_features"]))
    
    return jsonify({
        "manufacturers": list(manufacturer_stats.values()),
        "total_manufacturers": len(manufacturer_stats),
        "total_equipment": len(MULTI_BRAND_EQUIPMENT),
        "total_protocols": len(MANUFACTURER_PROTOCOLS),
        "source": "Multi-Brand Medical Imaging API"
    })

@app.route('/api/manufacturers/<manufacturer>', methods=['GET'])
def get_manufacturer_details(manufacturer):
    """Get detailed manufacturer information"""
    equipment = [e for e in MULTI_BRAND_EQUIPMENT if manufacturer.lower() in e["manufacturer"].lower()]
    protocols = [p for p in MANUFACTURER_PROTOCOLS if manufacturer.lower() in p["manufacturer"].lower()]
    
    if not equipment:
        return jsonify({"error": f"Manufacturer '{manufacturer}' not found"}), 404
    
    manufacturer_info = {
        "manufacturer": manufacturer,
        "brand": equipment[0]["brand"],
        "equipment": equipment,
        "equipment_count": len(equipment),
        "protocols": protocols,
        "protocol_count": len(protocols),
        "modalities": list(set(e["modality_code"] for e in equipment)),
        "advanced_features": list(set(feature for e in equipment for feature in e["advanced_features"])),
        "clinical_strengths": list(set(strength for e in equipment for strength in e["clinical_strengths"])),
        "source": "Multi-Brand Medical Imaging API"
    }
    
    return jsonify(manufacturer_info)

@app.route('/api/manufacturers/compare', methods=['GET'])
def compare_manufacturers():
    """Compare manufacturers"""
    manufacturers = request.args.get('manufacturers', '').split(',')
    if len(manufacturers) < 2:
        return jsonify({"error": "At least 2 manufacturers required for comparison"}), 400
    
    comparison_data = {}
    for manufacturer in manufacturers:
        equipment = [e for e in MULTI_BRAND_EQUIPMENT if manufacturer.lower() in e["manufacturer"].lower()]
        protocols = [p for p in MANUFACTURER_PROTOCOLS if manufacturer.lower() in p["manufacturer"].lower()]
        
        comparison_data[manufacturer] = {
            "equipment_count": len(equipment),
            "protocol_count": len(protocols),
            "modalities": list(set(e["modality_code"] for e in equipment)),
            "advanced_features_count": len(set(feature for e in equipment for feature in e["advanced_features"]))
        }
    
    return jsonify({
        "manufacturers": manufacturers,
        "comparison": comparison_data,
        "source": "Multi-Brand Medical Imaging API"
    })

@app.route('/api/manufacturers/market_share', methods=['GET'])
def get_market_share():
    """Get market share analysis"""
    total_equipment = len(MULTI_BRAND_EQUIPMENT)
    market_share = {}
    
    for equipment in MULTI_BRAND_EQUIPMENT:
        manufacturer = equipment["manufacturer"]
        if manufacturer not in market_share:
            market_share[manufacturer] = 0
        market_share[manufacturer] += 1
    
    # Calculate percentages
    for manufacturer in market_share:
        market_share[manufacturer] = {
            "equipment_count": market_share[manufacturer],
            "market_share_percentage": round((market_share[manufacturer] / total_equipment) * 100, 1)
        }
    
    return jsonify({
        "market_share": market_share,
        "total_equipment": total_equipment,
        "source": "Multi-Brand Medical Imaging API"
    })

# Modality endpoints
@app.route('/api/modalities/manufacturer/<manufacturer>', methods=['GET'])
def get_modalities_by_manufacturer(manufacturer):
    """Get modalities available from specific manufacturer"""
    equipment = [e for e in MULTI_BRAND_EQUIPMENT if manufacturer.lower() in e["manufacturer"].lower()]
    modalities = {}
    
    for modality_code in set(e["modality_code"] for e in equipment):
        modality_equipment = [e for e in equipment if e["modality_code"] == modality_code]
        modalities[modality_code] = {
            "modality_code": modality_code,
            "modality_name": modality_equipment[0]["modality_name"],
            "equipment_count": len(modality_equipment),
            "equipment": modality_equipment
        }
    
    return jsonify({
        "manufacturer": manufacturer,
        "modalities": modalities,
        "total_modalities": len(modalities),
        "source": "Multi-Brand Medical Imaging API"
    })

@app.route('/api/modalities/compare', methods=['GET'])
def compare_modalities():
    """Compare modalities across manufacturers"""
    modality = request.args.get('modality', '')
    if not modality:
        return jsonify({"error": "Modality parameter required"}), 400
    
    equipment = [e for e in MULTI_BRAND_EQUIPMENT if e["modality_code"].upper() == modality.upper()]
    
    if not equipment:
        return jsonify({"error": f"Modality '{modality}' not found"}), 404
    
    comparison = {
        "modality": modality,
        "modality_name": equipment[0]["modality_name"],
        "manufacturers": list(set(e["manufacturer"] for e in equipment)),
        "equipment": equipment,
        "manufacturer_comparison": {}
    }
    
    for manufacturer in set(e["manufacturer"] for e in equipment):
        manufacturer_equipment = [e for e in equipment if e["manufacturer"] == manufacturer]
        comparison["manufacturer_comparison"][manufacturer] = {
            "equipment_count": len(manufacturer_equipment),
            "models": [e["model"] for e in manufacturer_equipment],
            "advanced_features": list(set(feature for e in manufacturer_equipment for feature in e["advanced_features"]))
        }
    
    return jsonify(comparison)

@app.route('/api/modalities/market_analysis', methods=['GET'])
def get_modality_market_analysis():
    """Get modality market analysis"""
    modality_stats = {}
    
    for equipment in MULTI_BRAND_EQUIPMENT:
        modality = equipment["modality_code"]
        if modality not in modality_stats:
            modality_stats[modality] = {
                "modality_name": equipment["modality_name"],
                "equipment_count": 0,
                "manufacturers": [],
                "advanced_features": [],
                "clinical_applications": []
            }
        
        modality_stats[modality]["equipment_count"] += 1
        if equipment["manufacturer"] not in modality_stats[modality]["manufacturers"]:
            modality_stats[modality]["manufacturers"].append(equipment["manufacturer"])
        modality_stats[modality]["advanced_features"].extend(equipment["advanced_features"])
        modality_stats[modality]["clinical_applications"].extend(equipment["clinical_strengths"])
    
    # Remove duplicates and sort
    for modality in modality_stats:
        modality_stats[modality]["manufacturers"] = sorted(list(set(modality_stats[modality]["manufacturers"])))
        modality_stats[modality]["advanced_features"] = list(set(modality_stats[modality]["advanced_features"]))
        modality_stats[modality]["clinical_applications"] = list(set(modality_stats[modality]["clinical_applications"]))
    
    return jsonify({
        "modality_analysis": modality_stats,
        "total_modalities": len(modality_stats),
        "source": "Multi-Brand Medical Imaging API"
    })

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Multi-Brand Medical Imaging API",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "4.0.0",
        "port": 5001,
        "total_equipment": len(MULTI_BRAND_EQUIPMENT),
        "total_protocols": len(MANUFACTURER_PROTOCOLS),
        "manufacturers": list(set(e["manufacturer"] for e in MULTI_BRAND_EQUIPMENT)),
        "modalities": list(set(e["modality_code"] for e in MULTI_BRAND_EQUIPMENT))
    })

if __name__ == '__main__':
    print("Starting Multi-Brand Medical Imaging API...")
    print("Port: 5001")
    print("Health: http://localhost:5001/api/health")
    print("All Equipment: http://localhost:5001/api/equipment")
    print("Manufacturers: http://localhost:5001/api/manufacturers")
    print("GE Equipment: http://localhost:5001/api/equipment/manufacturer/GE")
    print("Siemens Equipment: http://localhost:5001/api/equipment/manufacturer/Siemens")
    print("Philips Equipment: http://localhost:5001/api/equipment/manufacturer/Philips")
    print("Mindray Equipment: http://localhost:5001/api/equipment/manufacturer/Mindray")
    print("All Protocols: http://localhost:5001/api/protocols")
    print("Compare Manufacturers: http://localhost:5001/api/manufacturers/compare?manufacturers=GE,Siemens")
    print("Modality Comparison: http://localhost:5001/api/modalities/compare?modality=CT")
    app.run(host='0.0.0.0', port=5001, debug=True)
