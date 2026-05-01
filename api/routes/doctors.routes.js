const express = require('express');
const router = express.Router();
const {
  createDoctor,
  getDoctors,
  getDoctorById,
  updateDoctor,
  deleteDoctor,
  searchDoctors,
  getDoctorStudies
} = require('../controllers/doctors.controller');

// CRUD routes
router.post('/', createDoctor);
router.get('/', getDoctors);
router.get('/search', searchDoctors);
router.get('/:doctorId', getDoctorById);
router.put('/:doctorId', updateDoctor);
router.delete('/:doctorId', deleteDoctor);

// Nested routes
router.get('/:doctorId/studies', getDoctorStudies);

module.exports = router;
