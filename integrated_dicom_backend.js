// Integrated DICOM Backend Service
// Complete DICOM processing with Node.js and Python bridge
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const jwt = require('jsonwebtoken');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 5002; // Use port 5002 to avoid conflicts

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

// JWT Secret
const JWT_SECRET = process.env.JWT_SECRET || 'your_super_secret_jwt_key_here_change_in_production';

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};

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
    service: 'Integrated DICOM Backend',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    port: PORT,
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

// Authentication (share with main backend)
app.post('/api/auth/login', (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }

    const testUsers = [
      { email: 'test@example.com', password: 'test123', role: 'admin', firstName: 'Test', lastName: 'User' },
      { email: 'doctor@medical.com', password: 'doctor123', role: 'doctor', firstName: 'John', lastName: 'Doe' },
      { email: 'radiologist@medical.com', password: 'rad123', role: 'radiologist', firstName: 'Sarah', lastName: 'Wilson' }
    ];

    const user = testUsers.find(u => u.email === email && u.password === password);

    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const token = jwt.sign(
      { 
        email: user.email, 
        role: user.role,
        firstName: user.firstName,
        lastName: user.lastName
      },
      JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.json({
      message: 'Login successful',
      token,
      user: {
        email: user.email,
        role: user.role,
        firstName: user.firstName,
        lastName: user.lastName
      }
    });

  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Upload DICOM file
app.post('/api/dicom/upload', authenticateToken, upload.single('file'), async (req, res) => {
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
    const thumbnailResult = await processDICOM('generate_thumbnail', filePath);
    
    // Generate processed image
    const imageResult = await processDICOM('generate_image', filePath);

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

// List DICOM files
app.get('/api/dicom/files', authenticateToken, (req, res) => {
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

// Get DICOM metadata
app.get('/api/dicom/metadata/:filename', authenticateToken, (req, res) => {
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

// Get DICOM thumbnail
app.get('/api/dicom/thumbnail/:filename', authenticateToken, (req, res) => {
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

// Get processed DICOM image
app.get('/api/dicom/image/:filename', authenticateToken, (req, res) => {
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

// Enhance DICOM image
app.post('/api/dicom/enhance/:filename', authenticateToken, (req, res) => {
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

// Get image statistics
app.get('/api/dicom/statistics/:filename', authenticateToken, (req, res) => {
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

// Delete DICOM file
app.delete('/api/dicom/delete/:filename', authenticateToken, (req, res) => {
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
  console.log(`Integrated DICOM Backend Service running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/dicom/health`);
  console.log(`Login endpoint: http://localhost:${PORT}/api/auth/login`);
  console.log(`Upload endpoint: http://localhost:${PORT}/api/dicom/upload`);
  console.log(`Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:3000'}`);
});

module.exports = app;
