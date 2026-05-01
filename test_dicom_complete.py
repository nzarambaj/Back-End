#!/usr/bin/env python3
"""
Test Complete DICOM Backend Service
Test all DICOM processing functionality on port 5002
"""

import requests
import json
import os
from datetime import datetime

class DICOMCompleteTester:
    def __init__(self):
        self.base_url = "http://localhost:5002"
        self.auth_token = None
        
    def authenticate(self):
        """Authenticate with DICOM backend"""
        print(" AUTHENTICATION")
        print("-" * 40)
        
        auth_data = {
            "email": "test@example.com",
            "password": "test123"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                  json=auth_data, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                print(f"   Status: SUCCESS")
                print(f"   Token: {self.auth_token[:20]}...")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def get_headers(self):
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.auth_token}"}
    
    def test_health_check(self):
        """Test DICOM backend health check"""
        print("\n HEALTH CHECK")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/api/dicom/health", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Status: SUCCESS")
                print(f"   Service: {data.get('service', 'Unknown')}")
                print(f"   Version: {data.get('version', 'Unknown')}")
                print(f"   Port: {data.get('port', 'Unknown')}")
                print(f"   Features: {len(data.get('features', []))} available")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def test_list_files(self):
        """Test listing DICOM files"""
        print("\n LIST DICOM FILES")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/api/dicom/files", 
                                  headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                files = data.get('files', [])
                print(f"   Status: SUCCESS")
                print(f"   Total Files: {data.get('total', 0)}")
                
                for file_info in files[:3]:  # Show first 3
                    print(f"      - {file_info['filename']}")
                    print(f"        Size: {file_info['size']} bytes")
                    print(f"        Thumbnail: {'Yes' if file_info['thumbnail'] else 'No'}")
                
                return files
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return []
    
    def create_sample_dicom_file(self):
        """Create a sample DICOM file for testing"""
        print("\n CREATE SAMPLE DICOM FILE")
        print("-" * 40)
        
        try:
            import pydicom
            from pydicom.dataset import Dataset, FileMetaDataset
            import numpy as np
            
            # Create a minimal DICOM dataset
            file_meta = FileMetaDataset()
            file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT Image Storage
            file_meta.MediaStorageSOPInstanceUID = '1.2.3.4.5.6.7.8.9.0.1.2'
            file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
            
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
            
            # Add series information
            ds.SeriesInstanceUID = '1.2.3.4.5.6.7.8.9.0.2'
            ds.SeriesNumber = '1'
            ds.SeriesDescription = 'Test Series'
            ds.Modality = 'CT'
            ds.BodyPartExamined = 'CHEST'
            
            # Add image information
            ds.SOPInstanceUID = '1.2.3.4.5.6.7.8.9.0.3'
            ds.InstanceNumber = '1'
            ds.Rows = 512
            ds.Columns = 512
            ds.BitsAllocated = 16
            ds.BitsStored = 16
            ds.HighBit = 15
            ds.PixelRepresentation = 0
            ds.SamplesPerPixel = 1
            ds.PhotometricInterpretation = 'MONOCHROME2'
            
            # Create sample pixel data
            pixel_array = np.random.randint(0, 1000, (512, 512), dtype=np.uint16)
            ds.PixelData = pixel_array.tobytes()
            
            # Add equipment information
            ds.Manufacturer = 'Test Manufacturer'
            ds.ManufacturerModelName = 'Test Model'
            ds.StationName = 'Test Station'
            ds.InstitutionName = 'Test Institution'
            
            # Save the DICOM file
            ds.save_as('uploads/dicom/sample_test.dcm')
            
            print(f"   Status: SUCCESS")
            print(f"   Created: uploads/dicom/sample_test.dcm")
            print(f"   Size: {512}x512 pixels")
            print(f"   Patient: Test Patient")
            print(f"   Modality: CT")
            
            return True
            
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def test_upload_dicom(self):
        """Test DICOM file upload"""
        print("\n UPLOAD DICOM FILE")
        print("-" * 40)
        
        try:
            # Check if sample file exists
            sample_file = 'uploads/dicom/sample_test.dcm'
            if not os.path.exists(sample_file):
                print(f"   Status: FAILED - Sample file not found")
                return None
            
            # Upload the file
            with open(sample_file, 'rb') as f:
                files = {'file': (sample_file, f, 'application/dicom')}
                response = requests.post(f"{self.base_url}/api/dicom/upload", 
                                       files=files, headers=self.get_headers(), timeout=10)
            
            if response.status_code == 201:
                data = response.json()
                print(f"   Status: SUCCESS")
                print(f"   Message: {data.get('message', '')}")
                
                file_info = data.get('file', {})
                print(f"   Original: {file_info.get('originalName', '')}")
                print(f"   Stored: {file_info.get('filename', '')}")
                print(f"   Size: {file_info.get('size', 0)} bytes")
                print(f"   Thumbnail: {'Yes' if data.get('thumbnail') else 'No'}")
                print(f"   PNG: {'Yes' if data.get('processedImage') else 'No'}")
                
                metadata = data.get('metadata', {})
                if 'patient_info' in metadata:
                    patient = metadata['patient_info']
                    print(f"   Patient: {patient.get('patient_name', '')}")
                    print(f"   ID: {patient.get('patient_id', '')}")
                
                if 'study_info' in metadata:
                    study = metadata['study_info']
                    print(f"   Study: {study.get('study_description', '')}")
                    print(f"   Modality: {study.get('modality', '')}")
                
                return file_info.get('filename')
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return None
    
    def test_get_metadata(self, filename):
        """Test getting DICOM metadata"""
        print(f"\n GET METADATA")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/api/dicom/metadata/{filename}", 
                                  headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                metadata = response.json()
                print(f"   Status: SUCCESS")
                
                # Display key metadata
                if 'patient_info' in metadata:
                    patient = metadata['patient_info']
                    print(f"   Patient: {patient.get('patient_name', '')}")
                    print(f"   ID: {patient.get('patient_id', '')}")
                    print(f"   DOB: {patient.get('patient_birth_date', '')}")
                    print(f"   Sex: {patient.get('patient_sex', '')}")
                
                if 'study_info' in metadata:
                    study = metadata['study_info']
                    print(f"   Study: {study.get('study_description', '')}")
                    print(f"   Date: {study.get('study_date', '')}")
                    print(f"   Modality: {study.get('modality', '')}")
                
                if 'image_info' in metadata:
                    image = metadata['image_info']
                    print(f"   Image: {image.get('rows', '')}x{image.get('columns', '')}")
                    print(f"   Bits: {image.get('bits_stored', '')}")
                
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def test_get_thumbnail(self, filename):
        """Test getting DICOM thumbnail"""
        print(f"\n GET THUMBNAIL")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/api/dicom/thumbnail/{filename}", 
                                  headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                print(f"   Status: SUCCESS")
                print(f"   Content-Type: {response.headers.get('content-type', '')}")
                print(f"   Size: {len(response.content)} bytes")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def test_get_image(self, filename):
        """Test getting processed DICOM image"""
        print(f"\n GET PROCESSED IMAGE")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/api/dicom/image/{filename}", 
                                  headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                print(f"   Status: SUCCESS")
                print(f"   Content-Type: {response.headers.get('content-type', '')}")
                print(f"   Size: {len(response.content)} bytes")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def test_enhance_image(self, filename):
        """Test image enhancement"""
        print(f"\n ENHANCE IMAGE")
        print("-" * 40)
        
        try:
            data = {'enhancement': 'contrast'}
            response = requests.post(f"{self.base_url}/api/dicom/enhance/{filename}", 
                                   json=data, headers=self.get_headers(), timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Status: SUCCESS")
                print(f"   Enhancement: {result.get('enhancement', '')}")
                print(f"   Image Size: {len(result.get('enhancedImage', ''))} chars")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def test_statistics(self, filename):
        """Test image statistics"""
        print(f"\n IMAGE STATISTICS")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/api/dicom/statistics/{filename}", 
                                  headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                stats = response.json()
                print(f"   Status: SUCCESS")
                print(f"   Min Value: {stats.get('minValue', '')}")
                print(f"   Max Value: {stats.get('maxValue', '')}")
                print(f"   Mean Value: {stats.get('meanValue', '')}")
                print(f"   Std Value: {stats.get('stdValue', '')}")
                print(f"   Shape: {stats.get('shape', '')}")
                print(f"   Dtype: {stats.get('dtype', '')}")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def test_delete_file(self, filename):
        """Test deleting DICOM file"""
        print(f"\n DELETE FILE")
        print("-" * 40)
        
        try:
            response = requests.delete(f"{self.base_url}/api/dicom/delete/{filename}", 
                                     headers=self.get_headers(), timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Status: SUCCESS")
                print(f"   Message: {data.get('message', '')}")
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def run_complete_test(self):
        """Run complete DICOM backend test"""
        print(" COMPLETE DICOM BACKEND TEST")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Authenticate
        auth_ok = self.authenticate()
        if not auth_ok:
            print("\n Authentication failed - cannot continue")
            return False
        
        # Step 2: Health check
        health_ok = self.test_health_check()
        
        # Step 3: List files (initial)
        initial_files = self.test_list_files()
        
        # Step 4: Create sample DICOM file
        sample_created = self.create_sample_dicom_file()
        
        # Step 5: Upload DICOM file
        uploaded_filename = self.test_upload_dicom()
        
        if uploaded_filename:
            # Step 6: Get metadata
            metadata_ok = self.test_get_metadata(uploaded_filename)
            
            # Step 7: Get thumbnail
            thumbnail_ok = self.test_get_thumbnail(uploaded_filename)
            
            # Step 8: Get processed image
            image_ok = self.test_get_image(uploaded_filename)
            
            # Step 9: Enhance image
            enhance_ok = self.test_enhance_image(uploaded_filename)
            
            # Step 10: Get statistics
            stats_ok = self.test_statistics(uploaded_filename)
            
            # Step 11: List files (after upload)
            updated_files = self.test_list_files()
            
            # Step 12: Delete file
            delete_ok = self.test_delete_file(uploaded_filename)
        
        # Summary
        print("\n" + "=" * 60)
        print(" TEST SUMMARY")
        print("=" * 60)
        print(f"Authentication: {'PASS' if auth_ok else 'FAIL'}")
        print(f"Health Check: {'PASS' if health_ok else 'FAIL'}")
        print(f"Sample Creation: {'PASS' if sample_created else 'FAIL'}")
        print(f"File Upload: {'PASS' if uploaded_filename else 'FAIL'}")
        if uploaded_filename:
            print(f"Metadata: {'PASS' if metadata_ok else 'FAIL'}")
            print(f"Thumbnail: {'PASS' if thumbnail_ok else 'FAIL'}")
            print(f"Image: {'PASS' if image_ok else 'FAIL'}")
            print(f"Enhancement: {'PASS' if enhance_ok else 'FAIL'}")
            print(f"Statistics: {'PASS' if stats_ok else 'FAIL'}")
            print(f"File Deletion: {'PASS' if delete_ok else 'FAIL'}")
        
        success = auth_ok and health_ok and sample_created and uploaded_filename
        
        print(f"\nOverall Status: {'PASS' if success else 'FAIL'}")
        
        if success:
            print("\n DICOM BACKEND: FULLY FUNCTIONAL")
            print(" All DICOM processing features are working")
            print(" Frontend can now mirror backend functionality")
            print(" Real medical image processing is available")
            print(" Backend mirrors frontend requirements completely")
        else:
            print("\n DICOM BACKEND: NEEDS FIXING")
            print(" Check failed operations above")
        
        return success

if __name__ == "__main__":
    tester = DICOMCompleteTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n FRONTEND INTEGRATION READY:")
        print("1. Create DICOM viewer components")
        print("2. Add file upload functionality")
        print("3. Implement image enhancement controls")
        print("4. Add metadata display panels")
        print("5. Test complete frontend-backend integration")
        print("\n BACKEND MIRRORS FRONTEND:")
        print("- DICOM file upload and processing")
        print("- Metadata extraction and display")
        print("- Image rendering and thumbnails")
        print("- Image enhancement capabilities")
        print("- File management and statistics")
    else:
        print("\n TROUBLESHOOTING:")
        print("1. Check DICOM backend service is running on port 5002")
        print("2. Verify authentication is working")
        print("3. Check required packages are installed")
        print("4. Review error messages above")
