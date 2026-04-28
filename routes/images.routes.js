const express = require('express');
const router = express.Router();
const {
  uploadStudyImages,
  getStudyImages,
  getImageById,
  deleteImage
} = require('../controllers/images.controller');

// Upload routes
router.post('/studies/:studyId/images', uploadStudyImages);

// Image CRUD routes
router.get('/studies/:studyId/images', getStudyImages);
router.get('/:imageId', getImageById);
router.delete('/:imageId', deleteImage);

module.exports = router;
