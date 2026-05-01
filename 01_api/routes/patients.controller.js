const { Patient, Study, Doctor } = require('../models');
const { Op } = require('sequelize');

// Create a new patient
const createPatient = async (req, res) => {
  try {
    const patientData = req.body;
    const patient = await Patient.create(patientData);
    
    res.status(201).json({
      message: 'Patient created successfully',
      patient
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Get all patients
const getPatients = async (req, res) => {
  try {
    const patients = await Patient.findAll({
      order: [['createdAt', 'DESC']]
    });
    
    res.json({ patients });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Get patient by ID
const getPatientById = async (req, res) => {
  try {
    const { patientId } = req.params;
    
    const patient = await Patient.findByPk(patientId);
    
    if (!patient) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    res.json({ patient });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Update patient
const updatePatient = async (req, res) => {
  try {
    const { patientId } = req.params;
    const updates = req.body;
    
    const patient = await Patient.findByPk(patientId);
    
    if (!patient) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    await patient.update(updates);
    
    res.json({
      message: 'Patient updated successfully',
      patient
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Delete patient
const deletePatient = async (req, res) => {
  try {
    const { patientId } = req.params;
    
    const patient = await Patient.findByPk(patientId);
    
    if (!patient) {
      return res.status(404).json({ error: 'Patient not found' });
    }
    
    await patient.destroy();
    
    res.json({ message: 'Patient deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Search patients
const searchPatients = async (req, res) => {
  try {
    const { q } = req.query;
    
    const patients = await Patient.findAll({
      where: {
        [Op.or]: [
          { firstName: { [Op.iLike]: `%${q}%` } },
          { lastName: { [Op.iLike]: `%${q}%` } }
        ]
      },
      limit: 20
    });
    
    res.json({ patients });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = {
  createPatient,
  getPatients,
  getPatientById,
  updatePatient,
  deletePatient,
  searchPatients
};
