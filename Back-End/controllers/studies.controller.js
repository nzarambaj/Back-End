const { Study, Patient, Doctor, Image } = require('../models');
const { Op } = require('sequelize');

// Create a new study
const createStudy = async (req, res) => {
  try {
    const studyData = req.body;
    const study = await Study.create(studyData);
    
    res.status(201).json({
      message: 'Study created successfully',
      study
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Get all studies
const getStudies = async (req, res) => {
  try {
    const { patientId, doctorId, status } = req.query;
    
    let whereClause = {};
    
    if (patientId) whereClause.patientId = patientId;
    if (doctorId) whereClause.doctorId = doctorId;
    if (status) whereClause.status = status;
    
    const studies = await Study.findAll({
      where: whereClause,
      order: [['studyDate', 'DESC']]
    });
    
    res.json({ studies });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Get study by ID
const getStudyById = async (req, res) => {
  try {
    const { studyId } = req.params;
    
    const study = await Study.findByPk(studyId);
    
    if (!study) {
      return res.status(404).json({ error: 'Study not found' });
    }
    
    res.json({ study });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Get full study details
const getFullStudyDetails = async (req, res) => {
  try {
    const { studyId } = req.params;
    
    const study = await Study.findByPk(studyId, {
      include: [
        { model: Patient, as: 'patient' },
        { model: Doctor, as: 'doctor' },
        { model: Image, as: 'images' }
      ]
    });
    
    if (!study) {
      return res.status(404).json({ error: 'Study not found' });
    }
    
    res.json({ study });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Update study
const updateStudy = async (req, res) => {
  try {
    const { studyId } = req.params;
    const updates = req.body;
    
    const study = await Study.findByPk(studyId);
    
    if (!study) {
      return res.status(404).json({ error: 'Study not found' });
    }
    
    await study.update(updates);
    
    res.json({
      message: 'Study updated successfully',
      study
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Delete study
const deleteStudy = async (req, res) => {
  try {
    const { studyId } = req.params;
    
    const study = await Study.findByPk(studyId);
    
    if (!study) {
      return res.status(404).json({ error: 'Study not found' });
    }
    
    await study.destroy();
    
    res.json({ message: 'Study deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Add study report
const addStudyReport = async (req, res) => {
  try {
    const { studyId } = req.params;
    const { findings, impression, recommendation } = req.body;
    
    const study = await Study.findByPk(studyId);
    
    if (!study) {
      return res.status(404).json({ error: 'Study not found' });
    }
    
    await study.update({
      report: {
        findings,
        impression,
        recommendation,
        reportedDate: new Date(),
        reportStatus: 'preliminary'
      },
      status: 'reported'
    });
    
    res.json({
      message: 'Report added successfully',
      study
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Get study report
const getStudyReport = async (req, res) => {
  try {
    const { studyId } = req.params;
    
    const study = await Study.findByPk(studyId, {
      include: [
        { model: Patient, as: 'patient' },
        { model: Doctor, as: 'doctor' }
      ]
    });
    
    if (!study) {
      return res.status(404).json({ error: 'Study not found' });
    }
    
    if (!study.report) {
      return res.status(404).json({ error: 'No report found for this study' });
    }
    
    res.json({
      study: {
        studyId: study.studyId,
        accessionNumber: study.accessionNumber,
        patient: study.patient,
        doctor: study.doctor,
        modality: study.modality,
        bodyPart: study.bodyPart,
        studyDate: study.studyDate,
        report: study.report
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = {
  createStudy,
  getStudies,
  getStudyById,
  getFullStudyDetails,
  updateStudy,
  deleteStudy,
  addStudyReport,
  getStudyReport
};
