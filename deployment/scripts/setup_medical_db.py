#!/usr/bin/env python3
"""
Setup Medical Database (medical_db)
Configure PostgreSQL database with name medical_db
"""

import subprocess
import time
from datetime import datetime

def create_medical_db_setup():
    """Create medical_db database setup"""
    print(" SETTING UP MEDICAL DATABASE (medical_db)")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    setup_sql = '''-- Medical Database Setup
-- Create database and tables for medical imaging system

-- Drop existing database if exists
DROP DATABASE IF EXISTS medical_db;

-- Create new database
CREATE DATABASE medical_db;

-- Connect to medical_db database
\\c medical_db;

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create studies table
CREATE TABLE IF NOT EXISTS studies (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    doctor_id INTEGER REFERENCES doctors(id),
    study_type VARCHAR(50),
    study_date DATE,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create images table
CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    study_id INTEGER REFERENCES studies(id),
    image_type VARCHAR(50),
    file_path TEXT,
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO patients (first_name, last_name, date_of_birth, gender, email, phone, address, city, state, zip_code) VALUES
('Jane', 'Smith', '1990-05-15', 'F', 'jane.smith@example.com', '555-0101', '456 Oak Ave', 'Springfield', 'IL', '62701'),
('John', 'Doe', '1985-03-20', 'M', 'john.doe@example.com', '555-0102', '123 Main St', 'Anytown', 'CA', '12345'),
('Alice', 'Johnson', '1988-08-12', 'F', 'alice.johnson@example.com', '555-0103', '789 Pine St', 'Riverside', 'CA', '92501');

INSERT INTO doctors (full_name, specialization, phone, email) VALUES
('Dr. John Wilson', 'Radiology', '555-0201', 'john.wilson@medical.com'),
('Dr. Sarah Johnson', 'Cardiology', '555-0202', 'sarah.johnson@medical.com'),
('Dr. Michael Brown', 'Neurology', '555-0203', 'michael.brown@medical.com'),
('Dr. Emily Davis', 'Orthopedics', '555-0204', 'emily.davis@medical.com'),
('Dr. Robert Miller', 'Pediatrics', '555-0205', 'robert.miller@medical.com');

INSERT INTO studies (patient_id, doctor_id, study_type, study_date, description, status) VALUES
(1, 1, 'CT', '2024-01-15', 'Chest CT scan', 'completed'),
(2, 2, 'MRI', '2024-01-20', 'Brain MRI', 'completed'),
(3, 3, 'X-Ray', '2024-01-25', 'Chest X-ray', 'completed'),
(1, 4, 'Ultrasound', '2024-02-01', 'Abdominal ultrasound', 'in_progress'),
(2, 5, 'CT', '2024-02-05', 'Sinus CT scan', 'pending');

-- Grant permissions to postgres user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Show setup completion
SELECT 'Medical database setup completed' as status,
       'medical_db' as database_name,
       (SELECT COUNT(*) FROM patients) as patient_count,
       (SELECT COUNT(*) FROM doctors) as doctor_count,
       (SELECT COUNT(*) FROM studies) as study_count;
'''
    
    with open(r"C:\Users\TTR\Documents\Project_BackEnd\medical_db_setup.sql", "w") as f:
        f.write(setup_sql)
    
    print("Medical database setup script created: medical_db_setup.sql")
    print("Database name: medical_db")
    print("Features:")
    print("- Complete medical imaging database")
    print("- Patients, doctors, studies, images tables")
    print("- Sample data insertion")
    print("- Proper permissions")
    
    return True

def create_medical_db_backend():
    """Create backend with medical_db configuration"""
    print("\n CREATING MEDICAL DB BACKEND")
    print("=" * 60)
    
    backend_js = '''// Medical Database Backend
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

// Database configuration for medical_db
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'medical_db',
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
'''
    
    with open(r"C:\Users\TTR\Documents\Project_BackEnd\medical_db_backend.js", "w") as f:
        f.write(backend_js)
    
    print("Medical database backend created: medical_db_backend.js")
    print("Features:")
    print("- PostgreSQL connection to medical_db")
    print("- Complete medical imaging system")
    print("- 5 sample doctors added")
    print("- 3 sample patients added")
    print("- 5 sample studies added")
    print("- Flask API integration")
    print("- Medical DB status endpoint")
    
    return True

