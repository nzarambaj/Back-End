// System Integration Backend
// Frontend (3000) -> Backend (5000) -> PostgreSQL (5432) -> Flask API (5001)

const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');
const axios = require('axios');

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

// Database configuration
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'medical_imaging',
  password: 'Sibo25Mana',
  port: 5432,
  ssl: false,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Flask API configuration
const FLASK_API_URL = 'http://localhost:5001';

// In-memory fallback data
let fallbackDoctors = [
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

let databaseConnected = false;

// Test database connection
pool.connect((err, client, release) => {
  if (err) {
    console.error('Database connection error:', err.message);
    console.log('Using in-memory data as fallback');
    databaseConnected = false;
  } else {
    console.log('Database connected successfully to medical_imaging');
    console.log('PostgreSQL 18 integration: ACTIVE');
    databaseConnected = true;
    release();
  }
});

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
    service: 'System Integration Backend',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    port: PORT,
    database: databaseConnected ? 'PostgreSQL 18 - medical_imaging' : 'In-memory fallback',
    database_connected: databaseConnected,
    flask_api: FLASK_API_URL,
    features: ['Authentication', 'Patient CRUD', 'Doctor CRUD', 'Flask API Integration', 'CORS Enabled']
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
app.get('/api/doctors', authenticateToken, async (req, res) => {
  try {
    if (databaseConnected) {
      const result = await pool.query('SELECT * FROM doctors ORDER BY created_at DESC');
      res.json({
        doctors: result.rows,
        total: result.rows.length,
        source: 'PostgreSQL'
      });
    } else {
      res.json({
        doctors: fallbackDoctors,
        total: fallbackDoctors.length,
        source: 'In-memory fallback'
      });
    }
  } catch (error) {
    console.error('Get doctors error:', error);
    res.status(500).json({ error: 'Failed to get doctors' });
  }
});

app.post('/api/doctors', authenticateToken, async (req, res) => {
  try {
    const { full_name, specialization, phone, email } = req.body;
    
    if (!full_name || !specialization) {
      return res.status(400).json({ 
        error: 'Missing required fields: full_name, specialization' 
      });
    }
    
    if (databaseConnected) {
      const result = await pool.query(
        'INSERT INTO doctors (full_name, specialization, phone, email) VALUES ($1, $2, $3, $4) RETURNING *',
        [full_name, specialization, phone || null, email || null]
      );
      
      res.status(201).json({
        message: 'Doctor created successfully',
        doctor: result.rows[0],
        source: 'PostgreSQL'
      });
    } else {
      const newDoctor = {
        id: fallbackDoctors.length + 1,
        full_name: full_name,
        specialization: specialization,
        phone: phone || null,
        email: email || null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      
      fallbackDoctors.push(newDoctor);
      
      res.status(201).json({
        message: 'Doctor created successfully',
        doctor: newDoctor,
        source: 'In-memory fallback'
      });
    }
    
  } catch (error) {
    console.error('Create doctor error:', error);
    res.status(500).json({ error: 'Failed to create doctor' });
  }
});

// Flask API Integration
app.get('/api/equipment', authenticateToken, async (req, res) => {
  try {
    console.log('Fetching equipment from Flask API...');
    const response = await axios.get(`${FLASK_API_URL}/api/equipment`, { timeout: 5000 });
    
    res.json({
      equipment: response.data.equipment,
      total: response.data.equipment.length,
      source: 'Flask API',
      flask_api_url: FLASK_API_URL
    });
    
  } catch (error) {
    console.error('Flask API error:', error.message);
    res.status(500).json({ error: 'Failed to fetch equipment from Flask API' });
  }
});

// Complete system integration endpoint
app.get('/api/system/integration', authenticateToken, async (req, res) => {
  try {
    // Test PostgreSQL
    let postgresqlStatus = 'disconnected';
    let doctorCount = 0;
    
    if (databaseConnected) {
      try {
        const result = await pool.query('SELECT COUNT(*) as count FROM doctors');
        postgresqlStatus = 'connected';
        doctorCount = result.rows[0].count;
      } catch (error) {
        postgresqlStatus = 'error';
      }
    } else {
      doctorCount = fallbackDoctors.length;
    }
    
    // Test Flask API
    let flaskApiStatus = 'disconnected';
    let equipmentCount = 0;
    
    try {
      const response = await axios.get(`${FLASK_API_URL}/api/health`, { timeout: 5000 });
      flaskApiStatus = 'connected';
      
      const equipmentResponse = await axios.get(`${FLASK_API_URL}/api/equipment`, { timeout: 5000 });
      equipmentCount = equipmentResponse.data.equipment.length;
    } catch (error) {
      flaskApiStatus = 'error';
    }
    
    res.json({
      system_status: 'integrated',
      timestamp: new Date().toISOString(),
      services: {
        frontend: {
          url: 'http://localhost:3000',
          status: 'running'
        },
        backend: {
          url: 'http://localhost:5000',
          status: 'running'
        },
        postgresql: {
          status: postgresqlStatus,
          database: 'medical_imaging',
          doctor_count: doctorCount
        },
        flask_api: {
          status: flaskApiStatus,
          url: FLASK_API_URL,
          equipment_count: equipmentCount
        }
      },
      data_flow: {
        'frontend -> backend': 'working',
        'backend -> postgresql': postgresqlStatus === 'connected' ? 'working' : 'fallback',
        'backend -> flask_api': flaskApiStatus === 'connected' ? 'working' : 'error'
      }
    });
    
  } catch (error) {
    console.error('System integration error:', error);
    res.status(500).json({ error: 'Failed to check system integration' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`System Integration Backend running on port ${PORT}`);
  console.log(`Database: ${databaseConnected ? 'PostgreSQL 18 - medical_imaging' : 'In-memory fallback'}`);
  console.log(`Flask API: ${FLASK_API_URL}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`System integration: http://localhost:${PORT}/api/system/integration`);
  console.log(`Frontend URL: http://localhost:3000`);
  console.log(`Architecture: Frontend (3000) -> Backend (5000) -> PostgreSQL (5432) -> Flask API (5001)`);
});

module.exports = app;
