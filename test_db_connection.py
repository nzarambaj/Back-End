#!/usr/bin/env python3
"""
Test PostgreSQL Database Connection
Test the database connection with the provided password
"""

import psycopg2
import os
from datetime import datetime

def test_postgresql_connection():
    """Test PostgreSQL connection with provided credentials"""
    print(" POSTGRESQL CONNECTION TEST")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Database configuration
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'medical_imaging',
        'user': 'postgres',
        'password': 'Sibo25mana'
    }
    
    print(" Database Configuration:")
    print(f"   Host: {db_config['host']}")
    print(f"   Port: {db_config['port']}")
    print(f"   Database: {db_config['database']}")
    print(f"   User: {db_config['user']}")
    print(f"   Password: ***HIDDEN***")
    
    print("\n Testing connection...")
    
    try:
        # Attempt to connect
        conn = psycopg2.connect(**db_config)
        print("   Connection: SUCCESS")
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"   PostgreSQL Version: {version[0]}")
        
        # Test database tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()
        print(f"   Tables found: {len(tables)}")
        
        if tables:
            print("   Table list:")
            for table in tables[:5]:  # Show first 5 tables
                print(f"      - {table[0]}")
            if len(tables) > 5:
                print(f"      ... and {len(tables) - 5} more")
        
        cursor.close()
        conn.close()
        
        print("\n Connection Test: PASSED")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"   Connection Error: {e}")
        print("\n Connection Test: FAILED")
        return False
    except Exception as e:
        print(f"   Error: {e}")
        print("\n Connection Test: FAILED")
        return False

def create_env_file():
    """Create a temporary .env file with correct configuration"""
    print("\n CREATING ENVIRONMENT FILE...")
    
    env_content = """# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_imaging
DB_USER=postgres
DB_PASSWORD=Sibo25mana

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_here_change_in_production
JWT_EXPIRES_IN=24h

# Server Configuration
PORT=5000
NODE_ENV=development

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
"""
    
    try:
        with open('.env_temp', 'w') as f:
            f.write(env_content)
        print("   Temporary .env file created: .env_temp")
        return True
    except Exception as e:
        print(f"   Error creating .env file: {e}")
        return False

if __name__ == "__main__":
    # Test database connection
    connection_success = test_postgresql_connection()
    
    if connection_success:
        # Create environment file
        create_env_file()
        
        print("\n NEXT STEPS:")
        print("1. Copy .env_temp to .env (if needed)")
        print("2. Restart the backend server")
        print("3. Test API endpoints")
    else:
        print("\n TROUBLESHOOTING:")
        print("1. Check if PostgreSQL is running")
        print("2. Verify database name: 'medical_imaging'")
        print("3. Verify user: 'postgres'")
        print("4. Check password: 'Sibo25mana'")
        print("5. Ensure PostgreSQL allows local connections")
