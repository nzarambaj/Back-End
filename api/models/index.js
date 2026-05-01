const Patient = require('./patient.model');
const Doctor = require('./doctor.model');
const Study = require('./study.model');
const Image = require('./image.model');
const User = require('./user.model');

// Define associations
const setupAssociations = () => {
  // Patient has many studies
  Patient.hasMany(Study, {
    foreignKey: 'patientId',
    as: 'studies',
    onDelete: 'CASCADE'
  });

  // Doctor has many studies
  Doctor.hasMany(Study, {
    foreignKey: 'doctorId',
    as: 'studies',
    onDelete: 'CASCADE'
  });

  // Study belongs to patient and doctor
  Study.belongsTo(Patient, {
    foreignKey: 'patientId',
    as: 'patient'
  });

  Study.belongsTo(Doctor, {
    foreignKey: 'doctorId',
    as: 'doctor'
  });

  // Study has many images
  Study.hasMany(Image, {
    foreignKey: 'studyId',
    as: 'images',
    onDelete: 'CASCADE'
  });

  // Image belongs to study
  Image.belongsTo(Study, {
    foreignKey: 'studyId',
    as: 'study'
  });

  // User associations (for reports)
  User.hasMany(Study, {
    foreignKey: 'report.reportedBy',
    as: 'reportedStudies',
    sourceKey: 'id'
  });

  Study.belongsTo(User, {
    foreignKey: 'report.reportedBy',
    as: 'reportingDoctor',
    targetKey: 'id'
  });
};

module.exports = {
  Patient,
  Doctor,
  Study,
  Image,
  User,
  setupAssociations
};
