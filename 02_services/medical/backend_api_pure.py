"""
Medical Imaging Backend API - Pure Backend
RESTful API server for medical imaging modalities on port 5001
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all modality modules
from core.US_ultrasound_imaging import UltrasoundImaging
from core.XR_xray_imaging import XRayImaging
from core.CARM_fluoroscopy_imaging import CArmFluoroscopy
from core.CT_scan_imaging import CTImaging
from core.MR_scan_imaging import MRIImaging
from core.cathlab_imaging import CathLabImaging
from modality_comparison import ModalityComparison

# Import DICOM integration modules
from dicom_integration import DICOMManager
from dicom_network import DICOMNetwork, DICOMStorageManager
from dicom_pacs_integration import PACSIntegration

# Import image processing
from image_processor import ImageProcessor
from image_plotter import MedicalImagePlotter
from equipment_specs import equipment_registry
from nifti_processor import NIfTIProcessor
from nifti_visualizer import NIfTIVisualizer
from vessel_identifier import VesselIdentifier
from bone_identifier import BoneIdentifier

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize all modalities
modalities = {
    'ultrasound': UltrasoundImaging(),
    'xray': XRayImaging(),
    'carm': CArmFluoroscopy(),
    'ct': CTImaging(),
    'mri': MRIImaging(),
    'cathlab': CathLabImaging()
}

# Initialize DICOM components
dicom_manager = DICOMManager()
dicom_network = DICOMNetwork()
pacs_integration = PACSIntegration()
modality_comparison = ModalityComparison()

@app.route('/')
def api_root():
    """API root endpoint with available endpoints"""
    return jsonify({
        'api_name': 'Medical Imaging Backend API',
        'version': '2.0',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'modalities': '/api/modalities',
            'modality_detail': '/api/modalities/<modality_name>',
            'modality_characteristics': '/api/modalities/<modality_name>/characteristics',
            'anatomical_structures': '/api/modalities/<modality_name>/anatomy',
            'identification_checklist': '/api/modalities/<modality_name>/checklist/<structure_type>',
            'safety_guidelines': '/api/modalities/<modality_name>/safety',
            'report_templates': '/api/templates/<modality_name>',
            'dicom_status': '/api/dicom/status',
            'dicom_operations': '/api/dicom/operations',
            'pacs_status': '/api/pacs/status',
            'modality_comparison': '/api/comparison',
            'clinical_scenarios': '/api/scenarios',
            'image_processing': '/api/images/process',
            'image_analysis': '/api/images/analyze/<filename>',
            'plotting': '/api/plotting',
            'plot_individual': '/api/plotting/individual',
            'plot_comparison': '/api/plotting/comparison',
            'plot_contrast': '/api/plotting/contrast',
            'plot_dashboard': '/api/plotting/dashboard',
            'equipment_specs': '/api/equipment/<modality>',
            'equipment_exams': '/api/equipment/<modality>/exams',
            'equipment_all': '/api/equipment',
            'nifti_process': '/api/nifti/process',
            'nifti_visualize': '/api/nifti/visualize',
            'nifti_slices': '/api/nifti/slices',
            'nifti_masks': '/api/nifti/masks',
            'nifti_summary': '/api/nifti/summary',
            'vessel_identify': '/api/vessels/identify',
            'vessel_visualize': '/api/vessels/visualize',
            'vessel_analyze': '/api/vessels/analyze/<image_path>',
            'bones_identify': '/api/bones/identify',
            'bones_visualize': '/api/bones/visualize',
            'bones_analyze': '/api/bones/analyze/<image_path>',
            'system_health': '/api/health'
        }
    })

@app.route('/api/modalities')
def get_modalities():
    """Get list of all available modalities"""
    modality_list = []
    for key, modality in modalities.items():
        modality_list.append({
            'id': key,
            'name': modality.modality_name,
            'characteristics_summary': {
                'imaging_type': modality.characteristics.get('imaging_principle', 'N/A'),
                'radiation': modality.characteristics.get('radiation', 'N/A'),
                'real_time': modality.characteristics.get('real_time', False)
            }
        })
    return jsonify({
        'modalities': modality_list,
        'count': len(modality_list)
    })

@app.route('/api/modalities/<modality_name>')
def get_modality_detail(modality_name):
    """Get detailed information about a specific modality"""
    if modality_name not in modalities:
        return jsonify({'error': 'Modality not found'}), 404
    
    modality = modalities[modality_name]
    return jsonify({
        'id': modality_name,
        'name': modality.modality_name,
        'characteristics': modality.characteristics,
        'anatomical_structures': modality.anatomical_structures,
        'available_checklists': list(modality.identification_checklist.keys()) if hasattr(modality, 'identification_checklist') else []
    })

@app.route('/api/modalities/<modality_name>/characteristics')
def get_modality_characteristics(modality_name):
    """Get characteristics of a specific modality"""
    if modality_name not in modalities:
        return jsonify({'error': 'Modality not found'}), 404
    
    modality = modalities[modality_name]
    return jsonify({
        'modality': modality_name,
        'characteristics': modality.characteristics
    })

@app.route('/api/modalities/<modality_name>/anatomy')
def get_anatomical_structures(modality_name):
    """Get anatomical structures for a specific modality"""
    if modality_name not in modalities:
        return jsonify({'error': 'Modality not found'}), 404
    
    modality = modalities[modality_name]
    return jsonify({
        'modality': modality_name,
        'anatomical_structures': modality.anatomical_structures
    })

@app.route('/api/modalities/<modality_name>/checklist/<structure_type>')
def get_identification_checklist(modality_name, structure_type):
    """Get identification checklist for specific structure type"""
    if modality_name not in modalities:
        return jsonify({'error': 'Modality not found'}), 404
    
    modality = modalities[modality_name]
    checklist = modality.get_identification_checklist(structure_type)
    
    if not checklist:
        return jsonify({'error': f'Checklist for {structure_type} not found'}), 404
    
    return jsonify({
        'modality': modality_name,
        'structure_type': structure_type,
        'checklist': checklist
    })

@app.route('/api/modalities/<modality_name>/safety')
def get_safety_guidelines(modality_name):
    """Get safety guidelines for a specific modality"""
    if modality_name not in modalities:
        return jsonify({'error': 'Modality not found'}), 404
    
    modality = modalities[modality_name]
    if hasattr(modality, 'safety_parameters'):
        return jsonify({
            'modality': modality_name,
            'safety_guidelines': modality.safety_parameters
        })
    else:
        return jsonify({'error': 'Safety guidelines not available for this modality'}), 404

@app.route('/api/templates/<modality_name>')
def get_report_template(modality_name):
    """Get report template for a specific modality"""
    if modality_name not in modalities:
        return jsonify({'error': 'Modality not found'}), 404
    
    modality = modalities[modality_name]
    
    # Generate report template based on modality type
    if modality_name == 'ct':
        template = modality.generate_ct_report_template()
    elif modality_name == 'mri':
        template = modality.generate_mri_report_template()
    elif modality_name == 'cathlab':
        template = modality.generate_cathlab_report_template()
    else:
        template = f"Report template for {modality.modality_name}\n{'='*50}\n[PATIENT INFORMATION]\n[TECHNICAL PARAMETERS]\n[FINDINGS]\n[IMPRESSION]\n[RECOMMENDATIONS]"
    
    return jsonify({
        'modality': modality_name,
        'template': template,
        'generated_at': datetime.now().isoformat()
    })

@app.route('/api/dicom/status')
def get_dicom_status():
    """Get DICOM system status"""
    return jsonify({
        'dicom_manager': {
            'status': 'active',
            'capabilities': ['file_creation', 'metadata_management', 'validation']
        },
        'dicom_network': {
            'status': 'ready',
            'operations': ['C-STORE', 'C-FIND', 'C-MOVE', 'C-GET', 'C-ECHO']
        },
        'pacs_integration': {
            'status': 'active',
            'database': 'SQLite',
            'features': ['patient_management', 'study_management', 'storage']
        }
    })

@app.route('/api/dicom/operations', methods=['GET', 'POST'])
def dicom_operations():
    """Handle DICOM operations"""
    if request.method == 'GET':
        return jsonify({
            'available_operations': [
                'create_dicom_file',
                'validate_dicom',
                'extract_metadata',
                'store_dicom',
                'query_dicom',
                'retrieve_dicom'
            ]
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        operation = data.get('operation')
        
        if operation == 'create_dicom_file':
            # Simulate DICOM file creation
            return jsonify({
                'operation': 'create_dicom_file',
                'status': 'success',
                'file_id': f"DICOM_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'message': 'DICOM file created successfully'
            })
        else:
            return jsonify({'error': 'Operation not implemented'}), 501

@app.route('/api/pacs/status')
def get_pacs_status():
    """Get PACS system status"""
    return jsonify({
        'pacs_status': 'active',
        'database_type': 'SQLite',
        'storage_path': './dicom_storage',
        'statistics': {
            'total_patients': 0,
            'total_studies': 0,
            'total_series': 0,
            'total_images': 0
        }
    })

@app.route('/api/comparison')
def get_modality_comparison():
    """Get modality comparison tools"""
    return jsonify({
        'comparison_tools': {
            'radiation_dose': {
                'ultrasound': '0 mSv',
                'xray': '0.1-0.5 mSv',
                'carm': '2-10 mSv',
                'ct': '2-20 mSv',
                'mri': '0 mSv',
                'cathlab': '5-15 mSv'
            },
            'contrast_media': {
                'ultrasound': 'Microbubble contrast',
                'xray': 'Iodinated contrast',
                'carm': 'Iodinated contrast',
                'ct': 'Iodinated contrast',
                'mri': 'Gadolinium contrast',
                'cathlab': 'Iodinated contrast'
            },
            'procedure_time': {
                'ultrasound': '15-30 minutes',
                'xray': '5-15 minutes',
                'carm': '30-90 minutes',
                'ct': '10-30 minutes',
                'mri': '30-90 minutes',
                'cathlab': '60-180 minutes'
            }
        }
    })

@app.route('/api/scenarios')
def get_clinical_scenarios():
    """Get clinical scenario recommendations"""
    scenarios = {
        'trauma': {
            'recommended_modalities': ['xray', 'ct', 'ultrasound'],
            'primary_choice': 'ct',
            'reasoning': 'Fast, comprehensive assessment of injuries'
        },
        'stroke': {
            'recommended_modalities': ['ct', 'mri'],
            'primary_choice': 'mri',
            'reasoning': 'Superior for early stroke detection and tissue characterization'
        },
        'abdominal_pain': {
            'recommended_modalities': ['ultrasound', 'ct'],
            'primary_choice': 'ct',
            'reasoning': 'Comprehensive abdominal assessment'
        },
        'musculoskeletal': {
            'recommended_modalities': ['xray', 'ultrasound', 'mri'],
            'primary_choice': 'mri',
            'reasoning': 'Best soft tissue detail for ligaments and tendons'
        },
        'vascular_disease': {
            'recommended_modalities': ['ultrasound', 'ct', 'mri', 'cathlab'],
            'primary_choice': 'cathlab',
            'reasoning': 'Gold standard for vascular intervention'
        }
    }
    
    return jsonify({
        'clinical_scenarios': scenarios
    })

@app.route('/api/health')
def system_health():
    """System health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'api_server': 'running',
            'modalities': 'active',
            'dicom': 'ready',
            'pacs': 'active'
        },
        'version': '2.0',
        'uptime': 'active'
    })

