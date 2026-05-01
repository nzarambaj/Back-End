// Patient CRUD Backend with PostgreSQL 18 Database
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const { spawn } = require('child_process');
const path = require('path');

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

// Python database bridge
const queryDatabase = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    const pythonScript = path.join(__dirname, 'database_bridge.py');
    
    const python = spawn('python', [pythonScript, sql, JSON.stringify(params)]);
    
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
app.get('/api/health', async (req, res) => {
  try {
    const result = await queryDatabase('SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = $1', ['public']);
    
    res.json({
      status: 'healthy',
      database: 'PostgreSQL 18 (Python Bridge)',
      timestamp: new Date().toISOString(),
      server: 'Patient CRUD Backend',
      tables: result.rows[0].table_count
    });
  } catch (error) {
    console.error('Health check error:', error);
    res.json({
      status: 'healthy',
      database: 'PostgreSQL 18 (Python Bridge)',
      timestamp: new Date().toISOString(),
      server: 'Patient CRUD Backend',
      error: error.message
    });
  }
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
app.get('/api/patients', authenticateToken, async (req, res) => {
  try {
    const result = await queryDatabase(
      'SELECT id, first_name, last_name, email, phone_number, date_of_birth, gender, address, medical_history, allergies, emergency_contact, emergency_phone, created_at, updated_at FROM patients ORDER BY created_at DESC'
    );
    
    const patients = result.rows.map(patient => ({
      id: patient.id,
      firstName: patient.first_name,
      lastName: patient.last_name,
      email: patient.email,
      phoneNumber: patient.phone_number,
      dateOfBirth: patient.date_of_birth,
      gender: patient.gender,
      address: patient.address,
      medicalHistory: patient.medical_history,
      allergies: patient.allergies,
      emergencyContact: patient.emergency_contact,
      emergencyPhone: patient.emergency_phone,
      createdAt: patient.created_at,
      updatedAt: patient.updated_at
    }));

    res.json({ patients });
  } catch (error) {
    console.error('Patients error:', error);
    res.status(500).json({ error: 'Failed to fetch patients' });
  }
});

// GET single patient
app.get('/api/patients/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    
    const result = await queryDatabase(
      'SELECT id, first_name, last_name, email, phone_number, date_of_birth, gender, address, medical_history, allergies, emergency_contact, emergency_phone, created_at, updated_at FROM patients WHERE id = $1',
      [id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    const patient = result.rows[0];
    
    res.json({
      patient: {
        id: patient.id,
        firstName: patient.first_name,
        lastName: patient.last_name,
        email: patient.email,
        phoneNumber: patient.phone_number,
        dateOfBirth: patient.date_of_birth,
        gender: patient.gender,
        address: patient.address,
        medicalHistory: patient.medical_history,
        allergies: patient.allergies,
        emergencyContact: patient.emergency_contact,
        emergencyPhone: patient.emergency_phone,
        createdAt: patient.created_at,
        updatedAt: patient.updated_at
      }
    });
  } catch (error) {
    console.error('Patient error:', error);
    res.status(500).json({ error: 'Failed to fetch patient' });
  }
});

// CREATE new patient
app.post('/api/patients', authenticateToken, validatePatient, async (req, res) => {
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
    
    const patientId = generateUUID();
    const now = new Date().toISOString();
    
    // Check if email already exists
    const existingPatient = await queryDatabase(
      'SELECT id FROM patients WHERE email = $1',
      [email]
    );
    
    if (existingPatient.rows.length > 0) {
      return res.status(400).json({ error: 'Patient with this email already exists' });
    }
    
    const result = await queryDatabase(
      `INSERT INTO patients (id, first_name, last_name, email, phone_number, date_of_birth, gender, address, medical_history, allergies, emergency_contact, emergency_phone, created_at, updated_at) 
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14) RETURNING *`,
      [patientId, firstName, lastName, email, phoneNumber, dateOfBirth, gender, address, medicalHistory || null, allergies || null, emergencyContact || null, emergencyPhone || null, now, now]
    );
    
    const newPatient = result.rows[0];
    
    res.status(201).json({
      message: 'Patient created successfully',
      patient: {
        id: newPatient.id,
        firstName: newPatient.first_name,
        lastName: newPatient.last_name,
        email: newPatient.email,
        phoneNumber: newPatient.phone_number,
        dateOfBirth: newPatient.date_of_birth,
        gender: newPatient.gender,
        address: newPatient.address,
        medicalHistory: newPatient.medical_history,
        allergies: newPatient.allergies,
        emergencyContact: newPatient.emergency_contact,
        emergencyPhone: newPatient.emergency_phone,
        createdAt: newPatient.created_at,
        updatedAt: newPatient.updated_at
      }
    });
  } catch (error) {
    console.error('Create patient error:', error);
    res.status(500).json({ error: 'Failed to create patient' });
  }
});

// UPDATE patient
app.put('/api/patients/:id', authenticateToken, validatePatient, async (req, res) => {
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
    
    // Check if patient exists
    const existingPatient = await queryDatabase(
      'SELECT id FROM patients WHERE id = $1',
      [id]
    );
    
    if (existingPatient.rows.length === 0) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    // Check if email is being changed and if new email already exists
    if (email) {
      const emailCheck = await queryDatabase(
        'SELECT id FROM patients WHERE email = $1 AND id != $2',
        [email, id]
      );
      
      if (emailCheck.rows.length > 0) {
        return res.status(400).json({ error: 'Patient with this email already exists' });
      }
    }
    
    const now = new Date().toISOString();
    
    const result = await queryDatabase(
      `UPDATE patients SET first_name = $1, last_name = $2, email = $3, phone_number = $4, date_of_birth = $5, gender = $6, address = $7, medical_history = $8, allergies = $9, emergency_contact = $10, emergency_phone = $11, updated_at = $12
       WHERE id = $13 RETURNING *`,
      [firstName, lastName, email, phoneNumber, dateOfBirth, gender, address, medicalHistory || null, allergies || null, emergencyContact || null, emergencyPhone || null, now, id]
    );
    
    const updatedPatient = result.rows[0];
    
    res.json({
      message: 'Patient updated successfully',
      patient: {
        id: updatedPatient.id,
        firstName: updatedPatient.first_name,
        lastName: updatedPatient.last_name,
        email: updatedPatient.email,
        phoneNumber: updatedPatient.phone_number,
        dateOfBirth: updatedPatient.date_of_birth,
        gender: updatedPatient.gender,
        address: updatedPatient.address,
        medicalHistory: updatedPatient.medical_history,
        allergies: updatedPatient.allergies,
        emergencyContact: updatedPatient.emergency_contact,
        emergencyPhone: updatedPatient.emergency_phone,
        createdAt: updatedPatient.created_at,
        updatedAt: updatedPatient.updated_at
      }
    });
  } catch (error) {
    console.error('Update patient error:', error);
    res.status(500).json({ error: 'Failed to update patient' });
  }
});

