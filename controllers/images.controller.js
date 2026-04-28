const { Image, Study } = require('../models');
const { Op } = require('sequelize');

// Upload images to a study
const uploadStudyImages = async (req, res) => {
  try {
    const { studyId } = req.params;
    
    // Verify study exists
    const study = await Study.findByPk(studyId);
    if (!study) {
      return res.status(404).json({ error: 'Study not found' });
    }
    
    const uploadedImages = [];
    
    if (req.files && req.files.length > 0) {
      for (const file of req.files) {
        const imageData = {
          studyId,
          sequenceType: req.body.sequenceType || 'Unknown',
          fileName: file.filename,
          originalFileName: file.originalname,
          filePath: file.path,
          fileUrl: `/uploads/studies/${studyId}/${file.filename}`,
          fileSize: file.size,
          mimeType: file.mimetype,
          acquisitionDate: new Date(),
          acquisitionTime: new Date().toTimeString().split(' ')[0]
        };
        
        const image = await Image.create(imageData);
        uploadedImages.push(image);
      }
    }
    
    res.status(201).json({
      message: `${uploadedImages.length} images uploaded successfully`,
      images: uploadedImages
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Get all images for a study
const getStudyImages = async (req, res) => {
  try {
    const { studyId } = req.params;
    
    // Verify study exists
    const study = await Study.findByPk(studyId);
    if (!study) {
      return res.status(404).json({ error: 'Study not found' });
    }
    
    const images = await Image.findAll({
      where: { studyId, isDeleted: false },
      order: [['acquisitionDate', 'DESC']]
    });
    
    res.json({ images });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Get single image by ID
const getImageById = async (req, res) => {
  try {
    const { imageId } = req.params;
    
    const image = await Image.findByPk(imageId);
    
    if (!image || image.isDeleted) {
      return res.status(404).json({ error: 'Image not found' });
    }
    
    res.json({ image });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Delete image
const deleteImage = async (req, res) => {
  try {
    const { imageId } = req.params;
    
    const image = await Image.findByPk(imageId);
    
    if (!image) {
      return res.status(404).json({ error: 'Image not found' });
    }
    
    await image.update({ isDeleted: true });
    
    res.json({ message: 'Image deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = {
  uploadStudyImages,
  getStudyImages,
  getImageById,
  deleteImage
};
