#!/usr/bin/env python3
"""
Test DICOM Backend with Working Sample File
Test all DICOM processing functionality with proper DICOM file
"""

import requests
import json
import os
from datetime import datetime

class DICOMWorkingTester:
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
                return True
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return False
    
    def get_headers(self):
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.auth_token}"}
    
    def test_upload_working_dicom(self):
        """Test uploading working DICOM file"""
        print("\n UPLOAD WORKING DICOM FILE")
        print("-" * 40)
        
        try:
            # Check if working sample file exists
            sample_file = 'uploads/dicom/working_sample.dcm'
            if not os.path.exists(sample_file):
                print(f"   Status: FAILED - Working sample file not found")
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
                
                for file_info in files:
                    print(f"      - {file_info['filename']}")
                    print(f"        Size: {file_info['size']} bytes")
                    print(f"        Thumbnail: {'Yes' if file_info['thumbnail'] else 'No'}")
                    print(f"        Processed: {'Yes' if file_info['processedImage'] else 'No'}")
                
                return files
            else:
                print(f"   Status: FAILED - HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   Status: ERROR - {e}")
            return []
    
    def run_complete_test(self):
        """Run complete DICOM backend test with working file"""
        print(" DICOM BACKEND TEST - WORKING FILE")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Authenticate
        auth_ok = self.authenticate()
        if not auth_ok:
            print("\n Authentication failed - cannot continue")
            return False
        
        # Step 2: Upload working DICOM file
        uploaded_filename = self.test_upload_working_dicom()
        
        if uploaded_filename:
            # Step 3: Get metadata
            metadata_ok = self.test_get_metadata(uploaded_filename)
            
            # Step 4: Get thumbnail
            thumbnail_ok = self.test_get_thumbnail(uploaded_filename)
            
            # Step 5: Get processed image
            image_ok = self.test_get_image(uploaded_filename)
            
            # Step 6: Enhance image
            enhance_ok = self.test_enhance_image(uploaded_filename)
            
            # Step 7: Get statistics
            stats_ok = self.test_statistics(uploaded_filename)
            
            # Step 8: List files
            files_ok = self.test_list_files()
            
            success = auth_ok and uploaded_filename and metadata_ok and thumbnail_ok and image_ok and enhance_ok and stats_ok
        else:
            success = False
        
        # Summary
        print("\n" + "=" * 60)
        print(" TEST SUMMARY")
        print("=" * 60)
        print(f"Authentication: {'PASS' if auth_ok else 'FAIL'}")
        print(f"File Upload: {'PASS' if uploaded_filename else 'FAIL'}")
        if uploaded_filename:
            print(f"Metadata: {'PASS' if metadata_ok else 'FAIL'}")
            print(f"Thumbnail: {'PASS' if thumbnail_ok else 'FAIL'}")
            print(f"Image: {'PASS' if image_ok else 'FAIL'}")
            print(f"Enhancement: {'PASS' if enhance_ok else 'FAIL'}")
            print(f"Statistics: {'PASS' if stats_ok else 'FAIL'}")
            print(f"File List: {'PASS' if files_ok else 'FAIL'}")
        
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
    tester = DICOMWorkingTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n DICOM BACKEND MIRRORS FRONTEND:")
        print("=====================================")
        print("FRONTEND REQUIREMENT -> BACKEND CAPABILITY")
        print("=====================================")
        print("DICOM file upload -> /api/dicom/upload")
        print("Metadata display -> /api/dicom/metadata/:filename")
        print("Image rendering -> /api/dicom/image/:filename")
        print("Thumbnail generation -> /api/dicom/thumbnail/:filename")
        print("Image enhancement -> /api/dicom/enhance/:filename")
        print("File management -> /api/dicom/files")
        print("Statistics -> /api/dicom/statistics/:filename")
        print("\n FRONTEND INTEGRATION READY:")
        print("1. Add DICOM upload component")
        print("2. Create image viewer with enhancement controls")
        print("3. Add metadata display panel")
        print("4. Implement file management interface")
        print("5. Test complete frontend-backend integration")
    else:
        print("\n TROUBLESHOOTING:")
        print("1. Check DICOM backend service is running on port 5002")
        print("2. Verify authentication is working")
        print("3. Check required packages are installed")
        print("4. Review error messages above")
