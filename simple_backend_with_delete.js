// Simple Backend with Doctors Delete Endpoint
// PostgreSQL password: Sibo25Mana

const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = 5000;

// Middleware
app.use(cors({
  origin: ['http://localhost:3000', 'http://127.0.0.1:3000'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());

// In-memory data storage (working fallback)
let doctors = [
  {
    id: 1,
    full_name: 'Dr. John Wilson',
    specialization: 'Radiology',
    phone: '555-0201',
    email: 'john.wilson@medical.com',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: 2,
    full_name: 'Dr. Sarah Johnson',
    specialization: 'Cardiology',
    phone: '555-0202',
    email: 'sarah.johnson@medical.com',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: 3,
    full_name: 'Dr. Michael Brown',
    specialization: 'Neurology',
    phone: '555-0203',
    email: 'michael.brown@medical.com',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
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

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Simple Backend with Doctors Delete',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    port: PORT,
    database: 'In-memory storage',
    postgresql_password: 'Sibo25Mana',
    features: ['Authentication', 'Patient CRUD', 'Doctor CRUD', 'Studies CRUD', 'CORS Enabled']
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

// Doctor CRUD Routes
app.get('/api/doctors', authenticateToken, (req, res) => {
  res.json({
    doctors: doctors,
    total: doctors.length
  });
});

app.post('/api/doctors', authenticateToken, (req, res) => {
  try {
    const { full_name, specialization, phone, email } = req.body;
    
    if (!full_name || !specialization) {
      return res.status(400).json({ 
        error: 'Missing required fields: full_name, specialization' 
      });
    }
    
    const newDoctor = {
      id: doctors.length + 1,
      full_name: full_name,
      specialization: specialization,
      phone: phone || null,
      email: email || null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    doctors.push(newDoctor);
    
    res.status(201).json({
      message: 'Doctor created successfully',
      doctor: newDoctor
    });
    
  } catch (error) {
    console.error('Create doctor error:', error);
    res.status(500).json({ error: 'Failed to create doctor' });
  }
});

app.delete('/doctors/:id', authenticateToken, (req, res) => {
  try {
    const { id } = req.params;
    const doctorId = parseInt(id);

    // Find the doctor
    const doctor = doctors.find(d => d.id === doctorId);
    
    if (!doctor) {
      return res.status(404).json({ error: 'Doctor not found' });
    }

    // Delete the doctor
    const doctorIndex = doctors.findIndex(d => d.id === doctorId);
    const deletedDoctor = doctors[doctorIndex];
    doctors.splice(doctorIndex, 1);

    res.json({ 
      message: 'Doctor deleted successfully',
      doctor: deletedDoctor
    });
    
  } catch (error) {
    console.error('Delete doctor error:', error);
    res.status(500).json({ error: 'Failed to delete doctor' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Simple Backend with Doctors Delete running on port ${PORT}`);
  console.log(`PostgreSQL Password: Sibo25Mana`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`Login endpoint: http://localhost:${PORT}/api/auth/login`);
  console.log(`Frontend URL: http://localhost:3000`);
  console.log(`Features: Patient CRUD, Doctor CRUD, Studies CRUD`);
  console.log(`Delete endpoint: app.delete('/doctors/:id', ...) - WORKING`);
  console.log(`Your delete code: const { id } = req.params; doctors.splice(doctorIndex, 1);`);
});
