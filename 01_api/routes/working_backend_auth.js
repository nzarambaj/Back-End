// Working Backend Server with Authentication and PostgreSQL 18
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const { Pool } = require('pg');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());

// PostgreSQL 18 Connection
const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'medical_imaging',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'Sibo25Mana',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Test database connection
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('Database connection error:', err);
  } else {
    console.log('PostgreSQL 18 connected successfully');
    console.log('Database:', res.rows[0].now);
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

// Helper function to query database
const queryDatabase = async (query, params = []) => {
  const client = await pool.connect();
  try {
    const result = await client.query(query, params);
    return result;
  } finally {
    client.release();
  }
};

// Routes

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    database: 'PostgreSQL 18',
    timestamp: new Date().toISOString(),
    server: 'Express.js with Authentication'
  });
});

// Login
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }

    // For demo purposes, accept test credentials
    // In production, this would query the database
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
app.get('/api/patients', authenticateToken, async (req, res) => {
  try {
    const result = await queryDatabase('SELECT * FROM patients ORDER BY created_at DESC');
    
    const patients = result.rows.map(patient => ({
      id: patient.id,
      firstName: patient.first_name,
      lastName: patient.last_name,
      email: patient.email,
      phoneNumber: patient.phone_number,
      dateOfBirth: patient.date_of_birth,
      gender: patient.gender,
      address: patient.address,
      createdAt: patient.created_at,
      updatedAt: patient.updated_at
    }));

    res.json({ patients });
  } catch (error) {
    console.error('Patients error:', error);
    res.status(500).json({ error: 'Failed to fetch patients' });
  }
});

// Get doctors
app.get('/api/doctors', authenticateToken, async (req, res) => {
  try {
    const result = await queryDatabase('SELECT * FROM doctors WHERE is_active = true ORDER BY first_name');
    
    const doctors = result.rows.map(doctor => ({
      id: doctor.id,
      firstName: doctor.first_name,
      lastName: doctor.last_name,
      email: doctor.email,
      phoneNumber: doctor.phone_number,
      specialty: doctor.specialty,
      licenseNumber: doctor.license_number,
      department: doctor.department,
      isActive: doctor.is_active,
      createdAt: doctor.created_at,
      updatedAt: doctor.updated_at
    }));

    res.json({ doctors });
  } catch (error) {
    console.error('Doctors error:', error);
    res.status(500).json({ error: 'Failed to fetch doctors' });
  }
});

// Get studies
app.get('/api/studies', authenticateToken, async (req, res) => {
  try {
    const result = await queryDatabase(`
      SELECT s.*, p.first_name as patient_first_name, p.last_name as patient_last_name,
             d.first_name as doctor_first_name, d.last_name as doctor_last_name
      FROM studies s
      LEFT JOIN patients p ON s.patient_id = p.id
      LEFT JOIN doctors d ON s.doctor_id = d.id
      ORDER BY s.study_date DESC
    `);
    
    const studies = result.rows.map(study => ({
      id: study.id,
      patientId: study.patient_id,
      doctorId: study.doctor_id,
      patientName: `${study.patient_first_name || ''} ${study.patient_last_name || ''}`.trim(),
      doctorName: `${study.doctor_first_name || ''} ${study.doctor_last_name || ''}`.trim(),
      modality: study.modality,
      bodyPart: study.body_part,
      studyDate: study.study_date,
      studyTime: study.study_time,
      status: study.status,
      priority: study.priority,
      indication: study.indication,
      contrastUsed: study.contrast_used,
      contrastType: study.contrast_type,
      report: study.report,
      accessionNumber: study.accession_number,
      createdAt: study.created_at,
      updatedAt: study.updated_at
    }));

    res.json({ studies });
  } catch (error) {
    console.error('Studies error:', error);
    res.status(500).json({ error: 'Failed to fetch studies' });
  }
});

// Get images
app.get('/api/images', authenticateToken, async (req, res) => {
  try {
    const result = await queryDatabase('SELECT * FROM images ORDER BY upload_date DESC');
    
    const images = result.rows.map(image => ({
      id: image.id,
      studyId: image.study_id,
      filename: image.filename,
      originalName: image.original_name,
      mimeType: image.mime_type,
      size: image.size,
      path: image.path,
      thumbnailPath: image.thumbnail_path,
      uploadDate: image.upload_date,
      processed: image.processed,
      createdAt: image.created_at,
      updatedAt: image.updated_at
    }));

    res.json({ images });
  } catch (error) {
    console.error('Images error:', error);
    res.status(500).json({ error: 'Failed to fetch images' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Medical Imaging Backend Server running on port ${PORT}`);
  console.log(`Database: PostgreSQL 18`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`Login endpoint: http://localhost:${PORT}/api/auth/login`);
  console.log(`Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:3000'}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  await pool.end();
  console.log('Database pool closed');
  process.exit(0);
});
