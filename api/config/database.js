// PostgreSQL Database Configuration
const { config } = require('dotenv');
config();

module.exports = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'medical_imaging',
  username: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'Sibo25Mana',
  
  // Connection pool settings
  pool: {
    max: 20,
    min: 5,
    acquire: 30000,
    idle: 10000
  },
  
  // Sequelize options
  dialect: 'postgres',
  logging: process.env.NODE_ENV === 'development' ? console.log : false,
  
  // SSL configuration (disable for local development)
  dialectOptions: {
    ssl: process.env.NODE_ENV === 'production' ? {
      require: true,
      rejectUnauthorized: false
    } : false
  }
};
