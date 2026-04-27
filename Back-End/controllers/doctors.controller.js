const { Doctor, Study } = require('../models');
const { Op } = require('sequelize');

// Create a new doctor
const createDoctor = async (req, res) => {
  try {
    const doctorData = req.body;
    const doctor = await Doctor.create(doctorData);
    
    res.status(201).json({
      message: 'Doctor created successfully',
      doctor
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Get all doctors
const getDoctors = async (req, res) => {
  try {
    const doctors = await Doctor.findAll({
      where: { isActive: true },
      order: [['firstName', 'ASC']]
    });
    
    res.json({ doctors });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Get doctor by ID
const getDoctorById = async (req, res) => {
  try {
    const { doctorId } = req.params;
    
    const doctor = await Doctor.findByPk(doctorId);
    
    if (!doctor) {
      return res.status(404).json({ error: 'Doctor not found' });
    }
    
    res.json({ doctor });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Update doctor
const updateDoctor = async (req, res) => {
  try {
    const { doctorId } = req.params;
    const updates = req.body;
    
    const doctor = await Doctor.findByPk(doctorId);
    
    if (!doctor) {
      return res.status(404).json({ error: 'Doctor not found' });
    }
    
    await doctor.update(updates);
    
    res.json({
      message: 'Doctor updated successfully',
      doctor
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Delete doctor
const deleteDoctor = async (req, res) => {
  try {
    const { doctorId } = req.params;
    
    const doctor = await Doctor.findByPk(doctorId);
    
    if (!doctor) {
      return res.status(404).json({ error: 'Doctor not found' });
    }
    
    await doctor.update({ isActive: false });
    
    res.json({ message: 'Doctor deactivated successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Search doctors
const searchDoctors = async (req, res) => {
  try {
    const { q } = req.query;
    
    const doctors = await Doctor.findAll({
      where: {
        [Op.or]: [
          { firstName: { [Op.iLike]: `%${q}%` } },
          { lastName: { [Op.iLike]: `%${q}%` } },
          { specialty: { [Op.iLike]: `%${q}%` } }
        ]
      },
      limit: 20
    });
    
    res.json({ doctors });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Get doctor's studies
const getDoctorStudies = async (req, res) => {
  try {
    const { doctorId } = req.params;
    
    const studies = await Study.findAll({
      where: { doctorId },
      order: [['studyDate', 'DESC']]
    });
    
    res.json({ studies });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = {
  createDoctor,
  getDoctors,
  getDoctorById,
  updateDoctor,
  deleteDoctor,
  searchDoctors,
  getDoctorStudies
};
