const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Patient = sequelize.define('Patient', {
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
  dateOfBirth: {
    type: DataTypes.DATEONLY,
    allowNull: false,
    validate: {
      isDate: true,
      isBefore: new Date().toISOString().split('T')[0]
    }
  },
  gender: {
    type: DataTypes.ENUM('male', 'female', 'other'),
    allowNull: false
  },
  phoneNumber: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: true,
      is: /^[+]?[\d\s\-\(\)]+$/
    }
  },
  email: {
    type: DataTypes.STRING,
    allowNull: true,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  address: {
    type: DataTypes.JSONB,
    defaultValue: {
      street: '',
      city: '',
      state: '',
      zipCode: '',
      country: ''
    }
  },
  medicalHistory: {
    type: DataTypes.JSONB,
    defaultValue: {
      allergies: [],
      medications: [],
      conditions: []
    }
  },
  emergencyContact: {
    type: DataTypes.JSONB,
    defaultValue: {
      name: '',
      relationship: '',
      phoneNumber: ''
    }
  }
}, {
  tableName: 'patients',
  timestamps: true,
  indexes: [
    {
      type: 'FULLTEXT',
      fields: ['firstName', 'lastName']
    },
    {
      fields: ['email']
    }
  ]
});

// Virtual getter for full name
Patient.prototype.getFullName = function() {
  return `${this.firstName} ${this.lastName}`;
};

module.exports = Patient;
