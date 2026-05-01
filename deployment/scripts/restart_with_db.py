#!/usr/bin/env python3
"""
Restart Backend with PostgreSQL Database Configuration
Sets environment variables and restarts the backend server
"""

import os
import subprocess
import sys
from pathlib import Path

def set_environment_and_restart():
    """Set environment variables and restart backend server"""
    print(" RESTARTING BACKEND WITH POSTGRESQL CONFIGURATION")
    print("=" * 60)
    
    # Set environment variables
    env_vars = {
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'medical_imaging',
        'DB_USER': 'postgres',
        'DB_PASSWORD': 'Sibo25mana',
        'JWT_SECRET': 'your_super_secret_jwt_key_here_change_in_production',
        'JWT_EXPIRES_IN': '24h',
        'PORT': '5000',
        'NODE_ENV': 'development',
        'FRONTEND_URL': 'http://localhost:3000'
    }
    
    print(" Setting environment variables:")
    for key, value in env_vars.items():
        os.environ[key] = value
        if key == 'DB_PASSWORD':
            print(f"   {key}: ***HIDDEN***")
        else:
            print(f"   {key}: {value}")
    
    print("\n Killing existing backend processes...")
    try:
        # Kill existing Node.js processes on port 5000
        subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], capture_output=True)
        print("   Node.js processes killed")
    except:
        print("   No Node.js processes to kill")
    
    print("\n Starting backend server...")
    try:
        # Start the backend server with environment variables
        result = subprocess.run(['npm', 'start'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   Backend server started successfully!")
            print("   Server running on: http://localhost:5000")
        else:
            print(f"   Error starting backend: {result.stderr}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n Database connection test...")
    try:
        import requests
        response = requests.get('http://localhost:5000/api/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Database Status: {data.get('database', 'Unknown')}")
            print(f"   Server Status: {data.get('status', 'Unknown')}")
        else:
            print(f"   Health check failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"   Health check error: {e}")

if __name__ == "__main__":
    set_environment_and_restart()
