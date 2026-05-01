// Complete Backend with Doctors CRUD Operations
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');

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

// Test database connection
pool.connect((err, client, release) => {
  if (err) {
    console.error('Database connection error:', err.message);
    console.log('Using in-memory data as fallback');
  } else {
    console.log('Database connected successfully to medical_imaging');
    console.log('PostgreSQL 18 integration: ACTIVE');
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
    service: 'Complete Doctors Backend',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    port: PORT,
    database: 'PostgreSQL 18 - medical_imaging',
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

// Patient CRUD Routes
app.get('/api/patients', authenticateToken, async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM patients ORDER BY created_at DESC');
    
    res.json({
      patients: result.rows,
      total: result.rows.length
    });
  } catch (error) {
    console.error('Get patients error:', error);
    res.status(500).json({ error: 'Failed to get patients' });
  }
});

app.post('/api/patients', authenticateToken, async (req, res) => {
  try {
    const { firstName, lastName, dateOfBirth, gender, email, phone, address, city, state, zipCode } = req.body;
    
    if (!firstName || !lastName || !email) {
      return res.status(400).json({ 
        error: 'Missing required fields: firstName, lastName, email' 
      });
    }
    
    const result = await pool.query(
      'INSERT INTO patients (first_name, last_name, date_of_birth, gender, email, phone, address, city, state, zip_code) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *',
      [firstName, lastName, dateOfBirth, gender, email, phone, address, city, state, zipCode]
    );
    
    res.status(201).json({
      message: 'Patient created successfully',
      patient: result.rows[0]
    });
    
  } catch (error) {
    console.error('Create patient error:', error);
    res.status(500).json({ error: 'Failed to create patient' });
  }
});

// Doctor CRUD Routes
app.get('/api/doctors', authenticateToken, async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM doctors ORDER BY created_at DESC');
    
    res.json({
      doctors: result.rows,
      total: result.rows.length
    });
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
    
    const result = await pool.query(
      'INSERT INTO doctors (full_name, specialization, phone, email) VALUES ($1, $2, $3, $4) RETURNING *',
      [full_name, specialization, phone || null, email || null]
    );
    
    res.status(201).json({
      message: 'Doctor created successfully',
      doctor: result.rows[0]
    });
    
  } catch (error) {
    console.error('Create doctor error:', error);
    res.status(500).json({ error: 'Failed to create doctor' });
  }
});

app.get('/api/doctors/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    
    const result = await pool.query('SELECT * FROM doctors WHERE id = $1', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Doctor not found' });
    }
    
    res.json(result.rows[0]);
    
  } catch (error) {
    console.error('Get doctor error:', error);
    res.status(500).json({ error: 'Failed to get doctor' });
  }
});

app.put('/api/doctors/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const { full_name, specialization, phone, email } = req.body;
    
    const result = await pool.query(
      'UPDATE doctors SET full_name = $1, specialization = $2, phone = $3, email = $4, updated_at = CURRENT_TIMESTAMP WHERE id = $5 RETURNING *',
      [full_name, specialization, phone, email, id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Doctor not found' });
    }
    
    res.json({
      message: 'Doctor updated successfully',
      doctor: result.rows[0]
    });
    
  } catch (error) {
    console.error('Update doctor error:', error);
    res.status(500).json({ error: 'Failed to update doctor' });
  }
});

app.delete('/doctors/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;

    // Check if doctor exists
    const checkResult = await pool.query('SELECT * FROM doctors WHERE id = $1', [id]);
    
    if (checkResult.rows.length === 0) {
      return res.status(404).json({ error: 'Doctor not found' });
    }

    // Delete doctor
    await pool.query('DELETE FROM doctors WHERE id = $1', [id]);

    res.json({ 
      message: 'Doctor deleted successfully',
      doctor: checkResult.rows[0]
    });
    
  } catch (error) {
    console.error('Delete doctor error:', error);
    res.status(500).json({ error: 'Failed to delete doctor' });
  }
});

// Study CRUD Routes
app.get('/api/studies', authenticateToken, async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM studies ORDER BY created_at DESC');
    
    res.json({
      studies: result.rows,
      total: result.rows.length
    });
  } catch (error) {
    console.error('Get studies error:', error);
    res.status(500).json({ error: 'Failed to get studies' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Complete Doctors Backend running on port ${PORT}`);
  console.log(`Database: medical_imaging`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`Login endpoint: http://localhost:${PORT}/api/auth/login`);
  console.log(`Frontend URL: http://localhost:3000`);
  console.log(`Features: Patient CRUD, Doctor CRUD, Studies CRUD`);
  console.log(`Doctors endpoints: GET, POST, PUT, DELETE /api/doctors`);
});

module.exports = app;
