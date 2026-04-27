const express = require('express');
const router = express.Router();
const {
  createStudy,
  getStudies,
  getStudyById,
  getFullStudyDetails,
  updateStudy,
  deleteStudy,
  addStudyReport,
  getStudyReport
} = require('../controllers/studies.controller');

// CRUD routes
router.post('/', createStudy);
router.get('/', getStudies);
router.get('/:studyId', getStudyById);
router.get('/:studyId/full', getFullStudyDetails);
router.put('/:studyId', updateStudy);
router.delete('/:studyId', deleteStudy);

// Report routes
router.post('/:studyId/report', addStudyReport);
router.get('/:studyId/report', getStudyReport);

module.exports = router;
