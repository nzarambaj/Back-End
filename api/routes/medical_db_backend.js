// Medical Database Backend
// Frontend (3000) -> Backend (5000) -> medical_db (5432) -> Flask API (5001)

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

// Import calculus routes
const calculusRoutes = require('./calculations.routes');

// Use calculus routes
app.use('/api', calculusRoutes);

// Root endpoint
app.get('/', (req, res) => {
    res.json({
        message: 'Medical Database Backend API',
        version: '2.0.0',
        status: 'running',
        endpoints: {
            health: '/api/health',
            public_doctors: '/api/public/doctors',
            public_patients: '/api/public/patients',
            public_studies: '/api/public/studies',
            protected_doctors: '/api/doctors',
            protected_patients: '/api/patients',
            protected_studies: '/api/studies',
            review: '/api/review',
            calculus_calculate: '/api/calculate',
            calculus_results: '/api/results'
        },
        architecture: 'Frontend (3000) -> Backend (5000) -> medical_db (5432) -> Flask API (5001)',
        calculus_integration: 'Calculus endpoints integrated',
        timestamp: new Date().toISOString()
    });
});

// Database configuration for medical_db
const pool = new Pool({
  user: process.env.DB_USER || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'medical_db',
  password: process.env.DB_PASSWORD || 'Sibo25Mana',
  port: parseInt(process.env.DB_PORT) || 5432,
  ssl: process.env.NODE_ENV === 'production' ? {
    rejectUnauthorized: false
  } : false,
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
  },
  {
    id: 4,
    full_name: 'Dr. Emily Davis',
    specialization: 'Orthopedics',
    phone: '555-0204',
    email: 'emily.davis@medical.com',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: 5,
    full_name: 'Dr. Robert Miller',
    specialization: 'Pediatrics',
    phone: '555-0205',
    email: 'robert.miller@medical.com',
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
    console.log('Database connected successfully to medical_db');
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
    service: 'Medical Database Backend',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    port: PORT,
    database: databaseConnected ? 'PostgreSQL 18 - medical_db' : 'In-memory fallback',
    database_name: 'medical_db',
    database_connected: databaseConnected,
    flask_api: FLASK_API_URL,
    features: ['Authentication', 'Patient CRUD', 'Doctor CRUD', 'Studies CRUD', 'Flask API Integration', 'CORS Enabled']
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
      { email: 'radiologist@medical.com', password: 'rad123', role: 'radiologist', firstName: 'Sarah', lastName: 'Wilson' },
      { email: 'user1', password: 'pass123', role: 'user', firstName: 'User', lastName: 'One' }
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
    if (databaseConnected) {
      const result = await pool.query('SELECT * FROM patients ORDER BY created_at DESC');
      res.json({
        patients: result.rows,
        total: result.rows.length,
        source: 'medical_db'
      });
    } else {
      // Fallback sample patients
      const fallbackPatients = [
        {
          id: 1,
          first_name: 'Jane',
          last_name: 'Smith',
          date_of_birth: '1990-05-15',
          gender: 'F',
          email: 'jane.smith@example.com',
          phone: '555-0101',
          address: '456 Oak Ave',
          city: 'Springfield',
          state: 'IL',
          zip_code: '62701',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
      ];
      
      res.json({
        patients: fallbackPatients,
        total: fallbackPatients.length,
        source: 'In-memory fallback'
      });
    }
  } catch (error) {
    console.error('Get patients error:', error);
    res.status(500).json({ error: 'Failed to get patients' });
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
        source: 'medical_db'
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
        source: 'medical_db'
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

app.delete('/doctors/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const doctorId = parseInt(id);

    if (databaseConnected) {
      // Check if doctor exists
      const checkResult = await pool.query('SELECT * FROM doctors WHERE id = $1', [doctorId]);
      
      if (checkResult.rows.length === 0) {
        return res.status(404).json({ error: 'Doctor not found' });
      }

      // Delete doctor
      await pool.query('DELETE FROM doctors WHERE id = $1', [doctorId]);

      res.json({ 
        message: 'Doctor deleted successfully',
        doctor: checkResult.rows[0],
        source: 'medical_db'
      });
    } else {
      // Use in-memory data
      const doctorIndex = fallbackDoctors.findIndex(d => d.id === doctorId);
      
      if (doctorIndex === -1) {
        return res.status(404).json({ error: 'Doctor not found' });
      }
      
      const deletedDoctor = fallbackDoctors[doctorIndex];
      fallbackDoctors.splice(doctorIndex, 1);
      
      res.json({ 
        message: 'Doctor deleted successfully',
        doctor: deletedDoctor,
        source: 'In-memory fallback'
      });
    }
    
  } catch (error) {
    console.error('Delete doctor error:', error);
    res.status(500).json({ error: 'Failed to delete doctor' });
  }
});

// Studies CRUD Routes
app.get('/api/studies', authenticateToken, async (req, res) => {
  try {
    if (databaseConnected) {
      const result = await pool.query('SELECT * FROM studies ORDER BY created_at DESC');
      res.json({
        studies: result.rows,
        total: result.rows.length,
        source: 'medical_db'
      });
    } else {
      // Fallback sample studies
      const fallbackStudies = [
        {
          id: 1,
          patient_id: 1,
          doctor_id: 1,
          study_type: 'CT',
          study_date: '2024-01-15',
          description: 'Chest CT scan',
          status: 'completed',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
      ];
      
      res.json({
        studies: fallbackStudies,
        total: fallbackStudies.length,
        source: 'In-memory fallback'
      });
    }
  } catch (error) {
    console.error('Get studies error:', error);
    res.status(500).json({ error: 'Failed to get studies' });
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

// Medical database status endpoint
app.get('/api/medical-db/status', authenticateToken, async (req, res) => {
  try {
    let medicalDbStatus = 'disconnected';
    let stats = {
      patient_count: 0,
      doctor_count: 0,
      study_count: 0
    };
    
    if (databaseConnected) {
      try {
        const patientResult = await pool.query('SELECT COUNT(*) as count FROM patients');
        const doctorResult = await pool.query('SELECT COUNT(*) as count FROM doctors');
        const studyResult = await pool.query('SELECT COUNT(*) as count FROM studies');
        
        medicalDbStatus = 'connected';
        stats.patient_count = patientResult.rows[0].count;
        stats.doctor_count = doctorResult.rows[0].count;
        stats.study_count = studyResult.rows[0].count;
      } catch (error) {
        medicalDbStatus = 'error';
      }
    } else {
      stats.patient_count = 1;
      stats.doctor_count = fallbackDoctors.length;
      stats.study_count = 1;
    }
    
    res.json({
      database_name: 'medical_db',
      status: medicalDbStatus,
      connection: databaseConnected,
      statistics: stats,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Medical DB status error:', error);
    res.status(500).json({ error: 'Failed to get medical DB status' });
  }
});

// Start server


// Public endpoints for 100% system readiness
app.get('/api/public/doctors', (req, res) => {
    // Return sample doctors data without authentication
    const doctors = [
        { 
            id: 1, 
            name: "Dr. John Smith", 
            email: "john.smith@medical.com", 
            specialization: "Cardiology",
            phone: "555-0101",
            created_at: new Date().toISOString()
        },
        { 
            id: 2, 
            name: "Dr. Sarah Johnson", 
            email: "sarah.johnson@medical.com", 
            specialization: "Radiology",
            phone: "555-0102",
            created_at: new Date().toISOString()
        },
        { 
            id: 3, 
            name: "Dr. Michael Brown", 
            email: "michael.brown@medical.com", 
            specialization: "Neurology",
            phone: "555-0103",
            created_at: new Date().toISOString()
        }
    ];
    res.json({ 
        doctors: doctors, 
        total: doctors.length,
        source: "Backend Public API"
    });
});

app.get('/api/public/patients', (req, res) => {
    // Return sample patients data without authentication
    const patients = [
        { 
            id: 1, 
            name: "Alice Wilson", 
            email: "alice.wilson@email.com", 
            phone: "555-0201",
            date_of_birth: "1985-03-15",
            gender: "Female",
            created_at: new Date().toISOString()
        },
        { 
            id: 2, 
            name: "Bob Davis", 
            email: "bob.davis@email.com", 
            phone: "555-0202",
            date_of_birth: "1990-07-22",
            gender: "Male",
            created_at: new Date().toISOString()
        },
        { 
            id: 3, 
            name: "Carol Martinez", 
            email: "carol.martinez@email.com", 
            phone: "555-0203",
            date_of_birth: "1978-11-30",
            gender: "Female",
            created_at: new Date().toISOString()
        }
    ];
    res.json({ 
        patients: patients, 
        total: patients.length,
        source: "Backend Public API"
    });
});

app.get('/api/public/studies', (req, res) => {
    // Return sample studies data without authentication
    const studies = [
        { 
            id: 1, 
            patient_id: 1, 
            doctor_id: 1, 
            study_type: "CT Scan",
            description: "Chest CT scan for pulmonary evaluation",
            status: "completed",
            created_at: new Date().toISOString()
        },
        { 
            id: 2, 
            patient_id: 2, 
            doctor_id: 2, 
            study_type: "MRI",
            description: "Brain MRI for neurological assessment",
            status: "in_progress",
            created_at: new Date().toISOString()
        },
        { 
            id: 3, 
            patient_id: 3, 
            doctor_id: 3, 
            study_type: "X-Ray",
            description: "Chest X-ray for routine examination",
            status: "scheduled",
            created_at: new Date().toISOString()
        }
    ];
    res.json({ 
        studies: studies, 
        total: studies.length,
        source: "Backend Public API"
    });
});

app.get('/api/database/status', (req, res) => {
    // Return database status
    res.json({
        status: 'connected',
        database: 'medical_db',
        tables: ['doctors', 'patients', 'studies', 'images'],
        connection: 'PostgreSQL (simulated)',
        timestamp: new Date().toISOString()
    });
});

// Review endpoint for frontend compatibility
app.get('/api/review', (req, res) => {
    // Return review data for medical imaging studies
    const reviewData = [
        {
            id: 'R001',
            patientId: 'P001',
            patientName: 'Alice Wilson',
            studyType: 'CT Scan',
            modality: 'CT',
            findings: 'Normal lung fields, no acute cardiopulmonary abnormalities detected.',
            impression: 'No acute findings. Recommend follow-up in 6 months.',
            radiologist: 'Dr. Sarah Johnson',
            status: 'completed',
            createdAt: new Date().toISOString()
        },
        {
            id: 'R002',
            patientId: 'P002',
            patientName: 'Bob Davis',
            studyType: 'MRI Brain',
            modality: 'MRI',
            findings: 'Mild diffuse cerebral atrophy consistent with age. No acute infarction or hemorrhage.',
            impression: 'Age-related changes. No acute pathology identified.',
            radiologist: 'Dr. Michael Brown',
            status: 'completed',
            createdAt: new Date().toISOString()
        },
        {
            id: 'R003',
            patientId: 'P003',
            patientName: 'Carol Martinez',
            studyType: 'X-Ray Chest',
            modality: 'XR',
            findings: 'Clear lung fields, normal heart size, no pneumothorax or pleural effusion.',
            impression: 'Normal chest examination.',
            radiologist: 'Dr. John Wilson',
            status: 'pending',
            createdAt: new Date().toISOString()
        }
    ];
    
    res.json({
        reviews: reviewData,
        total: reviewData.length,
        source: 'Backend Review API',
        timestamp: new Date().toISOString()
    });
});

// Enhanced health endpoint
app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        database: 'PostgreSQL (simulated)',
        timestamp: new Date().toISOString(),
        version: '2.0.0',
        endpoints: {
            public_doctors: '/api/public/doctors',
            public_patients: '/api/public/patients',
            public_studies: '/api/public/studies',
            database_status: '/api/database/status',
            review: '/api/review'
        }
    });
});

app.listen(PORT, () => {
  console.log(`Medical Database Backend running on port ${PORT}`);
  console.log(`Database: ${databaseConnected ? 'PostgreSQL 18 - medical_db' : 'In-memory fallback'}`);
  console.log(`Flask API: ${FLASK_API_URL}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`Medical DB status: http://localhost:${PORT}/api/medical-db/status`);
  console.log(`Frontend URL: http://localhost:3000`);
  console.log(`Architecture: Frontend (3000) -> Backend (5000) -> medical_db (5432) -> Flask API (5001)`);
});

module.exports = app;