// DELETE patient
app.delete('/api/patients/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    
    // Check if patient exists
    const existingPatient = await queryDatabase(
      'SELECT id FROM patients WHERE id = $1',
      [id]
    );
    
    if (existingPatient.rows.length === 0) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    // Check if patient has associated studies
    const studiesCheck = await queryDatabase(
      'SELECT COUNT(*) as count FROM studies WHERE patient_id = $1',
      [id]
    );
    
    if (studiesCheck.rows[0].count > 0) {
      return res.status(400).json({ 
        error: 'Cannot delete patient with associated studies',
        studyCount: studiesCheck.rows[0].count
      });
    }
    
    await queryDatabase(
      'DELETE FROM patients WHERE id = $1',
      [id]
    );
    
    res.json({
      message: 'Patient deleted successfully'
    });
  } catch (error) {
    console.error('Delete patient error:', error);
    res.status(500).json({ error: 'Failed to delete patient' });
  }
});

// Get other endpoints for completeness
app.get('/api/doctors', authenticateToken, async (req, res) => {
  try {
    const result = await queryDatabase(
      'SELECT id, first_name, last_name, email, phone_number, specialty, license_number, department, is_active, created_at, updated_at FROM doctors WHERE is_active = true ORDER BY first_name'
    );
    
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

// Start server
app.listen(PORT, () => {
  console.log(`Patient CRUD Backend Server running on port ${PORT}`);
  console.log(`Database: PostgreSQL 18 (Python Bridge)`);
  console.log(`Password: Sibo25Mana`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`Login endpoint: http://localhost:${PORT}/api/auth/login`);
  console.log(`Patient CRUD: http://localhost:${PORT}/api/patients`);
  console.log(`Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:3000'}`);
});

module.exports = app;
