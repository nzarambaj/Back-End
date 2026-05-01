// Simple Patient CRUD Backend with Mock Database
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

// Mock database (simulating PostgreSQL 18)
let patients = [
  {
    id: '1f5bddc5-3465-40c0-a43c-4018b37b52e6',
    firstName: 'Alice',
    lastName: 'Brown',
    email: 'alice.brown@email.com',
    phoneNumber: '+1234567890',
    dateOfBirth: '1985-05-15',
    gender: 'female',
    address: '123 Main St, City, State',
    medicalHistory: 'Hypertension, Type 2 Diabetes',
    allergies: 'Penicillin, Peanuts',
    emergencyContact: 'John Brown',
    emergencyPhone: '+1234567891',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

// Helper function to generate UUID
const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

// Validation middleware
const validatePatient = (req, res, next) => {
  const { firstName, lastName, email, phoneNumber, dateOfBirth, gender } = req.body;
  
  if (!firstName || !lastName || !email || !phoneNumber || !dateOfBirth || !gender) {
    return res.status(400).json({ 
      error: 'Missing required fields',
      required: ['firstName', 'lastName', 'email', 'phoneNumber', 'dateOfBirth', 'gender']
    });
  }
  
  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ error: 'Invalid email format' });
  }
  
  // Validate gender
  const validGenders = ['male', 'female', 'other'];
  if (!validGenders.includes(gender.toLowerCase())) {
    return res.status(400).json({ 
      error: 'Invalid gender',
      validOptions: validGenders
    });
  }
  
  next();
};

// Routes

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    database: 'PostgreSQL 18 (Mock)',
    timestamp: new Date().toISOString(),
    server: 'Patient CRUD Backend',
    patients: patients.length
  });
});

// Login
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }

    const testUsers = [
      { email: 'test@example.com', password: 'test123', role: 'admin', firstName: 'Test', lastName: 'User' },
      { email: 'admin@medical.com', password: 'admin123', role: 'admin', firstName: 'Admin', lastName: 'User' },
      { email: 'doctor@medical.com', password: 'doctor123', role: 'doctor', firstName: 'John', lastName: 'Doe' }
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

// GET all patients
app.get('/api/patients', authenticateToken, (req, res) => {
  res.json({ patients: patients.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)) });
});

// GET single patient
app.get('/api/patients/:id', authenticateToken, (req, res) => {
  const { id } = req.params;
  const patient = patients.find(p => p.id === id);
  
  if (!patient) {
    return res.status(404).json({ error: 'Patient not found' });
  }
  
  res.json({ patient });
});

// CREATE new patient
app.post('/api/patients', authenticateToken, validatePatient, (req, res) => {
  try {
    const { 
      firstName, 
      lastName, 
      email, 
      phoneNumber, 
      dateOfBirth, 
      gender, 
      address, 
      medicalHistory, 
      allergies, 
      emergencyContact, 
      emergencyPhone 
    } = req.body;
    
    // Check if email already exists
    const existingPatient = patients.find(p => p.email === email);
    if (existingPatient) {
      return res.status(400).json({ error: 'Patient with this email already exists' });
    }
    
    const newPatient = {
      id: generateUUID(),
      firstName,
      lastName,
      email,
      phoneNumber,
      dateOfBirth,
      gender,
      address: address || '',
      medicalHistory: medicalHistory || '',
      allergies: allergies || '',
      emergencyContact: emergencyContact || '',
      emergencyPhone: emergencyPhone || '',
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

// UPDATE patient
app.put('/api/patients/:id', authenticateToken, validatePatient, (req, res) => {
  try {
    const { id } = req.params;
    const { 
      firstName, 
      lastName, 
      email, 
      phoneNumber, 
      dateOfBirth, 
      gender, 
      address, 
      medicalHistory, 
      allergies, 
      emergencyContact, 
      emergencyPhone 
    } = req.body;
    
    const patientIndex = patients.findIndex(p => p.id === id);
    
    if (patientIndex === -1) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    // Check if email is being changed and if new email already exists
    if (email && patients[patientIndex].email !== email) {
      const emailCheck = patients.find(p => p.email === email && p.id !== id);
      if (emailCheck) {
        return res.status(400).json({ error: 'Patient with this email already exists' });
      }
    }
    
    const updatedPatient = {
      ...patients[patientIndex],
      firstName,
      lastName,
      email,
      phoneNumber,
      dateOfBirth,
      gender,
      address: address || '',
      medicalHistory: medicalHistory || '',
      allergies: allergies || '',
      emergencyContact: emergencyContact || '',
      emergencyPhone: emergencyPhone || '',
      updatedAt: new Date().toISOString()
    };
    
    patients[patientIndex] = updatedPatient;
    
    res.json({
      message: 'Patient updated successfully',
      patient: updatedPatient
    });
  } catch (error) {
    console.error('Update patient error:', error);
    res.status(500).json({ error: 'Failed to update patient' });
  }
});

// DELETE patient
app.delete('/api/patients/:id', authenticateToken, (req, res) => {
  try {
    const { id } = req.params;
    
    const patientIndex = patients.findIndex(p => p.id === id);
    
    if (patientIndex === -1) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    // In a real system, you'd check for associated studies
    // For this demo, we'll just remove the patient
    patients.splice(patientIndex, 1);
    
    res.json({
      message: 'Patient deleted successfully'
    });
  } catch (error) {
    console.error('Delete patient error:', error);
    res.status(500).json({ error: 'Failed to delete patient' });
  }
});

// Get other endpoints for completeness
app.get('/api/doctors', authenticateToken, (req, res) => {
  const doctors = [
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

  res.json({ doctors });
});

app.get('/api/studies', authenticateToken, (req, res) => {
  const studies = [
    {
      id: '6j0ghi00-89bc-95h5-f98h-9563g8cg07j1',
      patientId: patients[0]?.id || '1f5bddc5-3465-40c0-a43c-4018b37b52e6',
      doctorId: '4h8efg88-6798-73f3-d76f-7341e6ae85h9',
      patientName: patients[0] ? `${patients[0].firstName} ${patients[0].lastName}` : 'Alice Brown',
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
        reportedBy: '4h8efg88-6798-73f3-d76f-7341e6ae85h9',
        reportDate: new Date().toISOString(),
        reportStatus: 'completed'
      },
      accessionNumber: 'ACC20240430001',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  ];

  res.json({ studies });
});

// Start server
app.listen(PORT, () => {
  console.log(`Patient CRUD Backend Server running on port ${PORT}`);
  console.log(`Database: PostgreSQL 18 (Mock)`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`Login endpoint: http://localhost:${PORT}/api/auth/login`);
  console.log(`Patient CRUD: http://localhost:${PORT}/api/patients`);
  console.log(`Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:3000'}`);
  console.log(`Initial patients: ${patients.length}`);
});

module.exports = app;
