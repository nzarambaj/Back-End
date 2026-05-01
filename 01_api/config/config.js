// Main Application Configuration
const { config } = require('dotenv');
config();

module.exports = {
  // Server configuration
  port: process.env.PORT || 5000,
  nodeEnv: process.env.NODE_ENV || 'development',
  
  // Frontend URL for CORS
  frontendUrl: process.env.FRONTEND_URL || 'http://localhost:3000',
  
  // JWT configuration
  jwt: {
    secret: process.env.JWT_SECRET || 'your_super_secret_jwt_key_here_change_in_production',
    expiresIn: process.env.JWT_EXPIRES_IN || '24h'
  },
  
  // File upload configuration
  upload: {
    maxSize: parseInt(process.env.MAX_FILE_SIZE) || 104857600, // 100MB
    directory: process.env.UPLOAD_DIR || './uploads'
  },
  
  // DICOM configuration
  dicom: {
    storagePath: process.env.DICOM_STORAGE_PATH || './uploads/dicom',
    thumbnailSize: parseInt(process.env.THUMBNAIL_SIZE) || 200
  }
};
