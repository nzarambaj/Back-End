const express = require('express');
const router = express.Router();
const {
  createPatient,
  getPatients,
  getPatientById,
  updatePatient,
  deletePatient,
  searchPatients
} = require('../controllers/patients.controller');

// CRUD routes
router.post('/', createPatient);
router.get('/', getPatients);
router.get('/search', searchPatients);
router.get('/:patientId', getPatientById);
router.put('/:patientId', updatePatient);
router.delete('/:patientId', deletePatient);

module.exports = router;
