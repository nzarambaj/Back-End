"""
DICOM image loading and metadata extraction utilities
"""

import pydicom
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Optional, Union

def load_dicom_image(file_path: Union[str, Path]) -> Tuple[np.ndarray, Dict]:
    """
    Load a DICOM file and return image array with metadata
    
    Args:
        file_path: Path to DICOM file
        
    Returns:
        Tuple of (image_array, metadata_dict)
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not valid DICOM
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"DICOM file not found: {file_path}")
    
    try:
        # Read DICOM file
        ds = pydicom.dcmread(file_path)
        
        # Extract pixel array
        if not hasattr(ds, 'pixel_array'):
            raise ValueError("DICOM file has no pixel data")
        
        pixel_array = ds.pixel_array
        
        # Apply rescale slope/intercept if present
        slope = float(getattr(ds, 'RescaleSlope', 1))
        intercept = float(getattr(ds, 'RescaleIntercept', 0))
        
        if slope != 1 or intercept != 0:
            pixel_array = pixel_array * slope + intercept
        
        # Extract metadata
        metadata = extract_metadata(ds)
        
        return pixel_array, metadata
        
    except Exception as e:
        raise ValueError(f"Error reading DICOM file: {e}")

def extract_metadata(ds: pydicom.Dataset) -> Dict:
    """
    Extract relevant metadata from DICOM dataset
    
    Args:
        ds: PyDICOM dataset
        
    Returns:
        Dictionary of metadata
    """
    metadata = {}
    
    # Patient information
    metadata['patient'] = {
        'id': getattr(ds, 'PatientID', ''),
        'name': getattr(ds, 'PatientName', ''),
        'birth_date': getattr(ds, 'PatientBirthDate', ''),
        'sex': getattr(ds, 'PatientSex', '')
    }
    
    # Study information
    metadata['study'] = {
        'uid': getattr(ds, 'StudyInstanceUID', ''),
        'date': getattr(ds, 'StudyDate', ''),
        'time': getattr(ds, 'StudyTime', ''),
        'description': getattr(ds, 'StudyDescription', '')
    }
    
    # Series information
    metadata['series'] = {
        'uid': getattr(ds, 'SeriesInstanceUID', ''),
        'number': getattr(ds, 'SeriesNumber', ''),
        'modality': getattr(ds, 'Modality', ''),
        'description': getattr(ds, 'SeriesDescription', '')
    }
    
    # Image information
    metadata['image'] = {
        'rows': getattr(ds, 'Rows', 0),
        'columns': getattr(ds, 'Columns', 0),
        'bits_allocated': getattr(ds, 'BitsAllocated', 0),
        'bits_stored': getattr(ds, 'BitsStored', 0),
        'high_bit': getattr(ds, 'HighBit', 0),
        'pixel_representation': getattr(ds, 'PixelRepresentation', 0),
        'samples_per_pixel': getattr(ds, 'SamplesPerPixel', 1),
        'photometric_interpretation': getattr(ds, 'PhotometricInterpretation', '')
    }
    
    # Window/Level information
    metadata['window_level'] = {
        'center': getattr(ds, 'WindowCenter', None),
        'width': getattr(ds, 'WindowWidth', None)
    }
    
    # Position and orientation
    metadata['position'] = {
        'image_position': getattr(ds, 'ImagePositionPatient', None),
        'image_orientation': getattr(ds, 'ImageOrientationPatient', None),
        'slice_thickness': getattr(ds, 'SliceThickness', None),
        'spacing': getattr(ds, 'PixelSpacing', None)
    }
    
    return metadata

def get_dicom_info(file_path: Union[str, Path]) -> Dict:
    """
    Get basic DICOM file information without loading pixel data
    
    Args:
        file_path: Path to DICOM file
        
    Returns:
        Dictionary with file information
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"DICOM file not found: {file_path}")
    
    try:
        ds = pydicom.dcmread(file_path, stop_before_pixels=True)
        
        info = {
            'file_path': str(file_path),
            'file_size': file_path.stat().st_size,
            'transfer_syntax': getattr(ds, 'TransferSyntaxUID', ''),
            'media_storage_sop_class': getattr(ds, 'MediaStorageSOPClassUID', ''),
            'media_storage_sop_instance': getattr(ds, 'MediaStorageSOPInstanceUID', ''),
            'implementation_class': getattr(ds, 'ImplementationClassUID', ''),
            'sop_class': getattr(ds, 'SOPClassUID', ''),
            'sop_instance': getattr(ds, 'SOPInstanceUID', '')
        }
        
        return info
        
    except Exception as e:
        raise ValueError(f"Error reading DICOM info: {e}")

def validate_dicom_file(file_path: Union[str, Path]) -> bool:
    """
    Validate if a file is a proper DICOM file
    
    Args:
        file_path: Path to file
        
    Returns:
        True if valid DICOM, False otherwise
    """
    try:
        pydicom.dcmread(file_path, stop_before_pixels=True)
        return True
    except:
        return False
