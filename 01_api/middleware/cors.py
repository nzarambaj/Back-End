"""
CORS Middleware for API
Professional 4-Folder Web Backend Organization
"""

def cors_middleware(app):
    """Configure CORS for the Express application"""
    cors = require('cors')
    
    cors_options = {
        origin: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5001",
            "http://127.0.0.1:5001"
        ],
        methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allowedHeaders: ["Content-Type", "Authorization", "X-Requested-With"],
        credentials: true
    }
    
    return cors(cors_options)
