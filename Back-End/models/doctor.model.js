const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Doctor = sequelize.define('Doctor', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  firstName: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: true,
      len: [1, 100]
    }
  },
  lastName: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: true,
      len: [1, 100]
    }
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true,
      notEmpty: true
    }
  },
  phoneNumber: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: true,
      is: /^[+]?[\d\s\-\(\)]+$/
    }
  },
  specialty: {
    type: DataTypes.ENUM(
      'Radiology',
      'Cardiology', 
      'Neurology',
      'Oncology',
      'Orthopedics',
      'Pediatrics',
      'General Practice',
      'Emergency Medicine',
      'Surgery',
      'Anesthesiology',
      'Pathology',
      'Psychiatry'
    ),
    allowNull: false
  },
  licenseNumber: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      notEmpty: true
    }
  },
  department: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: true
    }
  },
  qualifications: {
    type: DataTypes.JSONB,
    defaultValue: []
  },
  experience: {
    type: DataTypes.INTEGER,
    allowNull: false,
    validate: {
      min: 0,
      max: 70
    }
  },
  isActive: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  },
  schedule: {
    type: DataTypes.JSONB,
    defaultValue: {}
  }
}, {
  tableName: 'doctors',
  timestamps: true,
  indexes: [
    {
      type: 'FULLTEXT',
      fields: ['firstName', 'lastName', 'specialty']
    },
    {
      fields: ['email']
    },
    {
      fields: ['licenseNumber']
    }
  ]
});

// Virtual getter for full name
Doctor.prototype.getFullName = function() {
  return `${this.firstName} ${this.lastName}`;
};

module.exports = Doctor;
