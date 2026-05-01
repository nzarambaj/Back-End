"""
NIfTI Neuroimaging Processor
Process MNI Colin27 1998 brain atlas images
"""

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os
from typing import Dict, List, Tuple
from datetime import datetime
import json

class NIfTIProcessor:
    """Process NIfTI neuroimaging files with specialized analysis"""
    
    def __init__(self, nifti_folder: str):
        self.nifti_folder = nifti_folder
        self.supported_formats = ['.nii', '.nii.gz']
        self.processed_files = {}
        self.scan_folder()
        
    def scan_folder(self) -> Dict[str, Dict]:
        """Scan folder for NIfTI files and analyze them"""
        if not os.path.exists(self.nifti_folder):
            return {"error": f"Folder {self.nifti_folder} not found"}
        
        print(f"Scanning NIfTI folder: {self.nifti_folder}")
        
        for file in os.listdir(self.nifti_folder):
            if any(file.lower().endswith(fmt) for fmt in self.supported_formats):
                file_path = os.path.join(self.nifti_folder, file)
                print(f"Processing: {file}")
                
                try:
                    analysis = self.analyze_nifti(file_path)
                    self.processed_files[file] = analysis
                    print(f"  - Shape: {analysis['shape']}")
                    print(f"  - Data type: {analysis['data_type']}")
                    print(f"  - Voxel size: {analysis['voxel_size']}")
                except Exception as e:
                    print(f"  - Error: {str(e)}")
                    self.processed_files[file] = {'error': str(e)}
        
        return self.processed_files
    
    def analyze_nifti(self, file_path: str) -> Dict:
        """Analyze NIfTI file with neuroimaging specific metrics"""
        try:
            # Load NIfTI file
            img = nib.load(file_path)
            data = img.get_fdata()
            header = img.header
            
            # Basic properties
            analysis = {
                'path': file_path,
                'shape': [int(x) for x in data.shape],
                'data_type': str(data.dtype),
                'voxel_size': [float(x) for x in header.get_zooms()],
                'affine': img.affine.tolist(),
                'orientation': list(nib.aff2axcodes(img.affine)),
                'file_size_mb': os.path.getsize(file_path) / (1024 * 1024),
                'intensity_stats': self._calculate_intensity_stats(data),
                'brain_metrics': self._calculate_brain_metrics(data),
                'clinical_info': self._get_clinical_info(file_path)
            }
            
            return analysis
            
        except Exception as e:
            return {'error': f'Failed to analyze NIfTI: {str(e)}'}
    
    def _calculate_intensity_stats(self, data: np.ndarray) -> Dict:
        """Calculate intensity statistics for the image"""
        # Remove zeros (background) for brain tissue analysis
        brain_data = data[data > 0]
        
        if len(brain_data) == 0:
            return {'error': 'No brain tissue detected'}
        
        return {
            'mean_intensity': float(np.mean(brain_data)),
            'std_intensity': float(np.std(brain_data)),
            'min_intensity': float(np.min(brain_data)),
            'max_intensity': float(np.max(brain_data)),
            'median_intensity': float(np.median(brain_data)),
            'brain_voxels': int(len(brain_data)),
            'total_voxels': int(data.size),
            'brain_percentage': float(len(brain_data) / data.size * 100)
        }
    
    def _calculate_brain_metrics(self, data: np.ndarray) -> Dict:
        """Calculate brain-specific metrics"""
        brain_data = data[data > 0]
        
        if len(brain_data) == 0:
            return {'error': 'No brain tissue detected'}
        
        # Estimate brain volume (in mm^3)
        voxel_volume = 1.0  # Will be updated with actual voxel size
        brain_volume_mm3 = len(brain_data) * voxel_volume
        brain_volume_cm3 = brain_volume_mm3 / 1000
        
        return {
            'estimated_volume_mm3': brain_volume_mm3,
            'estimated_volume_cm3': brain_volume_cm3,
            'tissue_coverage': self._estimate_tissue_coverage(data),
            'signal_quality': self._assess_signal_quality(brain_data)
        }
    
    def _estimate_tissue_coverage(self, data: np.ndarray) -> Dict:
        """Estimate different tissue types based on intensity"""
        brain_data = data[data > 0]
        
        if len(brain_data) == 0:
            return {'error': 'No brain tissue detected'}
        
        # Simple tissue classification based on intensity percentiles
        p25 = np.percentile(brain_data, 25)
        p50 = np.percentile(brain_data, 50)
        p75 = np.percentile(brain_data, 75)
        
        csf_like = np.sum(brain_data <= p25)
        gray_matter_like = np.sum((brain_data > p25) & (brain_data <= p75))
        white_matter_like = np.sum(brain_data > p75)
        
        total = len(brain_data)
        
        return {
            'csf_percentage': float(csf_like / total * 100),
            'gray_matter_percentage': float(gray_matter_like / total * 100),
            'white_matter_percentage': float(white_matter_like / total * 100),
            'classification_method': 'intensity_percentile_based'
        }
    
    def _assess_signal_quality(self, brain_data: np.ndarray) -> Dict:
        """Assess signal quality of the brain image"""
        std_intensity = np.std(brain_data)
        
        # Avoid division by zero
        if std_intensity == 0:
            signal_to_noise = np.inf if np.mean(brain_data) > 0 else 0
            contrast_to_noise = 0
        else:
            signal_to_noise = np.mean(brain_data) / std_intensity
            contrast_to_noise = (np.max(brain_data) - np.min(brain_data)) / std_intensity
        
        # Quality assessment
        if signal_to_noise > 10:
            snr_quality = 'Excellent'
        elif signal_to_noise > 5:
            snr_quality = 'Good'
        elif signal_to_noise > 2:
            snr_quality = 'Fair'
        else:
            snr_quality = 'Poor'
        
        return {
            'signal_to_noise_ratio': float(signal_to_noise) if np.isfinite(signal_to_noise) else 0.0,
            'contrast_to_noise_ratio': float(contrast_to_noise) if np.isfinite(contrast_to_noise) else 0.0,
            'quality_assessment': snr_quality,
            'dynamic_range': float(np.max(brain_data) - np.min(brain_data))
        }
    
    def _get_clinical_info(self, file_path: str) -> Dict:
        """Get clinical information based on filename"""
        filename = os.path.basename(file_path).lower()
        
        clinical_info = {
            'dataset_type': 'MNI Colin27 1998 Brain Atlas',
            'subject': 'Colin27',
            'year': '1998',
            'template_type': 'Standardized Brain Template',
            'space': 'Talairach',
            'modality': 'T1-weighted MRI'
        }
        
        if 'mask' in filename:
            clinical_info['file_type'] = 'Brain Mask'
            clinical_info['purpose'] = 'Brain extraction/segmentation'
        elif 'headmask' in filename:
            clinical_info['file_type'] = 'Head Mask'
            clinical_info['purpose'] = 'Head tissue extraction'
        else:
            clinical_info['file_type'] = 'Anatomical Image'
            clinical_info['purpose'] = 'Brain anatomy reference'
        
        return clinical_info
    
    def generate_report(self) -> str:
        """Generate comprehensive analysis report"""
        if not self.processed_files:
            return "No NIfTI files processed. Run scan_folder() first."
        
        report = []
        report.append("MNI COLIN27 1998 NIfTI ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Source Folder: {self.nifti_folder}")
        report.append(f"Total Files: {len(self.processed_files)}")
        report.append("")
        
        for filename, analysis in self.processed_files.items():
            report.append(f"FILE: {filename}")
            report.append("-" * 40)
            
            if 'error' in analysis:
                report.append(f"Error: {analysis['error']}")
            else:
                report.append(f"Shape: {analysis['shape']}")
                report.append(f"Data Type: {analysis['data_type']}")
                voxel_size = [f"{x:.1f}" for x in analysis['voxel_size']]
                report.append(f"Voxel Size: {voxel_size}")
                report.append(f"Orientation: {' '.join(analysis['orientation'])}")
                report.append(f"File Size: {analysis['file_size_mb']:.1f} MB")
                
                # Intensity statistics
                if 'intensity_stats' in analysis:
                    stats = analysis['intensity_stats']
                    if 'error' not in stats:
                        report.append(f"Brain Voxels: {stats['brain_voxels']:,}")
                        report.append(f"Brain Coverage: {stats['brain_percentage']:.1f}%")
                        report.append(f"Mean Intensity: {stats['mean_intensity']:.1f}")
                        snr = stats['mean_intensity']/stats['std_intensity'] if stats['std_intensity'] > 0 else 0
                        report.append(f"SNR: {snr:.1f}")
                
                # Clinical information
                if 'clinical_info' in analysis:
                    clinical = analysis['clinical_info']
                    report.append(f"Dataset: {clinical['dataset_type']}")
                    report.append(f"File Type: {clinical['file_type']}")
                    report.append(f"Purpose: {clinical['purpose']}")
            
            report.append("")
        
        return "\n".join(report)
    
    def get_api_response(self) -> Dict:
        """Get API format response for web integration"""
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'source_folder': self.nifti_folder,
            'total_files': len(self.processed_files),
            'files': self.processed_files,
            'summary': self._generate_summary()
        }
    
    def _generate_summary(self) -> Dict:
        """Generate summary statistics"""
        if not self.processed_files:
            return {}
        
        summary = {
            'dataset_info': 'MNI Colin27 1998 Brain Atlas',
            'total_files': len(self.processed_files),
            'total_size_mb': sum(f.get('file_size_mb', 0) for f in self.processed_files.values() if 'error' not in f),
            'file_types': {},
            'voxel_sizes': [],
            'orientations': []
        }
        
        for filename, analysis in self.processed_files.items():
            if 'error' not in analysis:
                # File types
                file_type = analysis.get('clinical_info', {}).get('file_type', 'Unknown')
                summary['file_types'][file_type] = summary['file_types'].get(file_type, 0) + 1
                
                # Voxel sizes
                if 'voxel_size' in analysis:
                    summary['voxel_sizes'].append(analysis['voxel_size'])
                
                # Orientations
                if 'orientation' in analysis:
                    summary['orientations'].append(' '.join(analysis['orientation']))
        
        return summary

# Example usage
if __name__ == "__main__":
    print("NIfTI Neuroimaging Processor")
    print("=" * 50)
    
    # Process MNI Colin27 dataset
    processor = NIfTIProcessor("C:/Users/TTR/Documents/Calculus/mni_colin27_1998_nifti")
    
    print("\nANALYSIS REPORT:")
    print("=" * 50)
    print(processor.generate_report())
    
    print("\nAPI RESPONSE:")
    print("=" * 50)
    print(json.dumps(processor.get_api_response(), indent=2))
