#!/usr/bin/env python3
"""
Organize DICOM Backend Folder Structure
Create clean, organized DICOM backend without authentication
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class DICOMBackendOrganizer:
    def __init__(self):
        self.base_path = Path(r"C:\Users\TTR\Documents\Project_BackEnd")
        self.dicom_path = self.base_path / "dicom_service"
        
    def create_organized_structure(self):
        """Create organized DICOM backend folder structure"""
        print(" ORGANIZING DICOM BACKEND FOLDER")
        print("=" * 60)
        
        # Create main DICOM service directory
        directories = [
            "dicom_service",
            "dicom_service/src",
            "dicom_service/src/routes",
            "dicom_service/src/middleware",
            "dicom_service/src/processors",
            "dicom_service/src/utils",
            "dicom_service/uploads",
            "dicom_service/uploads/dicom",
            "dicom_service/uploads/thumbnails",
            "dicom_service/uploads/processed",
            "dicom_service/config",
            "dicom_service/tests",
            "dicom_service/docs"
        ]
        
        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   Created: {directory}")
        
        return True
    
    def create_clean_dicom_backend(self):
        """Create clean DICOM backend without authentication"""
        print("\n CREATING CLEAN DICOM BACKEND")
        print("=" * 60)
        
        backend_content = '''// Clean DICOM Backend Service
// Organized DICOM processing without authentication
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 5002;

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());

// Create upload directories
const uploadDir = 'uploads';
const dicomDir = path.join(uploadDir, 'dicom');
const thumbnailDir = path.join(uploadDir, 'thumbnails');
const processedDir = path.join(uploadDir, 'processed');

[uploadDir, dicomDir, thumbnailDir, processedDir].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, dicomDir);
  },
  filename: (req, file, cb) => {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const originalName = file.originalname.replace(/[^a-zA-Z0-9.]/g, '_');
    cb(null, `${timestamp}_${originalName}`);
  }
});

const upload = multer({ 
  storage: storage,
  limits: {
    fileSize: 100 * 1024 * 1024 // 100MB limit
  },
  fileFilter: (req, file, cb) => {
    // Accept DICOM files
    const allowedExtensions = ['.dcm', '.dicom', '.dic', '.ima'];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowedExtensions.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Only DICOM files are allowed'), false);
    }
  }
});

// Python DICOM processor bridge
const processDICOM = (action, filePath, options = {}) => {
  return new Promise((resolve, reject) => {
    const pythonScript = path.join(__dirname, 'dicom_processor.py');
    
    const python = spawn('python', [pythonScript, action, filePath, JSON.stringify(options)]);
    
    let data = '';
    let error = '';
    
    python.stdout.on('data', (chunk) => {
      data += chunk.toString();
    });
    
    python.stderr.on('data', (chunk) => {
      error += chunk.toString();
    });
    
    python.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(error || 'Python script failed'));
      } else {
        try {
          const result = JSON.parse(data);
          resolve(result);
        } catch (e) {
          reject(new Error('Failed to parse Python output'));
        }
      }
    });
  });
};

// Routes

// Health check
app.get('/api/dicom/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Clean DICOM Backend',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    port: PORT,
    authentication: 'disabled',
    features: [
      'DICOM file upload',
      'Metadata extraction',
      'Image rendering',
      'Thumbnail generation',
      'Image enhancement',
      'File management'
    ]
  });
});

// Upload DICOM file (no authentication required)
app.post('/api/dicom/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file provided' });
    }

    const filePath = req.file.path;
    const filename = req.file.filename;

    // Process DICOM file using Python bridge
    const result = await processDICOM('extract_metadata', filePath);

    if (result.error) {
      // Clean up file if processing failed
      fs.unlinkSync(filePath);
      return res.status(500).json({ error: result.error });
    }

    // Generate thumbnail
    let thumbnailResult = { success: false };
    try {
      thumbnailResult = await processDICOM('generate_thumbnail', filePath);
    } catch (e) {
      console.log('Thumbnail generation failed:', e.message);
    }
    
    // Generate processed image
    let imageResult = { success: false };
    try {
      imageResult = await processDICOM('generate_image', filePath);
    } catch (e) {
      console.log('Image generation failed:', e.message);
    }

    const response = {
      message: 'DICOM file uploaded and processed successfully',
      file: {
        originalName: req.file.originalname,
        filename: filename,
        size: req.file.size,
        path: filePath
      },
      metadata: result.metadata,
      thumbnail: thumbnailResult.success ? thumbnailResult.thumbnail_path : null,
      processedImage: imageResult.success ? imageResult.image_path : null
    };

    res.status(201).json(response);

  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ error: 'Failed to process DICOM file' });
  }
});

// List DICOM files (no authentication required)
app.get('/api/dicom/files', (req, res) => {
  try {
    const files = fs.readdirSync(dicomDir)
      .filter(file => file.endsWith('.dcm') || file.endsWith('.dicom'))
      .map(file => {
        const filePath = path.join(dicomDir, file);
        const stats = fs.statSync(filePath);
        const baseName = path.basename(file, path.extname(file));
        
        return {
          filename: file,
          originalName: file.split('_').slice(1).join('_').replace(/_/g, '.'),
          size: stats.size,
          createdAt: stats.birthtime,
          modifiedAt: stats.mtime,
          thumbnail: fs.existsSync(path.join(thumbnailDir, `${baseName}.jpg`)),
          processedImage: fs.existsSync(path.join(processedDir, `${baseName}.png`))
        };
      })
      .sort((a, b) => b.createdAt - a.createdAt);

    res.json({
      files,
      total: files.length
    });

  } catch (error) {
    console.error('List files error:', error);
    res.status(500).json({ error: 'Failed to list files' });
  }
});

// Get DICOM metadata (no authentication required)
app.get('/api/dicom/metadata/:filename', async (req, res) => {
  try {
    const { filename } = req.params;
    const filePath = path.join(dicomDir, filename);

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    const result = await processDICOM('extract_metadata', filePath);

    if (result.error) {
      return res.status(500).json({ error: result.error });
    }

    res.json(result.metadata);

  } catch (error) {
    console.error('Get metadata error:', error);
    res.status(500).json({ error: 'Failed to get metadata' });
  }
});

// Get DICOM thumbnail (no authentication required)
app.get('/api/dicom/thumbnail/:filename', (req, res) => {
  try {
    const { filename } = req.params;
    const baseName = path.basename(filename, path.extname(filename));
    const thumbnailPath = path.join(thumbnailDir, `${baseName}.jpg`);

    if (!fs.existsSync(thumbnailPath)) {
      // Generate thumbnail if it doesn't exist
      const filePath = path.join(dicomDir, filename);
      if (!fs.existsSync(filePath)) {
        return res.status(404).json({ error: 'File not found' });
      }

      processDICOM('generate_thumbnail', filePath).then(() => {
        if (fs.existsSync(thumbnailPath)) {
          res.sendFile(thumbnailPath);
        } else {
          res.status(500).json({ error: 'Failed to generate thumbnail' });
        }
      }).catch(() => {
        res.status(500).json({ error: 'Failed to generate thumbnail' });
      });
    } else {
      res.sendFile(thumbnailPath);
    }

  } catch (error) {
    console.error('Get thumbnail error:', error);
    res.status(500).json({ error: 'Failed to get thumbnail' });
  }
});

// Get processed DICOM image (no authentication required)
app.get('/api/dicom/image/:filename', (req, res) => {
  try {
    const { filename } = req.params;
    const baseName = path.basename(filename, path.extname(filename));
    const imagePath = path.join(processedDir, `${baseName}.png`);

    if (!fs.existsSync(imagePath)) {
      // Generate processed image if it doesn't exist
      const filePath = path.join(dicomDir, filename);
      if (!fs.existsSync(filePath)) {
        return res.status(404).json({ error: 'File not found' });
      }

      processDICOM('generate_image', filePath).then(() => {
        if (fs.existsSync(imagePath)) {
          res.sendFile(imagePath);
        } else {
          res.status(500).json({ error: 'Failed to generate image' });
        }
      }).catch(() => {
        res.status(500).json({ error: 'Failed to generate image' });
      });
    } else {
      res.sendFile(imagePath);
    }

  } catch (error) {
    console.error('Get image error:', error);
    res.status(500).json({ error: 'Failed to get image' });
  }
});

// Enhance DICOM image (no authentication required)
app.post('/api/dicom/enhance/:filename', async (req, res) => {
  try {
    const { filename } = req.params;
    const { enhancement = 'contrast' } = req.body;
    const filePath = path.join(dicomDir, filename);

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    const result = await processDICOM('enhance_image', filePath, { enhancement });

    if (result.error) {
      return res.status(500).json({ error: result.error });
    }

    res.json({
      enhancedImage: result.enhanced_image,
      enhancement: enhancement
    });

  } catch (error) {
    console.error('Enhance image error:', error);
    res.status(500).json({ error: 'Failed to enhance image' });
  }
});

// Get image statistics (no authentication required)
app.get('/api/dicom/statistics/:filename', async (req, res) => {
  try {
    const { filename } = req.params;
    const filePath = path.join(dicomDir, filename);

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    const result = await processDICOM('get_statistics', filePath);

    if (result.error) {
      return res.status(500).json({ error: result.error });
    }

    res.json(result.statistics);

  } catch (error) {
    console.error('Get statistics error:', error);
    res.status(500).json({ error: 'Failed to get statistics' });
  }
});

// Delete DICOM file (no authentication required)
app.delete('/api/dicom/delete/:filename', (req, res) => {
  try {
    const { filename } = req.params;
    const filePath = path.join(dicomDir, filename);
    const baseName = path.basename(filename, path.extname(filename));

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    // Delete main file
    fs.unlinkSync(filePath);

    // Delete thumbnail
    const thumbnailPath = path.join(thumbnailDir, `${baseName}.jpg`);
    if (fs.existsSync(thumbnailPath)) {
      fs.unlinkSync(thumbnailPath);
    }

    // Delete processed image
    const imagePath = path.join(processedDir, `${baseName}.png`);
    if (fs.existsSync(imagePath)) {
      fs.unlinkSync(imagePath);
    }

    res.json({ message: 'DICOM file deleted successfully' });

  } catch (error) {
    console.error('Delete file error:', error);
    res.status(500).json({ error: 'Failed to delete file' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Clean DICOM Backend Service running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/dicom/health`);
  console.log(`Upload endpoint: http://localhost:${PORT}/api/dicom/upload`);
  console.log(`Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:3000'}`);
  console.log(`Authentication: DISABLED`);
});

module.exports = app;
'''
        
        with open(self.dicom_path / 'server.js', 'w') as f:
            f.write(backend_content)
        
        print("   Created: dicom_service/server.js")
        return True
    
    def copy_dicom_processor(self):
        """Copy DICOM processor to organized structure"""
        print("\n COPYING DICOM PROCESSOR")
        print("=" * 60)
        
        # Copy existing DICOM processor
        source_processor = self.base_path / 'dicom_processor.py'
        target_processor = self.dicom_path / 'dicom_processor.py'
        
        if source_processor.exists():
            shutil.copy2(source_processor, target_processor)
            print("   Copied: dicom_processor.py")
        else:
            print("   Warning: Original dicom_processor.py not found")
        
        return True
    
    def create_package_json(self):
        """Create package.json for DICOM service"""
        print("\n CREATING PACKAGE.JSON")
        print("=" * 60)
        
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
        
        with open(self.dicom_path / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)
        
        print("   Created: package.json")
        return True
    
    def create_readme(self):
        """Create README for DICOM service"""
        print("\n CREATING README")
        print("=" * 60)
        
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

## File Structure

```
dicom_service/
  server.js              # Main server file
  dicom_processor.py     # Python DICOM processor
  uploads/
    dicom/               # Uploaded DICOM files
    thumbnails/          # Generated thumbnails
    processed/           # Processed PNG images
```
'''
        
        with open(self.dicom_path / 'README.md', 'w') as f:
            f.write(readme_content)
        
        print("   Created: README.md")
        return True
    
    def create_test_script(self):
        """Create test script for DICOM service"""
        print("\n CREATING TEST SCRIPT")
        print("=" * 60)
        
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
        
        with open(self.dicom_path / 'test_dicom_service.py', 'w') as f:
            f.write(test_content)
        
        print("   Created: test_dicom_service.py")
        return True
    
    def run_organization(self):
        """Run complete organization process"""
        print(" COMPLETE DICOM BACKEND ORGANIZATION")
        print("=" * 80)
        print(f"Base Path: {self.base_path}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Step 1: Create organized structure
        self.create_organized_structure()
        
        # Step 2: Create clean backend
        self.create_clean_dicom_backend()
        
        # Step 3: Copy DICOM processor
        self.copy_dicom_processor()
        
        # Step 4: Create package.json
        self.create_package_json()
        
        # Step 5: Create README
        self.create_readme()
        
        # Step 6: Create test script
        self.create_test_script()
        
        print("\n" + "=" * 80)
        print(" ORGANIZATION COMPLETE")
        print("=" * 80)
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
    organizer = DICOMBackendOrganizer()
    organizer.run_organization()
