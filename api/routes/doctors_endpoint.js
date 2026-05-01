// Doctors CRUD Endpoint
// Complete doctors operations with PostgreSQL integration
const express = require('express');
const { Pool } = require('pg');
const jwt = require('jsonwebtoken');

// Database configuration
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'medical_imaging',
  password: 'Sibo25Mana',
  port: 5432,
});

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, 'your_super_secret_jwt_key_here_change_in_production', (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};

// Create doctors endpoint
app.post('/api/doctors', authenticateToken, async (req, res) => {
  try {
    const { full_name, specialization, phone, email } = req.body;
    
    // Validation
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

// Get all doctors
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

// Get doctor by ID
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

// Update doctor
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

// Delete doctor
app.delete('/api/doctors/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    
    const result = await pool.query('DELETE FROM doctors WHERE id = $1 RETURNING *', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Doctor not found' });
    }
    
    res.json({
      message: 'Doctor deleted successfully',
      doctor: result.rows[0]
    });
    
  } catch (error) {
    console.error('Delete doctor error:', error);
    res.status(500).json({ error: 'Failed to delete doctor' });
  }
});

// Search doctors by specialization
app.get('/api/doctors/specialization/:spec', authenticateToken, async (req, res) => {
  try {
    const { spec } = req.params;
    
    const result = await pool.query(
      'SELECT * FROM doctors WHERE specialization ILIKE $1 ORDER BY full_name',
      [`%${spec}%`]
    );
    
    res.json({
      doctors: result.rows,
      specialization: spec,
      total: result.rows.length
    });
    
  } catch (error) {
    console.error('Search doctors error:', error);
    res.status(500).json({ error: 'Failed to search doctors' });
  }
});

module.exports = {
  createDoctors: app,
  authenticateToken
};
