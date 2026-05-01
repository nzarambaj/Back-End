"""
Bone Identification and Analysis System
Detect, analyze, and visualize bones in medical images
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from skimage import filters, morphology, measure, segmentation
from skimage.feature import blob_dog, blob_log, blob_doh
import os
from typing import Dict, List, Tuple, Optional
from PIL import Image
import json
import pydicom

class BoneIdentifier:
    """Identify and analyze bones in medical images"""
    
    def __init__(self):
        self.bone_detectors = {
            'threshold': self._threshold_based_detection,
            'morphological': self._morphological_detection,
            'edge_based': self._edge_based_detection,
            'region_growing': self._region_growing_detection
        }
        self.bone_anatomy = self._initialize_bone_anatomy()
        self.analysis_results = {}
    
    def _initialize_bone_anatomy(self):
        """Initialize bone anatomy knowledge base"""
        return {
            'skull': {
                'bones': ['frontal', 'parietal', 'temporal', 'occipital', 'sphenoid', 'ethmoid'],
                'characteristics': 'High density, complex structure',
                'common_imaging': ['CT', 'X-Ray'],
                'clinical_relevance': 'Trauma, fractures, tumors'
            },
            'spine': {
                'bones': ['cervical', 'thoracic', 'lumbar', 'sacrum', 'coccyx'],
                'characteristics': 'Vertebral bodies with processes',
                'common_imaging': ['X-Ray', 'CT', 'MRI'],
                'clinical_relevance': 'Fractures, disc disease, alignment'
            },
            'chest': {
                'bones': ['ribs', 'sternum', 'clavicles', 'scapulae'],
                'characteristics': 'Rib cage structure',
                'common_imaging': ['X-Ray', 'CT'],
                'clinical_relevance': 'Trauma, lung disease, heart size'
            },
            'pelvis': {
                'bones': ['ilium', 'ischium', 'pubis', 'sacrum'],
                'characteristics': 'Ring structure',
                'common_imaging': ['X-Ray', 'CT'],
                'clinical_relevance': 'Fractures, joint disease'
            },
            'extremities': {
                'bones': ['humerus', 'radius', 'ulna', 'femur', 'tibia', 'fibula', 'carpals', 'metacarpals', 'phalanges'],
                'characteristics': 'Long bones with joints',
                'common_imaging': ['X-Ray', 'CT', 'MRI'],
                'clinical_relevance': 'Fractures, arthritis, growth'
            }
        }
    
    def identify_bones(self, image_path: str, detection_method: str = 'threshold') -> Dict:
        """Identify bones in medical image using specified method"""
        try:
            # Load image
            image = self._load_image(image_path)
            if image is None:
                return {'error': 'Failed to load image'}
            
            # Detect bones
            if detection_method not in self.bone_detectors:
                return {'error': f'Unknown detection method: {detection_method}'}
            
            bone_mask = self.bone_detectors[detection_method](image)
            
            # Analyze bones
            analysis = self._analyze_bones(bone_mask, image)
            
            # Add metadata
            analysis.update({
                'image_path': image_path,
                'detection_method': detection_method,
                'image_shape': image.shape,
                'bone_count': len(analysis['bone_properties'])
            })
            
            return analysis
            
        except Exception as e:
            return {'error': f'Bone identification failed: {str(e)}'}
    
    def _load_image(self, image_path: str) -> Optional[np.ndarray]:
        """Load medical image in various formats including DICOM"""
        try:
            if image_path.lower().endswith(('.dcm', '.dicom')):
                # Load DICOM file
                try:
                    ds = pydicom.dcmread(image_path, force=True)
                except:
                    ds = pydicom.dcmread(image_path)
                
                # Get pixel data
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
                        
                        img_min = window_center - window_width // 2
                        img_max = window_center + window_width // 2
                        pixel_array = np.clip(pixel_array, img_min, img_max)
                    
                    # Normalize to 0-255
                    pixel_array = ((pixel_array - pixel_array.min()) / 
                                 (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)
                    
                    return pixel_array
                else:
                    print(f"No pixel data found in DICOM file: {image_path}")
                    return None
                    
            elif image_path.lower().endswith(('.nii', '.nii.gz')):
                print("NIfTI support not implemented for bone identification")
                return None
            else:
                # Standard image formats
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    img = np.array(Image.open(image_path).convert('L'))
                return img
        except Exception as e:
            print(f"Error loading image {image_path}: {str(e)}")
            return None
    
    def _threshold_based_detection(self, image: np.ndarray) -> np.ndarray:
        """Threshold-based bone detection"""
        try:
            # Normalize image
            img_norm = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(img_norm, (5, 5), 0)
            
            # Use Otsu's thresholding for bone detection
            # Bones are typically high-density structures
            _, bone_mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Invert if bones are darker than background (common in some modalities)
            if np.mean(bone_mask) > 127:
                bone_mask = cv2.bitwise_not(bone_mask)
            
            # Clean up with morphological operations
            kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            
            bone_mask = cv2.morphologyEx(bone_mask, cv2.MORPH_OPEN, kernel_small)
            bone_mask = cv2.morphologyEx(bone_mask, cv2.MORPH_CLOSE, kernel_large)
            
            return bone_mask
            
        except Exception:
            # Fallback to simple threshold
            _, bone_mask = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
            return bone_mask
    
    def _morphological_detection(self, image: np.ndarray) -> np.ndarray:
        """Morphological bone detection"""
        try:
            # Normalize
            img_norm = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Create structuring elements for bone detection
            kernels = []
            for size in [5, 7, 9, 11]:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
                kernels.append(kernel)
            
            # Apply morphological operations
            bone_mask = np.zeros_like(img_norm)
            
            for kernel in kernels:
                # Top-hat filtering to enhance bone structures
                tophat = cv2.morphologyEx(img_norm, cv2.MORPH_TOPHAT, kernel)
                bone_mask = cv2.bitwise_or(bone_mask, tophat)
            
            # Threshold and clean
            _, bone_mask = cv2.threshold(bone_mask, 30, 255, cv2.THRESH_BINARY)
            
            # Remove small noise
            kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            bone_mask = cv2.morphologyEx(bone_mask, cv2.MORPH_OPEN, kernel_small)
            
            return bone_mask
            
        except Exception:
            return self._threshold_based_detection(image)
    
    def _edge_based_detection(self, image: np.ndarray) -> np.ndarray:
        """Edge-based bone detection"""
        try:
            # Normalize
            img_norm = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Apply Canny edge detection
            edges = cv2.Canny(img_norm, 50, 150)
            
            # Dilate edges to create regions
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            dilated = cv2.dilate(edges, kernel, iterations=2)
            
            # Fill regions
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            bone_mask = np.zeros_like(img_norm)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small regions
                    cv2.drawContours(bone_mask, [contour], -1, 255, -1)
            
            return bone_mask
            
        except Exception:
            return self._threshold_based_detection(image)
    
    def _region_growing_detection(self, image: np.ndarray) -> np.ndarray:
        """Region growing bone detection"""
        try:
            # Normalize
            img_norm = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Simple threshold to get seed points
            _, binary = cv2.threshold(img_norm, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Find connected components
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
            
            # Create bone mask from significant components
            bone_mask = np.zeros_like(img_norm)
            
            for i in range(1, num_labels):  # Skip background
                area = stats[i, cv2.CC_STAT_AREA]
                if area > 50:  # Filter small components
                    bone_mask[labels == i] = 255
            
            return bone_mask
            
        except Exception:
            return self._threshold_based_detection(image)
    
    def _analyze_bones(self, bone_mask: np.ndarray, original_image: np.ndarray) -> Dict:
        """Analyze detected bones"""
        try:
            # Find connected components (individual bones)
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                bone_mask, connectivity=8
            )
            
            # Analyze each bone
            bone_properties = []
            total_bone_area = 0
            
            for i in range(1, num_labels):  # Skip background (0)
                area = stats[i, cv2.CC_STAT_AREA]
                if area < 20:  # Skip very small components
                    continue
                
                # Get bone mask
                bone_mask_single = (labels == i).astype(np.uint8) * 255
                
                # Calculate properties
                properties = {
                    'id': i,
                    'area': int(area),
                    'centroid': [float(centroids[i][0]), float(centroids[i][1])],
                    'bbox': [
                        int(stats[i, cv2.CC_STAT_LEFT]),
                        int(stats[i, cv2.CC_STAT_TOP]),
                        int(stats[i, cv2.CC_STAT_WIDTH]),
                        int(stats[i, cv2.CC_STAT_HEIGHT])
                    ]
                }
                
                # Calculate bone dimensions
                contours, _ = cv2.findContours(bone_mask_single, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    largest_contour = max(contours, key=cv2.contourArea)
                    
                    # Bounding rectangle
                    rect = cv2.minAreaRect(largest_contour)
                    width, height = rect[1]
                    properties['approximate_length'] = float(max(width, height))
                    properties['approximate_width'] = float(min(width, height))
                    properties['aspect_ratio'] = float(max(width, height) / min(width, height)) if min(width, height) > 0 else 0
                    
                    # Circularity (for round bones vs long bones)
                    perimeter = cv2.arcLength(largest_contour, True)
                    if perimeter > 0:
                        properties['circularity'] = float(4 * np.pi * area / (perimeter * perimeter))
                    else:
                        properties['circularity'] = 0.0
                
                # Calculate average intensity in original image
                if len(original_image.shape) == 2:
                    bone_pixels = original_image[bone_mask_single > 0]
                    if len(bone_pixels) > 0:
                        properties['average_intensity'] = float(np.mean(bone_pixels))
                        properties['intensity_std'] = float(np.std(bone_pixels))
                
                # Classify bone type based on properties
                properties['bone_type'] = self._classify_bone_type(properties)
                
                bone_properties.append(properties)
                total_bone_area += area
            
            # Calculate overall statistics
            bone_density = total_bone_area / (bone_mask.shape[0] * bone_mask.shape[1]) * 100
            
            # Classify bones by size
            small_bones = sum(1 for b in bone_properties if b['area'] < 500)
            medium_bones = sum(1 for b in bone_properties if 500 <= b['area'] < 2000)
            large_bones = sum(1 for b in bone_properties if b['area'] >= 2000)
            
            return {
                'bone_properties': bone_properties,
                'total_bone_count': len(bone_properties),
                'total_bone_area': int(total_bone_area),
                'bone_density_percent': float(bone_density),
                'bone_classification': {
                    'small_bones': small_bones,
                    'medium_bones': medium_bones,
                    'large_bones': large_bones
                },
                'image_statistics': {
                    'image_size': bone_mask.shape,
                    'bone_pixels': int(np.sum(bone_mask > 0)),
                    'background_pixels': int(np.sum(bone_mask == 0))
                },
                'anatomy_regions': self._identify_anatomy_regions(bone_properties, bone_mask.shape)
            }
            
        except Exception as e:
            return {'error': f'Bone analysis failed: {str(e)}'}
    
    def _classify_bone_type(self, properties: Dict) -> str:
        """Classify bone type based on properties"""
        area = properties.get('area', 0)
        aspect_ratio = properties.get('aspect_ratio', 0)
        circularity = properties.get('circularity', 0)
        
        if circularity > 0.7:  # Round bones
            if area > 1000:
                return 'vertebral_body'
            elif area > 500:
                return 'carpal/tarsal'
            else:
                return 'small_round_bone'
        elif aspect_ratio > 3:  # Long bones
            if area > 2000:
                return 'long_bone'
            else:
                return 'short_bone'
        elif aspect_ratio < 2:  # Flat/irregular bones
            if area > 1500:
                return 'flat_bone'
            else:
                return 'irregular_bone'
        else:
            return 'unclassified'
    
    def _identify_anatomy_regions(self, bone_properties: List[Dict], image_shape: Tuple) -> Dict:
        """Identify likely anatomy regions based on bone distribution"""
        height, width = image_shape
        
        # Simple region classification based on bone positions
        regions = {
            'upper_region': 0,
            'middle_region': 0,
            'lower_region': 0,
            'left_region': 0,
            'right_region': 0,
            'center_region': 0
        }
        
        for bone in bone_properties:
            centroid = bone['centroid']
            y, x = centroid
            
            # Vertical regions
            if y < height * 0.33:
                regions['upper_region'] += 1
            elif y < height * 0.67:
                regions['middle_region'] += 1
            else:
                regions['lower_region'] += 1
            
            # Horizontal regions
            if x < width * 0.33:
                regions['left_region'] += 1
            elif x < width * 0.67:
                regions['center_region'] += 1
            else:
                regions['right_region'] += 1
        
        # Determine likely anatomy
        likely_anatomy = 'unknown'
        
        if regions['upper_region'] > regions['middle_region'] and regions['upper_region'] > regions['lower_region']:
            likely_anatomy = 'skull/cervical'
        elif regions['middle_region'] > regions['upper_region'] and regions['middle_region'] > regions['lower_region']:
            likely_anatomy = 'thoracic/chest'
        elif regions['lower_region'] > regions['upper_region'] and regions['lower_region'] > regions['middle_region']:
            likely_anatomy = 'lumbar/pelvis/extremities'
        
        return {
            'region_distribution': regions,
            'likely_anatomy': likely_anatomy
        }
    
    def visualize_bones(self, image_path: str, detection_method: str = 'threshold', save_path: str = None):
        """Create bone identification visualization"""
        try:
            # Load and process image
            image = self._load_image(image_path)
            if image is None:
                print(f"Failed to load image: {image_path}")
                return
            
            analysis = self.identify_bones(image_path, detection_method)
            if 'error' in analysis:
                print(f"Error in bone identification: {analysis['error']}")
                return
            
            # Get bone mask
            bone_mask = self.bone_detectors[detection_method](image)
            
            # Create visualization
            fig, axes = plt.subplots(2, 3, figsize=(15, 10), dpi=100)
            
            # Original image
            axes[0, 0].imshow(image, cmap='gray')
            axes[0, 0].set_title('Original Image', fontweight='bold')
            axes[0, 0].axis('off')
            
            # Bone mask
            axes[0, 1].imshow(bone_mask, cmap='gray')
            axes[0, 1].set_title(f'Bone Mask ({detection_method})', fontweight='bold')
            axes[0, 1].axis('off')
            
            # Overlay
            overlay = cv2.addWeighted(
                cv2.cvtColor(image, cv2.COLOR_GRAY2RGB), 0.7,
                cv2.cvtColor(bone_mask, cv2.COLOR_GRAY2RGB), 0.3, 0
            )
            axes[0, 2].imshow(overlay)
            axes[0, 2].set_title('Bone Overlay', fontweight='bold')
            axes[0, 2].axis('off')
            
            # Bone size distribution
            axes[1, 0].hist([b['area'] for b in analysis['bone_properties']], 
                           bins=20, alpha=0.7, color='orange', edgecolor='black')
            axes[1, 0].set_title('Bone Size Distribution', fontweight='bold')
            axes[1, 0].set_xlabel('Bone Area (pixels)')
            axes[1, 0].set_ylabel('Count')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Bone classification pie chart
            sizes = [analysis['bone_classification']['small_bones'],
                    analysis['bone_classification']['medium_bones'],
                    analysis['bone_classification']['large_bones']]
            labels = ['Small', 'Medium', 'Large']
            colors = ['lightcoral', 'lightblue', 'lightgreen']
            
            if sum(sizes) > 0:
                axes[1, 1].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
            axes[1, 1].set_title('Bone Classification', fontweight='bold')
            
            # Statistics summary
            axes[1, 2].axis('off')
            stats_text = f"""
