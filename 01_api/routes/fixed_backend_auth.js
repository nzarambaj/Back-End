// Fixed Backend Server with PostgreSQL 18 and Mock Data
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());

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

// Mock data (simulating database access)
const mockPatients = [
  {
    id: '1f5bddc5-3465-40c0-a43c-4018b37b52e6',
    firstName: 'Alice',
    lastName: 'Brown',
    email: 'alice.brown@email.com',
    phoneNumber: '+1234567890',
    dateOfBirth: '1985-05-15',
    gender: 'female',
    address: '123 Main St, City, State',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    id: '2f6cde66-4576-51d1-b54d-5129c48c63f7',
    firstName: 'Bob',
    lastName: 'Smith',
    email: 'bob.smith@email.com',
    phoneNumber: '+0987654321',
    dateOfBirth: '1978-08-22',
    gender: 'male',
    address: '456 Oak Ave, Town, State',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    id: '3g7def77-5687-62e2-c65e-6230d59d74g8',
    firstName: 'Carol',
    lastName: 'Johnson',
    email: 'carol.johnson@email.com',
    phoneNumber: '+1122334455',
    dateOfBirth: '1990-12-03',
    gender: 'female',
    address: '789 Pine Rd, Village, State',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

const mockDoctors = [
  {
    id: '4h8efg88-6798-73f3-d76f-7341e6ae85h9',
    firstName: 'Sarah',
    lastName: 'Wilson',
    email: 'sarah.wilson@hospital.com',
    phoneNumber: '+2233445566',
    specialty: 'Radiology',
    licenseNumber: 'RAD123456',
    department: 'Radiology',
    isActive: true,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    id: '5i9fgh99-78ab-84g4-e87g-8452f7bf96i0',
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@hospital.com',
    phoneNumber: '+3344556677',
    specialty: 'Cardiology',
    licenseNumber: 'CAR789012',
    department: 'Cardiology',
    isActive: true,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

const mockStudies = [
  {
    id: '6j0ghi00-89bc-95h5-f98h-9563g8cg07j1',
    patientId: mockPatients[0].id,
    doctorId: mockDoctors[0].id,
    patientName: 'Alice Brown',
    doctorName: 'Sarah Wilson',
    modality: 'CT',
    bodyPart: 'Chest',
    studyDate: new Date().toISOString().split('T')[0],
    studyTime: '14:30:00',
    status: 'completed',
    priority: 'routine',
    indication: 'Chest pain evaluation',
    contrastUsed: true,
    contrastType: 'iodinated',
    report: {
      findings: 'Normal chest CT scan',
      impression: 'No acute pulmonary pathology',
      recommendation: 'Routine follow-up',
      reportedBy: mockDoctors[0].id,
      reportDate: new Date().toISOString(),
      reportStatus: 'completed'
    },
    accessionNumber: 'ACC20240430001',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    id: '7k1hij11-9acd-06i6-g09i-0674h9dh18k2',
    patientId: mockPatients[1].id,
    doctorId: mockDoctors[1].id,
    patientName: 'Bob Smith',
    doctorName: 'John Doe',
    modality: 'MRI',
    bodyPart: 'Brain',
    studyDate: new Date().toISOString().split('T')[0],
    studyTime: '10:15:00',
    status: 'in-progress',
    priority: 'urgent',
    indication: 'Headache evaluation',
    contrastUsed: false,
    contrastType: null,
    report: {
      findings: '',
      impression: '',
      recommendation: '',
      reportedBy: null,
      reportDate: null,
      reportStatus: 'pending'
    },
    accessionNumber: 'ACC20240430002',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

const mockImages = [
  {
    id: '8l2ijk22-abde-17j7-h0aj-1785i9ei29l3',
    studyId: mockStudies[0].id,
    filename: 'alice_brown_chest_ct_001.dcm',
    originalName: 'alice_brown_chest_ct_001.dcm',
    mimeType: 'application/dicom',
    size: 1048576,
    path: '/uploads/dicom/alice_brown_chest_ct_001.dcm',
    thumbnailPath: '/uploads/thumbnails/alice_brown_chest_ct_001.jpg',
    uploadDate: new Date().toISOString(),
    processed: true,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    id: '9m3jkl33-bcef-28k8-i1bk-2896j0fj30m4',
    studyId: mockStudies[1].id,
    filename: 'bob_smith_brain_mri_001.dcm',
    originalName: 'bob_smith_brain_mri_001.dcm',
    mimeType: 'application/dicom',
    size: 2097152,
    path: '/uploads/dicom/bob_smith_brain_mri_001.dcm',
    thumbnailPath: '/uploads/thumbnails/bob_smith_brain_mri_001.jpg',
    uploadDate: new Date().toISOString(),
    processed: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

// Routes

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    database: 'PostgreSQL 18 (Mock Data)',
    timestamp: new Date().toISOString(),
    server: 'Express.js with Authentication',
    patients: mockPatients.length,
    doctors: mockDoctors.length,
    studies: mockStudies.length,
    images: mockImages.length
  });
});

// Login
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }

    // Test users
    const testUsers = [
      { email: 'test@example.com', password: 'test123', role: 'admin', firstName: 'Test', lastName: 'User' },
      { email: 'admin@medical.com', password: 'admin123', role: 'admin', firstName: 'Admin', lastName: 'User' },
      { email: 'doctor@medical.com', password: 'doctor123', role: 'doctor', firstName: 'John', lastName: 'Doe' }
    ];

    const user = testUsers.find(u => u.email === email && u.password === password);

    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Create JWT token
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

// Get patients
app.get('/api/patients', authenticateToken, (req, res) => {
  res.json({ patients: mockPatients });
});

// Get doctors
app.get('/api/doctors', authenticateToken, (req, res) => {
  res.json({ doctors: mockDoctors });
});

// Get studies
app.get('/api/studies', authenticateToken, (req, res) => {
  res.json({ studies: mockStudies });
});

// Get images
app.get('/api/images', authenticateToken, (req, res) => {
  res.json({ images: mockImages });
});

// Start server
app.listen(PORT, () => {
  console.log(`Fixed Medical Imaging Backend Server running on port ${PORT}`);
  console.log(`Database: PostgreSQL 18 (Mock Data)`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`Login endpoint: http://localhost:${PORT}/api/auth/login`);
  console.log(`Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:3000'}`);
  console.log(`Mock Data: ${mockPatients.length} patients, ${mockDoctors.length} doctors, ${mockStudies.length} studies, ${mockImages.length} images`);
});

module.exports = app;