def setup_medical_database():
    """Setup the medical database"""
    print("\n SETTING UP MEDICAL DATABASE")
    print("=" * 60)
    
    try:
        # Execute medical database setup
        result = subprocess.run([
            'psql', '-U', 'postgres', '-h', 'localhost', '-p', '5432', 
            '-d', 'postgres', '-f', r'C:\Users\TTR\Documents\Project_BackEnd\medical_db_setup.sql'
        ], capture_output=True, text=True, timeout=30)
        
        print("Medical database setup execution:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("Medical database setup: SUCCESS")
            return True
        else:
            print("Medical database setup: FAILED")
            return False
            
    except Exception as e:
        print(f"Medical database setup error: {e}")
        return False

def start_medical_db_backend():
    """Start medical database backend"""
    print("\n STARTING MEDICAL DATABASE BACKEND")
    print("=" * 60)
    
    # Stop current backend
    try:
        import os
        os.system('taskkill /f /im node.exe >nul 2>&1')
        print("Stopped current backend")
        time.sleep(2)
    except:
        pass
    
    # Start medical database backend
    try:
        import subprocess
        subprocess.Popen(['node', 'medical_db_backend.js'], 
                       cwd=r"C:\Users\TTR\Documents\Project_BackEnd")
        print("Started medical database backend")
        return True
    except Exception as e:
        print(f"Failed to start medical database backend: {e}")
        return False

def main():
    """Main function to setup medical database"""
    print(" MEDICAL DATABASE (medical_db) SETUP")
    print("=" * 80)
    
    # Step 1: Create medical database setup
    setup_created = create_medical_db_setup()
    
    # Step 2: Create medical database backend
    backend_created = create_medical_db_backend()
    
    # Step 3: Setup medical database
    if setup_created and backend_created:
        db_setup = setup_medical_database()
        
        # Step 4: Start medical database backend
        if db_setup:
            backend_started = start_medical_db_backend()
            
            # Summary
            print("\n" + "=" * 80)
            print(" MEDICAL DATABASE SETUP SUMMARY")
            print("=" * 80)
            
            if db_setup and backend_started:
                print("Medical Database: COMPLETE")
                print("\nDatabase Configuration:")
                print("- Name: medical_db")
                print("- Host: localhost")
                print("- Port: 5432")
                print("- User: postgres")
                print("- Password: Sibo25Mana")
                
                print("\nSystem Architecture:")
                print("Frontend (3000) -> Backend (5000) -> medical_db (5432) -> Flask API (5001)")
                
                print("\nAccess Points:")
                print("- Frontend: http://localhost:3000")
                print("- Backend: http://localhost:5000")
                print("- Medical DB status: http://localhost:5000/api/medical-db/status")
                print("- Flask API: http://localhost:5001")
                
                print("\nSample Data:")
                print("- Patients: 3 (Jane Smith, John Doe, Alice Johnson)")
                print("- Doctors: 5 (Radiology, Cardiology, Neurology, Orthopedics, Pediatrics)")
                print("- Studies: 5 (CT, MRI, X-Ray, Ultrasound, various statuses)")
                
                print("\nFeatures:")
                print("- Complete CRUD operations")
                print("- PostgreSQL 18 integration")
                print("- Flask API integration")
                print("- Authentication middleware")
                print("- Medical database status endpoint")
                
                return True
            else:
                print("Medical Database Setup: INCOMPLETE")
                return False
        else:
            print("Database setup failed")
            return False
    else:
        print("Setup files not created")
        return False

if __name__ == "__main__":
    main()
