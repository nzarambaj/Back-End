const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

// Import database and models
const { sequelize, testConnection, initDatabase } = require('./config/database');
const { setupAssociations } = require('./models');

// Import routes
const patientRoutes = require('./routes/patients.routes');
const doctorRoutes = require('./routes/doctors.routes');
const studyRoutes = require('./routes/studies.routes');
const imageRoutes = require('./routes/images.routes');
const authRoutes = require('./routes/auth.routes');
const calculationRoutes = require('./routes/calculations.routes');

// Import middleware
const { authMiddleware } = require('./middleware/auth');

const app = express();

// Security middleware
app.use(helmet());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// CORS configuration
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// File upload middleware
app.use('/uploads', express.static('uploads'));

// Setup model associations
setupAssociations();

// Database connection and initialization
const startServer = async () => {
  try {
    // Test database connection
    await testConnection();
    
    // Initialize database (create tables)
    await initDatabase();
    
    const PORT = process.env.PORT || 5000;
    app.listen(PORT, () => {
      console.log(`🚀 Medical Imaging API running on port ${PORT}`);
      console.log(`📊 PostgreSQL database connected`);
      console.log(`🔗 Health check: http://localhost:${PORT}/api/health`);
    });
  } catch (error) {
    console.error('⚠️  Database connection failed:', error.message);
    console.log('📡 Starting server without database - read-only mode');
    const PORT = process.env.PORT || 5000;
    app.listen(PORT, () => {
      console.log(`🚀 Medical Imaging API running on port ${PORT}`);
      console.log(`🔗 Health check: http://localhost:${PORT}/api/health`);
      console.log(`⚠️  Database is not available - API endpoints requiring DB will fail`);
    });
  }
};

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/patients', authMiddleware, patientRoutes);
app.use('/api/doctors', authMiddleware, doctorRoutes);
app.use('/api/studies', authMiddleware, studyRoutes);
app.use('/api/images', authMiddleware, imageRoutes);
app.use('/api/calculate', calculationRoutes);
app.use('/api/results', calculationRoutes);

// Root endpoint for status and quick API info
app.get('/', (req, res) => {
  res.json({
    status: 'running',
    service: 'Medical Imaging API',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      api_health: '/api/health',
      auth: '/api/auth/login',
      patients: '/api/patients',
      doctors: '/api/doctors',
      studies: '/api/studies',
      images: '/api/images'
    }
  });
});

// Health check endpoints
const healthResponse = (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    database: 'PostgreSQL',
    environment: process.env.NODE_ENV || 'development'
  });
};

app.get('/health', healthResponse);
app.get('/api/health', healthResponse);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ 
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('🔄 SIGTERM received, shutting down gracefully');
  await sequelize.close();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('🔄 SIGINT received, shutting down gracefully');
  await sequelize.close();
  process.exit(0);
});

// Start the server
startServer();

module.exports = app;
