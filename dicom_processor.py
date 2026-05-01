#!/usr/bin/env python3
"""
DICOM Processor
Python backend for DICOM file processing
Handles metadata extraction, image rendering, and enhancement
"""

import sys
import json
import os
import hashlib
import base64
import io
from pathlib import Path
import pydicom
from pydicom import dcmread
from PIL import Image, ImageEnhance
import numpy as np

class DICOMProcessor:
    def __init__(self):
        self.supported_formats = ['.dcm', '.dicom', '.dic', '.ima']
        self.thumbnail_size = (200, 200)
        
    def is_dicom_file(self, file_path):
        """Check if file is a valid DICOM file"""
        try:
            ds = pydicom.dcmread(file_path)
            return True
        except:
            return False
    
    def extract_metadata(self, file_path, options=None):
        """Extract comprehensive DICOM metadata"""
        try:
            if not self.is_dicom_file(file_path):
                return {'error': 'Invalid DICOM file'}
            
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
            
            return {'success': True, 'metadata': metadata}
            
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
    
    def generate_thumbnail(self, file_path, options=None):
        """Generate thumbnail from DICOM image"""
        try:
            pixel_array = self.get_pixel_array(file_path)
            
            if pixel_array is None:
                return {'error': 'No pixel data found'}
            
            # Convert to PIL Image
            if len(pixel_array.shape) == 2:
                # Grayscale image
                image = Image.fromarray(pixel_array, mode='L')
            elif len(pixel_array.shape) == 3:
                # RGB image
                image = Image.fromarray(pixel_array, mode='RGB')
            else:
                return {'error': 'Unsupported image format'}
            
            # Resize to thumbnail size
            image.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
            
            # Convert to RGB if grayscale
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save thumbnail
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            thumbnail_path = f'uploads/thumbnails/{base_name}.jpg'
            
            # Ensure thumbnail directory exists
            os.makedirs('uploads/thumbnails', exist_ok=True)
            
            image.save(thumbnail_path, 'JPEG', quality=85)
            
            return {'success': True, 'thumbnail_path': thumbnail_path}
            
        except Exception as e:
            return {'error': f'Failed to generate thumbnail: {str(e)}'}
    
    def generate_image(self, file_path, options=None):
        """Generate processed PNG image from DICOM"""
        try:
            pixel_array = self.get_pixel_array(file_path)
            
            if pixel_array is None:
                return {'error': 'No pixel data found'}
            
            # Convert to PIL Image
            if len(pixel_array.shape) == 2:
                # Grayscale image
                image = Image.fromarray(pixel_array, mode='L')
            elif len(pixel_array.shape) == 3:
                # RGB image
                image = Image.fromarray(pixel_array, mode='RGB')
            else:
                return {'error': 'Unsupported image format'}
            
            # Save as PNG
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            image_path = f'uploads/processed/{base_name}.png'
            
            # Ensure processed directory exists
            os.makedirs('uploads/processed', exist_ok=True)
            
            image.save(image_path, 'PNG')
            
            return {'success': True, 'image_path': image_path}
            
        except Exception as e:
            return {'error': f'Failed to generate image: {str(e)}'}
    
    def enhance_image(self, file_path, options=None):
        """Enhance DICOM image"""
        try:
            enhancement_type = options.get('enhancement', 'contrast') if options else 'contrast'
            
            pixel_array = self.get_pixel_array(file_path)
            
            if pixel_array is None:
                return {'error': 'No pixel data found'}
            
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
            
            # Convert to base64
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            return {'success': True, 'enhanced_image': f"data:image/png;base64,{img_base64}"}
            
        except Exception as e:
            return {'error': f'Failed to enhance image: {str(e)}'}
    
    def get_statistics(self, file_path, options=None):
        """Calculate image statistics"""
        try:
            pixel_array = self.get_pixel_array(file_path)
            
            if pixel_array is None:
                return {'error': 'No pixel data found'}
            
            stats = {
                'min_value': float(np.min(pixel_array)),
                'max_value': float(np.max(pixel_array)),
                'mean_value': float(np.mean(pixel_array)),
                'std_value': float(np.std(pixel_array)),
                'shape': list(pixel_array.shape),
                'dtype': str(pixel_array.dtype)
            }
            
            return {'success': True, 'statistics': stats}
            
        except Exception as e:
            return {'error': f'Failed to calculate statistics: {str(e)}'}

def main():
    if len(sys.argv) < 3:
        print(json.dumps({'error': 'Insufficient arguments'}))
        return
    
    action = sys.argv[1]
    file_path = sys.argv[2]
    options = {}
    
    if len(sys.argv) > 3:
        try:
            options = json.loads(sys.argv[3])
        except:
            options = {}
    
    processor = DICOMProcessor()
    
    if action == 'extract_metadata':
        result = processor.extract_metadata(file_path, options)
    elif action == 'generate_thumbnail':
        result = processor.generate_thumbnail(file_path, options)
    elif action == 'generate_image':
        result = processor.generate_image(file_path, options)
    elif action == 'enhance_image':
        result = processor.enhance_image(file_path, options)
    elif action == 'get_statistics':
        result = processor.get_statistics(file_path, options)
    else:
        result = {'error': f'Unknown action: {action}'}
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()
