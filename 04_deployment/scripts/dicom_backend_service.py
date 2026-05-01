#!/usr/bin/env python3
"""
DICOM Backend Service
Complete DICOM file processing, parsing, and rendering backend
Mirrors frontend functionality with actual medical image processing
"""

import os
import json
import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pydicom
from pydicom import dcmread
from PIL import Image, ImageEnhance
import numpy as np
import io
import base64
from werkzeug.utils import secure_filename
import jwt
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DICOM_FOLDER'] = 'uploads/dicom'
app.config['THUMBNAIL_FOLDER'] = 'uploads/thumbnails'
app.config['PROCESSED_FOLDER'] = 'uploads/processed'

# JWT Secret
JWT_SECRET = 'your_super_secret_jwt_key_here_change_in_production'

# Create upload directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DICOM_FOLDER'], exist_ok=True)
os.makedirs(app.config['THUMBNAIL_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Authentication middleware
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = data['email']
        except:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

class DICOMProcessor:
    def __init__(self):
        self.supported_formats = ['.dcm', '.dicom', '.dic', '.ima']
        
    def is_dicom_file(self, file_path):
        """Check if file is a valid DICOM file"""
        try:
            ds = pydicom.dcmread(file_path)
            return True
        except:
            return False
    
    def extract_metadata(self, file_path):
        """Extract comprehensive DICOM metadata"""
        try:
            ds = pydicom.dcmread(file_path)
            
            # Extract key metadata
            metadata = {
                'file_info': {
                    'file_name': os.path.basename(file_path),
                    'file_size': os.path.getsize(file_path),
                    'file_hash': self.calculate_file_hash(file_path)
                },
                'patient_info': {
                    'patient_id': getattr(ds, 'PatientID', ''),
                    'patient_name': str(getattr(ds, 'PatientName', '')),
                    'patient_birth_date': str(getattr(ds, 'PatientBirthDate', '')),
                    'patient_sex': getattr(ds, 'PatientSex', ''),
                    'patient_age': str(getattr(ds, 'PatientAge', ''))
                },
                'study_info': {
                    'study_instance_uid': getattr(ds, 'StudyInstanceUID', ''),
                    'study_date': str(getattr(ds, 'StudyDate', '')),
                    'study_time': str(getattr(ds, 'StudyTime', '')),
                    'study_description': str(getattr(ds, 'StudyDescription', '')),
                    'accession_number': str(getattr(ds, 'AccessionNumber', ''))
                },
                'series_info': {
                    'series_instance_uid': getattr(ds, 'SeriesInstanceUID', ''),
                    'series_number': getattr(ds, 'SeriesNumber', ''),
                    'series_description': str(getattr(ds, 'SeriesDescription', '')),
                    'modality': getattr(ds, 'Modality', ''),
                    'body_part_examined': str(getattr(ds, 'BodyPartExamined', ''))
                },
                'image_info': {
                    'sop_instance_uid': getattr(ds, 'SOPInstanceUID', ''),
                    'instance_number': getattr(ds, 'InstanceNumber', ''),
                    'rows': getattr(ds, 'Rows', 0),
                    'columns': getattr(ds, 'Columns', 0),
                    'bits_allocated': getattr(ds, 'BitsAllocated', 0),
                    'bits_stored': getattr(ds, 'BitsStored', 0),
                    'high_bit': getattr(ds, 'HighBit', 0),
                    'pixel_representation': getattr(ds, 'PixelRepresentation', 0),
                    'samples_per_pixel': getattr(ds, 'SamplesPerPixel', 0),
                    'photometric_interpretation': str(getattr(ds, 'PhotometricInterpretation', ''))
                },
                'equipment_info': {
                    'manufacturer': str(getattr(ds, 'Manufacturer', '')),
                    'manufacturer_model_name': str(getattr(ds, 'ManufacturerModelName', '')),
                    'station_name': str(getattr(ds, 'StationName', '')),
                    'institution_name': str(getattr(ds, 'InstitutionName', ''))
                }
            }
            
            return metadata
            
        except Exception as e:
            return {'error': f'Failed to extract metadata: {str(e)}'}
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def get_pixel_array(self, file_path):
        """Extract pixel array from DICOM file"""
        try:
            ds = pydicom.dcmread(file_path)
            
            if hasattr(ds, 'pixel_array'):
                pixel_array = ds.pixel_array
                
                # Apply window/level if available
                if hasattr(ds, 'WindowCenter') and hasattr(ds, 'WindowWidth'):
                    window_center = ds.WindowCenter
                    window_width = ds.WindowWidth
                    
                    if isinstance(window_center, list):
                        window_center = window_center[0]
                    if isinstance(window_width, list):
                        window_width = window_width[0]
                    
                    pixel_array = self.apply_window_level(pixel_array, window_center, window_width)
                
                return pixel_array
            else:
                return None
                
        except Exception as e:
            return None
    
    def apply_window_level(self, pixel_array, window_center, window_width):
        """Apply window/level adjustment to pixel array"""
        min_pixel = window_center - window_width // 2
        max_pixel = window_center + window_width // 2
        
        pixel_array = np.clip(pixel_array, min_pixel, max_pixel)
        pixel_array = ((pixel_array - min_pixel) / (max_pixel - min_pixel) * 255).astype(np.uint8)
        
        return pixel_array
    
    def create_thumbnail(self, file_path, size=(200, 200)):
        """Create thumbnail from DICOM image"""
        try:
            pixel_array = self.get_pixel_array(file_path)
            
            if pixel_array is None:
                return None
            
            # Convert to PIL Image
            if len(pixel_array.shape) == 2:
                # Grayscale image
                image = Image.fromarray(pixel_array, mode='L')
            elif len(pixel_array.shape) == 3:
                # RGB image
                image = Image.fromarray(pixel_array, mode='RGB')
            else:
                return None
            
            # Resize to thumbnail size
            image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Convert to RGB if grayscale
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            return image
            
        except Exception as e:
            return None
    
    def save_thumbnail(self, file_path, thumbnail_path, size=(200, 200)):
        """Save thumbnail to file"""
        try:
            thumbnail = self.create_thumbnail(file_path, size)
            
            if thumbnail:
                thumbnail.save(thumbnail_path, 'JPEG', quality=85)
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def convert_to_png(self, file_path, output_path):
        """Convert DICOM to PNG format"""
        try:
            pixel_array = self.get_pixel_array(file_path)
            
            if pixel_array is None:
                return False
            
            # Convert to PIL Image
            if len(pixel_array.shape) == 2:
                # Grayscale image
                image = Image.fromarray(pixel_array, mode='L')
            elif len(pixel_array.shape) == 3:
                # RGB image
                image = Image.fromarray(pixel_array, mode='RGB')
            else:
                return False
            
            # Save as PNG
            image.save(output_path, 'PNG')
            return True
            
        except Exception as e:
            return False
    
    def enhance_image(self, file_path, enhancement_type='contrast'):
        """Enhance DICOM image"""
        try:
            pixel_array = self.get_pixel_array(file_path)
            
            if pixel_array is None:
                return None
            
            # Convert to PIL Image
            image = Image.fromarray(pixel_array, mode='L')
            
            # Apply enhancement
            if enhancement_type == 'contrast':
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.5)
            elif enhancement_type == 'brightness':
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(1.2)
            elif enhancement_type == 'sharpness':
                enhancer = ImageEnhance.Sharpness(image)
                image = enhancer.enhance(2.0)
            
            return image
            
        except Exception as e:
            return None
    
    def get_image_statistics(self, file_path):
        """Calculate image statistics"""
        try:
            pixel_array = self.get_pixel_array(file_path)
            
            if pixel_array is None:
                return None
            
            stats = {
                'min_value': float(np.min(pixel_array)),
                'max_value': float(np.max(pixel_array)),
                'mean_value': float(np.mean(pixel_array)),
                'std_value': float(np.std(pixel_array)),
                'shape': pixel_array.shape,
                'dtype': str(pixel_array.dtype)
            }
            
            return stats
            
        except Exception as e:
            return None

# Initialize DICOM processor
dicom_processor = DICOMProcessor()

# Routes

@app.route('/api/dicom/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'DICOM Backend Service',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'supported_formats': dicom_processor.supported_formats
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authentication endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Simple authentication (replace with real database check)
        valid_users = [
            {'email': 'test@example.com', 'password': 'test123', 'role': 'admin'},
            {'email': 'doctor@medical.com', 'password': 'doctor123', 'role': 'doctor'},
            {'email': 'radiologist@medical.com', 'password': 'rad123', 'role': 'radiologist'}
        ]
        
        user = next((u for u in valid_users if u['email'] == email and u['password'] == password), None)
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token = jwt.encode({
            'email': user['email'],
            'role': user['role']
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'email': user['email'],
                'role': user['role']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dicom/upload', methods=['POST'])
@require_auth
def upload_dicom():
    """Upload DICOM file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in dicom_processor.supported_formats:
            return jsonify({'error': f'Unsupported file format. Supported: {dicom_processor.supported_formats}'}), 400
        
        # Secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        
        # Save file
        dicom_path = os.path.join(app.config['DICOM_FOLDER'], unique_filename)
        file.save(dicom_path)
        
        # Validate DICOM file
        if not dicom_processor.is_dicom_file(dicom_path):
            os.remove(dicom_path)
            return jsonify({'error': 'Invalid DICOM file'}), 400
        
        # Extract metadata
        metadata = dicom_processor.extract_metadata(dicom_path)
        
        # Create thumbnail
        thumbnail_filename = f"{timestamp}_{os.path.splitext(filename)[0]}.jpg"
        thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], thumbnail_filename)
        thumbnail_created = dicom_processor.save_thumbnail(dicom_path, thumbnail_path)
        
        # Create PNG version
        png_filename = f"{timestamp}_{os.path.splitext(filename)[0]}.png"
        png_path = os.path.join(app.config['PROCESSED_FOLDER'], png_filename)
        png_created = dicom_processor.convert_to_png(dicom_path, png_path)
        
        response_data = {
            'message': 'DICOM file uploaded successfully',
            'file_info': {
                'original_filename': file.filename,
                'stored_filename': unique_filename,
                'dicom_path': dicom_path,
                'thumbnail_path': thumbnail_path if thumbnail_created else None,
                'png_path': png_path if png_created else None,
                'file_size': metadata['file_info']['file_size'],
                'file_hash': metadata['file_info']['file_hash']
            },
            'metadata': metadata
        }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dicom/files', methods=['GET'])
@require_auth
def list_dicom_files():
    """List all DICOM files"""
    try:
        files = []
        
        for filename in os.listdir(app.config['DICOM_FOLDER']):
            if filename.endswith(('.dcm', '.dicom', '.dic', '.ima')):
                file_path = os.path.join(app.config['DICOM_FOLDER'], filename)
                
                # Get basic file info
                stat = os.stat(file_path)
                
                # Check for thumbnail
                base_name = os.path.splitext(filename)[0]
                thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], f"{base_name}.jpg")
                thumbnail_exists = os.path.exists(thumbnail_path)
                
                file_info = {
                    'filename': filename,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'thumbnail_available': thumbnail_exists
                }
                
                files.append(file_info)
        
        # Sort by creation date (newest first)
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'files': files,
            'total_count': len(files)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dicom/metadata/<filename>', methods=['GET'])
@require_auth
def get_dicom_metadata(filename):
    """Get DICOM metadata"""
    try:
        # Secure filename
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['DICOM_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        metadata = dicom_processor.extract_metadata(file_path)
        
        if 'error' in metadata:
            return jsonify(metadata), 500
        
        return jsonify(metadata)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dicom/thumbnail/<filename>', methods=['GET'])
@require_auth
def get_dicom_thumbnail(filename):
    """Get DICOM thumbnail"""
    try:
        # Secure filename
        filename = secure_filename(filename)
        base_name = os.path.splitext(filename)[0]
        thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], f"{base_name}.jpg")
        
        if not os.path.exists(thumbnail_path):
            # Generate thumbnail if it doesn't exist
            dicom_path = os.path.join(app.config['DICOM_FOLDER'], filename)
            if not os.path.exists(dicom_path):
                return jsonify({'error': 'File not found'}), 404
            
            if not dicom_processor.save_thumbnail(dicom_path, thumbnail_path):
                return jsonify({'error': 'Failed to generate thumbnail'}), 500
        
        return send_file(thumbnail_path, mimetype='image/jpeg')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dicom/image/<filename>', methods=['GET'])
@require_auth
def get_dicom_image(filename):
    """Get processed DICOM image (PNG)"""
    try:
        # Secure filename
        filename = secure_filename(filename)
        base_name = os.path.splitext(filename)[0]
        png_path = os.path.join(app.config['PROCESSED_FOLDER'], f"{base_name}.png")
        
        if not os.path.exists(png_path):
            # Generate PNG if it doesn't exist
            dicom_path = os.path.join(app.config['DICOM_FOLDER'], filename)
            if not os.path.exists(dicom_path):
                return jsonify({'error': 'File not found'}), 404
            
            if not dicom_processor.convert_to_png(dicom_path, png_path):
                return jsonify({'error': 'Failed to process image'}), 500
        
        return send_file(png_path, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dicom/enhance/<filename>', methods=['POST'])
@require_auth
def enhance_dicom_image(filename):
    """Enhance DICOM image"""
    try:
        data = request.get_json()
        enhancement_type = data.get('type', 'contrast')
        
        # Secure filename
        filename = secure_filename(filename)
        dicom_path = os.path.join(app.config['DICOM_FOLDER'], filename)
        
        if not os.path.exists(dicom_path):
            return jsonify({'error': 'File not found'}), 404
        
        enhanced_image = dicom_processor.enhance_image(dicom_path, enhancement_type)
        
        if enhanced_image is None:
            return jsonify({'error': 'Failed to enhance image'}), 500
        
        # Convert enhanced image to base64
        img_buffer = io.BytesIO()
        enhanced_image.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'enhanced_image': f"data:image/png;base64,{img_base64}",
            'enhancement_type': enhancement_type
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dicom/statistics/<filename>', methods=['GET'])
@require_auth
def get_dicom_statistics(filename):
    """Get DICOM image statistics"""
    try:
        # Secure filename
        filename = secure_filename(filename)
        dicom_path = os.path.join(app.config['DICOM_FOLDER'], filename)
        
        if not os.path.exists(dicom_path):
            return jsonify({'error': 'File not found'}), 404
        
        stats = dicom_processor.get_image_statistics(dicom_path)
        
        if stats is None:
            return jsonify({'error': 'Failed to calculate statistics'}), 500
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dicom/delete/<filename>', methods=['DELETE'])
@require_auth
def delete_dicom_file(filename):
    """Delete DICOM file and associated files"""
    try:
        # Secure filename
        filename = secure_filename(filename)
        dicom_path = os.path.join(app.config['DICOM_FOLDER'], filename)
        
        if not os.path.exists(dicom_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Delete main file
        os.remove(dicom_path)
        
        # Delete associated files
        base_name = os.path.splitext(filename)[0]
        
        # Delete thumbnail
        thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], f"{base_name}.jpg")
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        
        # Delete PNG
        png_path = os.path.join(app.config['PROCESSED_FOLDER'], f"{base_name}.png")
        if os.path.exists(png_path):
            os.remove(png_path)
        
        return jsonify({'message': 'DICOM file deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("DICOM Backend Service Starting...")
    print("Features:")
    print("- DICOM file upload and processing")
    print("- Metadata extraction")
    print("- Image rendering and thumbnails")
    print("- Image enhancement")
    print("- File management")
    print("\nInstall required packages:")
    print("pip install flask flask-cors pydicom pillow numpy")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
