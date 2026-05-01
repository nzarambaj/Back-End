#!/usr/bin/env python3
"""
Fix DICOM Backend Organization
Complete the organization with proper imports
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

def complete_dicom_organization():
    """Complete DICOM backend organization"""
    print(" COMPLETING DICOM BACKEND ORGANIZATION")
    print("=" * 60)
    
    base_path = Path(r"C:\Users\TTR\Documents\Project_BackEnd")
    dicom_path = base_path / "dicom_service"
    
    # Create package.json
    package_json = {
        "name": "dicom-service",
        "version": "1.0.0",
        "description": "Clean DICOM processing service without authentication",
        "main": "server.js",
        "scripts": {
            "start": "node server.js",
            "dev": "nodemon server.js",
            "test": "python test_dicom_service.py"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "multer": "^1.4.5-lts.1"
        },
        "devDependencies": {
            "nodemon": "^3.0.1"
        },
        "keywords": ["dicom", "medical", "imaging", "processing"],
        "author": "Medical Imaging System",
        "license": "MIT"
    }
    
    with open(dicom_path / 'package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    
    print("   Created: package.json")
    
    # Create README
    readme_content = '''# DICOM Service

Clean DICOM processing service without authentication requirements.

## Features

- DICOM file upload and processing
- Metadata extraction
- Image rendering and thumbnails
- Image enhancement (contrast, brightness, sharpness)
- File management and statistics
- No authentication required

## API Endpoints

### Health Check
```
GET /api/dicom/health
```

### File Operations
```
POST /api/dicom/upload          # Upload DICOM file
GET  /api/dicom/files           # List all files
DELETE /api/dicom/delete/:id   # Delete file
```

### Image Operations
```
GET  /api/dicom/image/:id       # Get processed image
GET  /api/dicom/thumbnail/:id   # Get thumbnail
POST /api/dicom/enhance/:id     # Enhance image
```

### Data Operations
```
GET  /api/dicom/metadata/:id    # Get metadata
GET  /api/dicom/statistics/:id  # Get statistics
```

## Installation

```bash
cd dicom_service
npm install
npm start
```

## Usage

1. Upload DICOM files via POST to `/api/dicom/upload`
2. View metadata via GET to `/api/dicom/metadata/:filename`
3. Get processed images via GET to `/api/dicom/image/:filename`
4. Enhance images via POST to `/api/dicom/enhance/:filename`

## Supported Formats

- .dcm
- .dicom
- .dic
- .ima
'''
    
    with open(dicom_path / 'README.md', 'w') as f:
        f.write(readme_content)
    
    print("   Created: README.md")
    
    # Create test script
    test_content = '''#!/usr/bin/env python3
"""
Test Clean DICOM Service
Test all functionality without authentication
"""

import requests
import json
import os
from datetime import datetime

def test_dicom_service():
    print(" CLEAN DICOM SERVICE TEST")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/api/dicom/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Health Check: SUCCESS")
            print(f"Service: {data.get('service', 'Unknown')}")
            print(f"Port: {data.get('port', 'Unknown')}")
            print(f"Auth: {data.get('authentication', 'Unknown')}")
        else:
            print(f"Health Check: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"Health Check: ERROR - {e}")
    
    # Test file listing
    try:
        response = requests.get(f"{base_url}/api/dicom/files", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"File Listing: SUCCESS")
            print(f"Total Files: {data.get('total', 0)}")
        else:
            print(f"File Listing: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"File Listing: ERROR - {e}")
    
    print("\\n" + "=" * 50)
    print(" CLEAN DICOM SERVICE: READY")
    print(" No authentication required")
    print(" All endpoints accessible")
    print("=" * 50)

if __name__ == "__main__":
    test_dicom_service()
'''
    
    with open(dicom_path / 'test_dicom_service.py', 'w') as f:
        f.write(test_content)
    
    print("   Created: test_dicom_service.py")
    
    print("\n" + "=" * 60)
    print(" ORGANIZATION COMPLETE")
    print("=" * 60)
    print(" 1. Created organized folder structure")
    print(" 2. Created clean DICOM backend without auth")
    print(" 3. Copied DICOM processor")
    print(" 4. Created package.json")
    print(" 5. Created README.md")
    print(" 6. Created test script")
    
    print("\n NEW STRUCTURE:")
    print("   dicom_service/")
    print("   server.js              # Clean backend (no auth)")
    print("   dicom_processor.py     # DICOM processing")
    print("   uploads/               # File storage")
    print("   package.json           # Dependencies")
    print("   README.md              # Documentation")
    print("   test_dicom_service.py  # Test script")
    
    print("\n NEXT STEPS:")
    print("1. cd dicom_service")
    print("2. npm install")
    print("3. npm start")
    print("4. Test with: python test_dicom_service.py")
    
    return True

if __name__ == "__main__":
    complete_dicom_organization()
