const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Image = sequelize.define('Image', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  imageId: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    defaultValue: () => `img_${Date.now()}`
  },
  studyId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'studies',
      key: 'id'
    }
  },
  sequenceType: {
    type: DataTypes.ENUM('T1', 'T2', 'FLAIR', 'DWI', 'ADC', 'MRA', 'MRV', 'CTA', 'Non-contrast', 'Contrast', 'Ultrasound'),
    allowNull: false
  },
  fileName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  originalFileName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  filePath: {
    type: DataTypes.STRING,
    allowNull: false
  },
  fileUrl: {
    type: DataTypes.STRING,
    allowNull: false
  },
  thumbnailUrl: {
    type: DataTypes.STRING,
    allowNull: true
  },
  fileSize: {
    type: DataTypes.BIGINT,
    allowNull: false,
    validate: {
      min: 0
    }
  },
  mimeType: {
    type: DataTypes.ENUM('application/dicom', 'image/jpeg', 'image/png', 'image/jp2'),
    allowNull: false
  },
  dimensions: {
    type: DataTypes.JSONB,
    defaultValue: {
      width: null,
      height: null,
      depth: null
    }
  },
  spacing: {
    type: DataTypes.JSONB,
    defaultValue: {
      x: null,
      y: null,
      z: null
    }
  },
  orientation: {
    type: DataTypes.ENUM('axial', 'sagittal', 'coronal', 'oblique'),
    allowNull: true
  },
  windowSettings: {
    type: DataTypes.JSONB,
    defaultValue: {
      windowCenter: null,
      windowWidth: null
    }
  },
  acquisitionDate: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW
  },
  acquisitionTime: {
    type: DataTypes.TIME,
    allowNull: false,
    defaultValue: DataTypes.NOW
  },
  dicomMetadata: {
    type: DataTypes.JSONB,
    defaultValue: {}
  },
  annotations: {
    type: DataTypes.JSONB,
    defaultValue: []
  },
  quality: {
    type: DataTypes.ENUM('good', 'fair', 'poor'),
    allowNull: false,
    defaultValue: 'good'
  },
  isDeleted: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  }
}, {
  tableName: 'images',
  timestamps: true,
  indexes: [
    {
      fields: ['studyId', 'acquisitionDate']
    },
    {
      fields: ['sequenceType']
    },
    {
      fields: ['acquisitionDate']
    },
    {
      fields: ['imageId']
    }
  ]
});

module.exports = Image;
