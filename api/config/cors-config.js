// CORS Configuration for Medical Imaging Backend
// Supports Vercel, localhost, and production environments

const corsConfig = {
  // Allowed origins
  origin: function (origin, callback) {
    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) return callback(null, true);
    
    // Development origins
    const devOrigins = [
      'http://localhost:3000',
      'http://127.0.0.1:3000',
      'http://localhost:3001',
      'http://127.0.0.1:3001'
    ];
    
    // Vercel origins (regex pattern)
    const vercelPattern = /^https:\/\/.*\.vercel\.app$/;
    
    // Render origins (regex pattern)
    const renderPattern = /^https:\/\/.*\.onrender\.com$/;
    
    // Custom production origins from environment
    const prodOrigins = process.env.ALLOWED_ORIGINS 
      ? process.env.ALLOWED_ORIGINS.split(',')
      : [];
    
    // Check if origin is allowed
    if (process.env.NODE_ENV === 'development') {
      // In development, allow all origins
      return callback(null, true);
    }
    
    if (
      devOrigins.includes(origin) ||
      vercelPattern.test(origin) ||
      renderPattern.test(origin) ||
      prodOrigins.includes(origin)
    ) {
      return callback(null, true);
    }
    
    // Log blocked origins for debugging
    console.log(`CORS blocked origin: ${origin}`);
    callback(new Error('Not allowed by CORS'));
  },
  
  // Credentials
  credentials: true,
  
  // Allowed methods
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
  
  // Allowed headers
  allowedHeaders: [
    'Content-Type',
    'Authorization',
    'X-Requested-With',
    'Accept',
    'Origin',
    'Access-Control-Request-Method',
    'Access-Control-Request-Headers'
  ],
  
  // Exposed headers
  exposedHeaders: [
    'X-Total-Count',
    'X-Page-Count',
    'X-Current-Page'
  ],
  
  // Preflight options
  preflightContinue: false,
  optionsSuccessStatus: 204,
  
  // Max age for preflight cache
  maxAge: 86400, // 24 hours
  
  // Custom headers for debugging
  setHeaders: (res, path, stat) => {
    res.set('X-Backend-CORS', 'medical-imaging-backend');
    res.set('X-Timestamp', new Date().toISOString());
  }
};

module.exports = corsConfig;
