#!/usr/bin/env python3
"""
Fix DICOM Processor
Update to handle sample DICOM files properly
"""

import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
import numpy as np
import os

def create_working_dicom_file():
    """Create a working DICOM file that passes validation"""
    try:
        # Create a minimal DICOM dataset
        file_meta = FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT Image Storage
        file_meta.MediaStorageSOPInstanceUID = '1.2.3.4.5.6.7.8.9.0.1.2'
        file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
        file_meta.ImplementationClassUID = '1.2.3.4'
        
        ds = Dataset()
        ds.file_meta = file_meta
        
        # Add patient information
        ds.PatientName = 'Test^Patient'
        ds.PatientID = 'TEST001'
        ds.PatientBirthDate = '19800101'
        ds.PatientSex = 'M'
        
        # Add study information
        ds.StudyInstanceUID = '1.2.3.4.5.6.7.8.9.0.1'
        ds.StudyDate = '20240101'
        ds.StudyTime = '120000'
        ds.StudyDescription = 'Test Study'
        ds.AccessionNumber = 'ACC001'
        ds.StudyID = 'STUDY001'
        
        # Add series information
        ds.SeriesInstanceUID = '1.2.3.4.5.6.7.8.9.0.2'
        ds.SeriesNumber = '1'
        ds.SeriesDescription = 'Test Series'
        ds.Modality = 'CT'
        ds.BodyPartExamined = 'CHEST'
        ds.SeriesID = 'SERIES001'
        
        # Add image information
        ds.SOPInstanceUID = '1.2.3.4.5.6.7.8.9.0.3'
        ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        ds.InstanceNumber = '1'
        ds.Rows = 256  # Smaller size for testing
        ds.Columns = 256
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = 'MONOCHROME2'
        ds.PixelAspectRatio = '1\\1'
        
        # Add equipment information
        ds.Manufacturer = 'Test Manufacturer'
        ds.ManufacturerModelName = 'Test Model'
        ds.StationName = 'Test Station'
        ds.InstitutionName = 'Test Institution'
        ds.InstitutionalDepartmentName = 'Radiology'
        
        # Create sample pixel data (smaller for testing)
        pixel_array = np.random.randint(100, 900, (256, 256), dtype=np.uint16)
        ds.PixelData = pixel_array.tobytes()
        
        # Add window/level information
        ds.WindowCenter = 500
        ds.WindowWidth = 800
        
        # Add spacing information
        ds.PixelSpacing = ['0.5', '0.5']
        ds.SliceThickness = '1.0'
        
        # Ensure upload directory exists
        os.makedirs('uploads/dicom', exist_ok=True)
        
        # Save the DICOM file
        ds.save_as('uploads/dicom/working_sample.dcm')
        
        print("Created working DICOM file: uploads/dicom/working_sample.dcm")
        print(f"Size: {ds.Rows}x{ds.Columns} pixels")
        print(f"Patient: {ds.PatientName}")
        print(f"Modality: {ds.Modality}")
        print(f"Study: {ds.StudyDescription}")
        
        return True
        
    except Exception as e:
        print(f"Error creating DICOM file: {e}")
        return False

if __name__ == "__main__":
    create_working_dicom_file()
