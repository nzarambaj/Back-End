// PostgreSQL Database Configuration
const { Sequelize } = require('sequelize');
const { config } = require('dotenv');
config();

// Database configuration
const dbConfig = {
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

// Create Sequelize instance
const sequelize = new Sequelize(
  dbConfig.database,
  dbConfig.username,
  dbConfig.password,
  {
    host: dbConfig.host,
    port: dbConfig.port,
    dialect: dbConfig.dialect,
    pool: dbConfig.pool,
    logging: dbConfig.logging,
    dialectOptions: dbConfig.dialectOptions
  }
);

module.exports = {
  sequelize,
  dbConfig
};