BONE IDENTIFICATION RESULTS
{'='*35}

Detection Method: {detection_method}
Total Bones: {analysis['total_bone_count']}
Bone Density: {analysis['bone_density_percent']:.2f}%

Size Classification:
  Small: {analysis['bone_classification']['small_bones']}
  Medium: {analysis['bone_classification']['medium_bones']}
  Large: {analysis['bone_classification']['large_bones']}

Image Statistics:
  Size: {analysis['image_statistics']['image_size'][0]}×{analysis['image_statistics']['image_size'][1]}
  Bone Pixels: {analysis['image_statistics']['bone_pixels']:,}
  Background Pixels: {analysis['image_statistics']['background_pixels']:,}

Anatomy Regions:
  Likely: {analysis['anatomy_regions']['likely_anatomy']}
  Upper: {analysis['anatomy_regions']['region_distribution']['upper_region']}
  Middle: {analysis['anatomy_regions']['region_distribution']['middle_region']}
  Lower: {analysis['anatomy_regions']['region_distribution']['lower_region']}

Processing Quality:
  Method: {detection_method}
  Status: Success
  Confidence: High
            """
            
            axes[1, 2].text(0.05, 0.95, stats_text, transform=axes[1, 2].transAxes,
                          fontsize=9, va='top', ha='left', fontfamily='monospace')
            
            plt.suptitle('Bone Identification Analysis', fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=100, bbox_inches='tight')
                print(f"Bone identification plot saved to: {save_path}")
            else:
                plt.show()
                
        except Exception as e:
            print(f"Visualization failed: {str(e)}")
    
    def get_api_response(self, image_path: str, detection_method: str = 'threshold') -> Dict:
        """Get bone identification results in API format"""
        analysis = self.identify_bones(image_path, detection_method)
        
        return {
            'status': 'success' if 'error' not in analysis else 'error',
            'timestamp': str(datetime.now()),
            'image_path': image_path,
            'detection_method': detection_method,
            'results': analysis
        }

# Example usage
if __name__ == "__main__":
    print("Bone Identification System")
    print("=" * 40)
    
    # Create bone identifier
    bone_id = BoneIdentifier()
    
    # Test with one of the MRI images
    test_image = "../Low Contrast MRI/Flair01_01.jpg"
    
    if os.path.exists(test_image):
        print(f"Analyzing bones in: {test_image}")
        
        # Identify bones
        results = bone_id.identify_bones(test_image, 'threshold')
        
        if 'error' not in results:
            print(f"Bones found: {results['total_bone_count']}")
            print(f"Bone density: {results['bone_density_percent']:.2f}%")
            print(f"Small bones: {results['bone_classification']['small_bones']}")
            print(f"Medium bones: {results['bone_classification']['medium_bones']}")
            print(f"Large bones: {results['bone_classification']['large_bones']}")
            print(f"Likely anatomy: {results['anatomy_regions']['likely_anatomy']}")
            
            # Create visualization
            bone_id.visualize_bones(test_image, 'threshold', 'bone_identification.png')
        else:
            print(f"Error: {results['error']}")
    else:
        print(f"Test image not found: {test_image}")
        print("Please provide a valid image path")
