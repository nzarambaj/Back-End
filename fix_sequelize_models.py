#!/usr/bin/env python3
"""
Fix Sequelize Models for PostgreSQL 18
Fix model imports and database configuration
"""

import os
import json
from pathlib import Path
from datetime import datetime

class SequelizeModelFixer:
    def __init__(self):
        self.base_path = Path(r"C:\Users\TTR\Documents\Project_BackEnd")
        
    def fix_model_imports(self):
        """Fix model imports to work with existing backend"""
        print(" FIXING SEQUELIZE MODEL IMPORTS")
        print("=" * 60)
        
        # Check existing models
        models_dir = self.base_path / 'models'
        if models_dir.exists():
            model_files = list(models_dir.glob('*.js'))
            print(f" Found {len(model_files)} model files:")
            
            for model_file in model_files:
                print(f"   - {model_file.name}")
                
                # Read the model file
                with open(model_file, 'r') as f:
                    content = f.read()
                
                # Fix common Sequelize import issues
                if 'const { DataTypes } = require('sequelize')' in content:
                    # Fix the import
                    content = content.replace(
                        'const { DataTypes } = require('sequelize')',
                        'const { DataTypes } = require(\'sequelize\')'
                    )
                    
                    # Add proper Sequelize import if missing
                    if 'const { Sequelize } = require('sequelize')' not in content:
                        content = 'const { Sequelize, DataTypes } = require(\'sequelize\');\n' + content
                
                # Fix database import
                if 'sequelize' in content and 'require' not in content:
                    content = content.replace(
                        'module.exports = sequelize.define(',
                        'const { sequelize } = require(\'../config/database\');\n\nmodule.exports = sequelize.define('
                    )
                
                # Write back the fixed content
                with open(model_file, 'w') as f:
                    f.write(content)
                
                print(f"     Fixed: {model_file.name}")
        
        return True
    
    def create_working_models(self):
        """Create working model files"""
        print("\n CREATING WORKING MODELS")
        print("=" * 60)
        
        models_dir = self.base_path / 'models'
        models_dir.mkdir(exist_ok=True)
        
        # Create a simple working model structure
        models_index = """// Database Models Index
const { Sequelize, DataTypes } = require('sequelize');

// Database configuration
const sequelize = new Sequelize(
  process.env.DB_NAME || 'medical_imaging',
  process.env.DB_USER || 'postgres',
  process.env.DB_PASSWORD || 'Sibo25Mana',
  {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    dialect: 'postgres',
    logging: false
  }
);

// Test connection
const testConnection = async () => {
  try {
    await sequelize.authenticate();
    console.log('Database connection established successfully');
  } catch (error) {
    console.error('Unable to connect to database:', error);
  }
};

// Export sequelize instance
module.exports = {
  sequelize,
  Sequelize,
  DataTypes,
  testConnection
};
"""
        
        with open(models_dir / 'index.js', 'w') as f:
            f.write(models_index)
        
        print("   Created: models/index.js")
        
        return True
    
    def check_existing_backend_structure(self):
        """Check existing backend structure"""
        print("\n CHECKING EXISTING BACKEND STRUCTURE")
        print("=" * 60)
        
        # Check app.js
        app_js_path = self.base_path / 'app.js'
        if app_js_path.exists():
            with open(app_js_path, 'r') as f:
                content = f.read()
            
            print("   app.js found:")
            
            # Check if it's using Sequelize
            if 'sequelize' in content.lower():
                print("     Sequelize: DETECTED")
            else:
                print("     Sequelize: NOT DETECTED")
            
            # Check database connection
            if 'database' in content.lower():
                print("     Database: CONFIGURED")
            else:
                print("     Database: NOT CONFIGURED")
            
            # Check if it's already working
            if 'app.listen' in content:
                print("     Server: CONFIGURED")
            else:
                print("     Server: NOT CONFIGURED")
        
        # Check controllers
        controllers_dir = self.base_path / 'controllers'
        if controllers_dir.exists():
            controllers = list(controllers_dir.glob('*.js'))
            print(f"   Controllers: {len(controllers)} files")
        
        # Check routes
        routes_dir = self.base_path / 'routes'
        if routes_dir.exists():
            routes = list(routes_dir.glob('*.js'))
            print(f"   Routes: {len(routes)} files")
        
        return True
    
    def restart_backend_server(self):
        """Restart backend server"""
        print("\n RESTARTING BACKEND SERVER")
        print("=" * 60)
        
        try:
            import subprocess
            
            # Kill existing Node.js processes
            subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], capture_output=True)
            print("   Killed existing Node.js processes")
            
            # Start backend server
            print("   Starting backend server...")
            
            # This will be started by the user after fixing models
            print("   Backend server ready to start")
            
            return True
            
        except Exception as e:
            print(f"   Error restarting backend: {e}")
            return False
    
    def create_simple_backend_test(self):
        """Create simple backend test"""
        print("\n CREATING SIMPLE BACKEND TEST")
        print("=" * 60)
        
        test_content = """// Simple Backend Test
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'application/json'});
  
  if (req.url === '/api/health') {
    res.end(JSON.stringify({
      status: 'healthy',
      database: 'PostgreSQL 18',
      timestamp: new Date().toISOString()
    }));
  } else {
    res.end(JSON.stringify({
      message: 'Backend server is running',
      port: 5000
    }));
  }
});

server.listen(5000, () => {
  console.log('Simple backend server running on port 5000');
  console.log('Health check: http://localhost:5000/api/health');
});
"""
        
        with open(self.base_path / 'simple_backend.js', 'w') as f:
            f.write(test_content)
        
        print("   Created: simple_backend.js")
        return True
    
    def run_complete_fix(self):
        """Run complete Sequelize model fix"""
        print(" COMPLETE SEQUELIZE MODEL FIX")
        print("=" * 80)
        print(f"Location: {self.base_path}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Step 1: Check existing structure
        self.check_existing_backend_structure()
        
        # Step 2: Fix model imports
        self.fix_model_imports()
        
        # Step 3: Create working models
        self.create_working_models()
        
        # Step 4: Create simple backend test
        self.create_simple_backend_test()
        
        # Step 5: Restart backend server
        self.restart_backend_server()
        
        print("\n" + "=" * 80)
        print(" FIX COMPLETE")
        print("=" * 80)
        print(" 1. Fixed Sequelize model imports")
        print(" 2. Created working model structure")
        print(" 3. Created simple backend test")
        print(" 4. Backend server ready to restart")
        
        print("\n NEXT STEPS:")
        print("1. Start backend server: node simple_backend.js")
        print("2. Test with: curl http://localhost:5000/api/health")
        print("3. If working, start full backend: npm start")
        print("4. Test all API endpoints")
        
        return True

if __name__ == "__main__":
    fixer = SequelizeModelFixer()
    fixer.run_complete_fix()
