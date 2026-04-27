const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Study = sequelize.define('Study', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  studyId: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    defaultValue: () => `study_${Date.now()}`
  },
  patientId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'patients',
      key: 'id'
    }
  },
  doctorId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'doctors',
      key: 'id'
    }
  },
  modality: {
    type: DataTypes.ENUM('MRI', 'CT', 'X-Ray', 'Ultrasound', 'PET', 'SPECT', 'Mammography'),
    allowNull: false
  },
  bodyPart: {
    type: DataTypes.ENUM(
      'Brain', 'Chest', 'Abdomen', 'Pelvis', 'Spine', 'Extremities',
      'Head', 'Neck', 'Heart', 'Lungs', 'Liver', 'Kidneys', 'Pancreas',
      'Spleen', 'Gallbladder', 'Bladder', 'Uterus', 'Prostate', 'Thyroid'
    ),
    allowNull: false
  },
  studyDate: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW
  },
  studyTime: {
    type: DataTypes.TIME,
    allowNull: false,
    defaultValue: DataTypes.NOW
  },
  status: {
    type: DataTypes.ENUM('scheduled', 'in-progress', 'completed', 'cancelled', 'reported'),
    allowNull: false,
    defaultValue: 'scheduled'
  },
  priority: {
    type: DataTypes.ENUM('routine', 'urgent', 'stat'),
    allowNull: false,
    defaultValue: 'routine'
  },
  indication: {
    type: DataTypes.TEXT,
    allowNull: false,
    validate: {
      notEmpty: true
    }
  },
  contrastUsed: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  },
  contrastType: {
    type: DataTypes.ENUM('iodinated', 'gadolinium', 'barium'),
    allowNull: true
  },
  report: {
    type: DataTypes.JSONB,
    defaultValue: {
      findings: '',
      impression: '',
      recommendation: '',
      reportedBy: null,
      reportDate: null,
      reportStatus: 'pending'
    }
  },
  accessionNumber: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    defaultValue: () => {
      const year = new Date().getFullYear();
      const random = Math.floor(Math.random() * 100000).toString().padStart(5, '0');
      return `ACC${year}${random}`;
    }
  },
  dicomData: {
    type: DataTypes.JSONB,
    defaultValue: {}
  }
}, {
  tableName: 'studies',
  timestamps: true,
  indexes: [
    {
      fields: ['patientId', 'studyDate']
    },
    {
      fields: ['doctorId', 'studyDate']
    },
    {
      fields: ['status']
    },
    {
      fields: ['modality']
    },
    {
      fields: ['studyDate']
    },
    {
      fields: ['accessionNumber']
    }
  ]
});

module.exports = Study;
