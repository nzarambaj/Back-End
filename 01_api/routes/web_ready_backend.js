// Web-Ready Backend Service
// Proper CRUD operations for ordinary web use
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({
  origin: ['http://localhost:3000', 'http://127.0.0.1:3000'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());

// In-memory data storage (for demo)
let patients = [
  {
    id: 1,
    firstName: 'Jane',
    lastName: 'Smith',
    dateOfBirth: '1990-05-15',
    gender: 'F',
    email: 'jane.smith@example.com',
    phone: '555-0101',
    address: '456 Oak Ave',
    city: 'Springfield',
    state: 'IL',
    zipCode: '62701',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

let doctors = [
  {
    id: 1,
    firstName: 'Dr. John',
    lastName: 'Wilson',
    email: 'john.wilson@medical.com',
    specialty: 'Radiology',
    phone: '555-0202',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    id: 2,
    firstName: 'Dr. Sarah',
    lastName: 'Johnson',
    email: 'sarah.johnson@medical.com',
    specialty: 'Cardiology',
    phone: '555-0203',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

let studies = [
  {
    id: 1,
    patientId: 1,
    doctorId: 1,
    studyType: 'CT',
    studyDate: '2024-01-15',
    description: 'Chest CT scan',
    status: 'completed',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

// JWT Secret
const JWT_SECRET = 'your_super_secret_jwt_key_here_change_in_production';

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

// Validation middleware
const validatePatient = (req, res, next) => {
  const { firstName, lastName, email } = req.body;
  
  if (!firstName || !lastName || !email) {
    return res.status(400).json({ 
      error: 'Missing required fields: firstName, lastName, email' 
    });
  }
  
  if (typeof firstName !== 'string' || typeof lastName !== 'string' || typeof email !== 'string') {
    return res.status(400).json({ 
      error: 'Invalid data types for required fields' 
    });
  }
  
  // Simple email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ error: 'Invalid email format' });
  }
  
  next();
};

// Routes

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Web-Ready Backend',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    port: PORT,
    features: ['Authentication', 'CRUD Operations', 'CORS Enabled']
  });
});

// Authentication
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

// Patient CRUD Routes
app.get('/api/patients', authenticateToken, (req, res) => {
  try {
    res.json({
      patients: patients,
      total: patients.length
    });
  } catch (error) {
    console.error('Get patients error:', error);
    res.status(500).json({ error: 'Failed to get patients' });
  }
});

app.post('/api/patients', authenticateToken, validatePatient, (req, res) => {
  try {
    const patientData = req.body;
    
    // Check for duplicate email
    const existingPatient = patients.find(p => p.email === patientData.email);
    if (existingPatient) {
      return res.status(400).json({ error: 'Patient with this email already exists' });
    }
    
    // Create new patient
    const newPatient = {
      id: patients.length + 1,
      ...patientData,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    patients.push(newPatient);
    
    res.status(201).json({
      message: 'Patient created successfully',
      patient: newPatient
    });
    
  } catch (error) {
    console.error('Create patient error:', error);
    res.status(500).json({ error: 'Failed to create patient' });
  }
});

app.get('/api/patients/:id', authenticateToken, (req, res) => {
  try {
    const patientId = parseInt(req.params.id);
    const patient = patients.find(p => p.id === patientId);
    
    if (!patient) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    res.json(patient);
    
  } catch (error) {
    console.error('Get patient error:', error);
    res.status(500).json({ error: 'Failed to get patient' });
  }
});

app.put('/api/patients/:id', authenticateToken, (req, res) => {
  try {
    const patientId = parseInt(req.params.id);
    const patientIndex = patients.findIndex(p => p.id === patientId);
    
    if (patientIndex === -1) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    const updateData = req.body;
    
    // Update patient
    patients[patientIndex] = {
      ...patients[patientIndex],
      ...updateData,
      updatedAt: new Date().toISOString()
    };
    
    res.json({
      message: 'Patient updated successfully',
      patient: patients[patientIndex]
    });
    
  } catch (error) {
    console.error('Update patient error:', error);
    res.status(500).json({ error: 'Failed to update patient' });
  }
});

app.delete('/api/patients/:id', authenticateToken, (req, res) => {
  try {
    const patientId = parseInt(req.params.id);
    const patientIndex = patients.findIndex(p => p.id === patientId);
    
    if (patientIndex === -1) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    const deletedPatient = patients[patientIndex];
    patients.splice(patientIndex, 1);
    
    res.json({
      message: 'Patient deleted successfully',
      patient: deletedPatient
    });
    
  } catch (error) {
    console.error('Delete patient error:', error);
    res.status(500).json({ error: 'Failed to delete patient' });
  }
});

// Doctor CRUD Routes
app.get('/api/doctors', authenticateToken, (req, res) => {
  try {
    res.json({
      doctors: doctors,
      total: doctors.length
    });
  } catch (error) {
    console.error('Get doctors error:', error);
    res.status(500).json({ error: 'Failed to get doctors' });
  }
});

// Study CRUD Routes
app.get('/api/studies', authenticateToken, (req, res) => {
  try {
    res.json({
      studies: studies,
      total: studies.length
    });
  } catch (error) {
    console.error('Get studies error:', error);
    res.status(500).json({ error: 'Failed to get studies' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Web-Ready Backend Service running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`Login endpoint: http://localhost:${PORT}/api/auth/login`);
  console.log(`Frontend URL: http://localhost:3000`);
  console.log(`CORS: Enabled for frontend`);
});

module.exports = app;