@app.route('/api/images/process', methods=['GET', 'POST'])
def process_images():
    """Process images from Low Contrast MRI folder"""
    try:
        # Initialize image processor with default folder
        processor = ImageProcessor("../Low Contrast MRI")
        
        if request.method == 'GET':
            return jsonify(processor.get_api_response())
        
        elif request.method == 'POST':
            data = request.get_json()
            custom_folder = data.get('folder_path') if data else None
            
            if custom_folder:
                processor = ImageProcessor(custom_folder)
            
            return jsonify(processor.get_api_response())
            
    except Exception as e:
        return jsonify({'error': f'Image processing failed: {str(e)}'}), 500

@app.route('/api/images/analyze/<filename>')
def analyze_specific_image(filename):
    """Analyze specific image file"""
    try:
        processor = ImageProcessor("../Low Contrast MRI")
        
        if filename in processor.processed_images:
            return jsonify({
                'filename': filename,
                'analysis': processor.processed_images[filename]
            })
        else:
            return jsonify({'error': 'Image not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/plotting/individual', methods=['GET'])
def plot_individual_images():
    """Generate individual images plot"""
    try:
        plotter = MedicalImagePlotter("../Low Contrast MRI")
        
        # Save plot to file and return path
        plot_path = f"plots/individual_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('plots', exist_ok=True)
        
        plotter.plot_all_images(save_path=plot_path)
        
        return jsonify({
            'status': 'success',
            'plot_type': 'individual_images',
            'plot_path': plot_path,
            'message': 'Individual images plot generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Plotting failed: {str(e)}'}), 500

@app.route('/api/plotting/comparison', methods=['GET'])
def plot_comparison_grid():
    """Generate comparison grid plot"""
    try:
        plotter = MedicalImagePlotter("../Low Contrast MRI")
        
        # Save plot to file
        plot_path = f"plots/comparison_grid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('plots', exist_ok=True)
        
        plotter.plot_comparison_grid(save_path=plot_path)
        
        return jsonify({
            'status': 'success',
            'plot_type': 'comparison_grid',
            'plot_path': plot_path,
            'message': 'Comparison grid plot generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Plotting failed: {str(e)}'}), 500

@app.route('/api/plotting/contrast', methods=['GET'])
def plot_contrast_analysis():
    """Generate contrast analysis plot"""
    try:
        plotter = MedicalImagePlotter("../Low Contrast MRI")
        
        # Save plot to file
        plot_path = f"plots/contrast_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('plots', exist_ok=True)
        
        plotter.plot_contrast_analysis(save_path=plot_path)
        
        return jsonify({
            'status': 'success',
            'plot_type': 'contrast_analysis',
            'plot_path': plot_path,
            'message': 'Contrast analysis plot generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Plotting failed: {str(e)}'}), 500

@app.route('/api/plotting/dashboard', methods=['GET'])
def plot_summary_dashboard():
    """Generate summary dashboard plot"""
    try:
        plotter = MedicalImagePlotter("../Low Contrast MRI")
        
        # Save plot to file
        plot_path = f"plots/summary_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('plots', exist_ok=True)
        
        plotter.plot_summary_dashboard(save_path=plot_path)
        
        return jsonify({
            'status': 'success',
            'plot_type': 'summary_dashboard',
            'plot_path': plot_path,
            'message': 'Summary dashboard plot generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Plotting failed: {str(e)}'}), 500

@app.route('/api/equipment/<modality>')
def get_equipment_specs(modality):
    """Get equipment specifications for a modality"""
    try:
        specs = equipment_registry.get_equipment_specs(modality)
        if not specs:
            return jsonify({'error': f'No equipment specs found for {modality}'}), 404
        
        return jsonify({
            'modality': modality,
            'equipment_specs': specs,
            'manufacturers': specs.get('manufacturers', []),
            'total_manufacturers': len(specs.get('manufacturers', []))
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get equipment specs: {str(e)}'}), 500

@app.route('/api/equipment/<modality>/exams')
def get_equipment_exams(modality):
    """Get all exam types for a modality"""
    try:
        all_exams = equipment_registry.get_all_exams_for_modality(modality)
        exam_types = equipment_registry.get_exam_types(modality)
        
        return jsonify({
            'modality': modality,
            'total_exams': len(all_exams),
            'exam_types': exam_types,
            'all_exams': all_exams
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get exam types: {str(e)}'}), 500

@app.route('/api/equipment')
def get_all_equipment():
    """Get all equipment specifications"""
    try:
        all_specs = {}
        for modality in ['ultrasound', 'xray', 'ct', 'mri', 'mammo', 'carm', 'cathlab']:
            specs = equipment_registry.get_equipment_specs(modality)
            if specs:
                all_specs[modality] = specs
        
        return jsonify({
            'total_modalities': len(all_specs),
            'equipment_specs': all_specs,
            'supported_manufacturers': {
                'ultrasound': ['GE Voluson', 'Siemens', 'Philips'],
                'xray': ['GE Definium HD 656'],
                'ct': ['GE Revolution CT'],
                'mri': ['GE Signa Magnus', 'GE Signa MRI (all models)'],
                'mammo': ['GE Healthcare Mammography'],
                'carm': ['GE Catheter and Vessels'],
                'cathlab': ['GE Image Guide']
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get all equipment specs: {str(e)}'}), 500

@app.route('/api/nifti/process', methods=['GET', 'POST'])
def process_nifti():
    """Process NIfTI neuroimaging files"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        folder_path = data.get('folder_path') if data else "C:/Users/TTR/Documents/Calculus/mni_colin27_1998_nifti"
        
        processor = NIfTIProcessor(folder_path)
        return jsonify(processor.get_api_response())
        
    except Exception as e:
        return jsonify({'error': f'NIfTI processing failed: {str(e)}'}), 500

@app.route('/api/nifti/slices', methods=['GET'])
def visualize_nifti_slices():
    """Generate brain slices visualization"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        folder_path = data.get('folder_path') if data else "C:/Users/TTR/Documents/Calculus/mni_colin27_1998_nifti"
        
        visualizer = NIfTIVisualizer(folder_path)
        
        # Save plot to file
        plot_path = f"plots/nifti_brain_slices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('plots', exist_ok=True)
        
        visualizer.plot_brain_slices(save_path=plot_path)
        
        return jsonify({
            'status': 'success',
            'plot_type': 'nifti_brain_slices',
            'plot_path': plot_path,
            'message': 'NIfTI brain slices visualization generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'NIfTI visualization failed: {str(e)}'}), 500

@app.route('/api/nifti/masks', methods=['GET'])
def visualize_nifti_masks():
    """Generate mask comparison visualization"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        folder_path = data.get('folder_path') if data else "C:/Users/TTR/Documents/Calculus/mni_colin27_1998_nifti"
        
        visualizer = NIfTIVisualizer(folder_path)
        
        # Save plot to file
        plot_path = f"plots/nifti_mask_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('plots', exist_ok=True)
        
        visualizer.plot_mask_comparison(save_path=plot_path)
        
        return jsonify({
            'status': 'success',
            'plot_type': 'nifti_mask_comparison',
            'plot_path': plot_path,
            'message': 'NIfTI mask comparison visualization generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'NIfTI mask visualization failed: {str(e)}'}), 500

@app.route('/api/nifti/summary', methods=['GET'])
def visualize_nifti_summary():
    """Generate dataset summary visualization"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        folder_path = data.get('folder_path') if data else "C:/Users/TTR/Documents/Calculus/mni_colin27_1998_nifti"
        
        visualizer = NIfTIVisualizer(folder_path)
        
        # Save plot to file
        plot_path = f"plots/nifti_dataset_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('plots', exist_ok=True)
        
        visualizer.plot_dataset_summary(save_path=plot_path)
        
        return jsonify({
            'status': 'success',
            'plot_type': 'nifti_dataset_summary',
            'plot_path': plot_path,
            'message': 'NIfTI dataset summary visualization generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'NIfTI summary visualization failed: {str(e)}'}), 500

@app.route('/api/nifti/visualize', methods=['GET'])
def visualize_all_nifti():
    """Generate all NIfTI visualizations"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        folder_path = data.get('folder_path') if data else "C:/Users/TTR/Documents/Calculus/mni_colin27_1998_nifti"
        
        visualizer = NIfTIVisualizer(folder_path)
        
        # Generate all plots
        plots = {}
        os.makedirs('plots', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Brain slices
        slices_path = f"plots/nifti_brain_slices_{timestamp}.png"
        visualizer.plot_brain_slices(save_path=slices_path)
        plots['brain_slices'] = slices_path
        
        # Mask comparison
        masks_path = f"plots/nifti_mask_comparison_{timestamp}.png"
        visualizer.plot_mask_comparison(save_path=masks_path)
        plots['mask_comparison'] = masks_path
        
        # Dataset summary
        summary_path = f"plots/nifti_dataset_summary_{timestamp}.png"
        visualizer.plot_dataset_summary(save_path=summary_path)
        plots['dataset_summary'] = summary_path
        
        return jsonify({
            'status': 'success',
            'visualizations': plots,
            'total_plots': len(plots),
            'message': 'All NIfTI visualizations generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'NIfTI visualization failed: {str(e)}'}), 500

@app.route('/api/vessels/identify', methods=['GET', 'POST'])
def identify_vessels():
    """Identify vessels in medical image"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        image_path = data.get('image_path') if data else "../Low Contrast MRI/Flair01_01.jpg"
        detection_method = data.get('method', 'frangi')
        
        vessel_id = VesselIdentifier()
        results = vessel_id.identify_vessels(image_path, detection_method)
        
        return jsonify({
            'status': 'success' if 'error' not in results else 'error',
            'image_path': image_path,
            'detection_method': detection_method,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Vessel identification failed: {str(e)}'}), 500

@app.route('/api/vessels/visualize', methods=['GET', 'POST'])
def visualize_vessels():
    """Generate vessel identification visualization"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        image_path = data.get('image_path') if data else "../Low Contrast MRI/Flair01_01.jpg"
        detection_method = data.get('method', 'frangi')
        
        vessel_id = VesselIdentifier()
        
        # Save visualization
        plot_path = f"plots/vessel_identification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('plots', exist_ok=True)
        
        vessel_id.visualize_vessels(image_path, detection_method, plot_path)
        
        return jsonify({
            'status': 'success',
            'plot_type': 'vessel_identification',
            'plot_path': plot_path,
            'image_path': image_path,
            'detection_method': detection_method,
            'message': 'Vessel identification visualization generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Vessel visualization failed: {str(e)}'}), 500

@app.route('/api/vessels/analyze/<path:image_path>')
def analyze_specific_vessels(image_path):
    """Analyze vessels in specific image"""
    try:
        detection_method = request.args.get('method', 'frangi')
        
        vessel_id = VesselIdentifier()
        results = vessel_id.identify_vessels(image_path, detection_method)
        
        if 'error' in results:
            return jsonify({'error': results['error']}), 404
        
        return jsonify({
            'status': 'success',
            'image_path': image_path,
            'detection_method': detection_method,
            'vessel_analysis': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Vessel analysis failed: {str(e)}'}), 500

@app.route('/api/bones/identify', methods=['GET', 'POST'])
def identify_bones():
    """Identify bones in medical image"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        image_path = data.get('image_path') if data else "../Low Contrast MRI/Flair01_01.jpg"
        detection_method = data.get('method', 'threshold')
        
        bone_id = BoneIdentifier()
        results = bone_id.identify_bones(image_path, detection_method)
        
        return jsonify({
            'status': 'success' if 'error' not in results else 'error',
            'image_path': image_path,
            'detection_method': detection_method,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Bone identification failed: {str(e)}'}), 500

@app.route('/api/bones/visualize', methods=['GET', 'POST'])
def visualize_bones():
    """Generate bone identification visualization"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        image_path = data.get('image_path') if data else "../Low Contrast MRI/Flair01_01.jpg"
        detection_method = data.get('method', 'threshold')
        
        bone_id = BoneIdentifier()
        
        # Save visualization
        plot_path = f"plots/bone_identification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('plots', exist_ok=True)
        
        bone_id.visualize_bones(image_path, detection_method, plot_path)
        
        return jsonify({
            'status': 'success',
            'plot_type': 'bone_identification',
            'plot_path': plot_path,
            'image_path': image_path,
            'detection_method': detection_method,
            'message': 'Bone identification visualization generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Bone visualization failed: {str(e)}'}), 500

@app.route('/api/bones/analyze/<path:image_path>')
def analyze_specific_bones(image_path):
    """Analyze bones in specific image"""
    try:
        detection_method = request.args.get('method', 'threshold')
        
        bone_id = BoneIdentifier()
        results = bone_id.identify_bones(image_path, detection_method)
        
        if 'error' in results:
            return jsonify({'error': results['error']}), 404
        
        return jsonify({
            'status': 'success',
            'image_path': image_path,
            'detection_method': detection_method,
            'bone_analysis': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Bone analysis failed: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Medical Imaging Backend API...")
    print("API Documentation: http://localhost:5001/")
    print("Health Check: http://localhost:5001/api/health")
    print("Available Modalities: http://localhost:5001/api/modalities")
    print("Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=5001, debug=False)  # Production mode
