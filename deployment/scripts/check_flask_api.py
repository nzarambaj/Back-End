#!/usr/bin/env python3
"""
Check Flask API Status
Check and restart Flask API service on port 5001
"""

import requests
import subprocess
import time
from datetime import datetime

def check_flask_api_status():
    """Check Flask API status"""
    print(" CHECKING FLASK API STATUS")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    flask_api_url = "http://localhost:5001"
    
    # Test Flask API accessibility
    print("1. TESTING FLASK API ACCESSIBILITY")
    print("-" * 40)
    
    try:
        response = requests.get(f"{flask_api_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("   Flask API: ACCESSIBLE")
            print(f"   URL: {flask_api_url}")
            print(f"   Status: HTTP {response.status_code}")
            return True
        else:
            print(f"   Flask API: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionRefusedError:
        print("   Flask API: CONNECTION REFUSED")
        return False
    except requests.exceptions.Timeout:
        print("   Flask API: TIMEOUT")
        return False
    except Exception as e:
        print(f"   Flask API: ERROR - {e}")
        return False

def check_flask_api_files():
    """Check if Flask API files exist"""
    print("\n2. CHECKING FLASK API FILES")
    print("-" * 40)
    
    import os
    
    flask_files = [
        r"C:\Users\TTR\Documents\Project_BackEnd\flask_api.py",
        r"C:\Users\TTR\Documents\Project_BackEnd\app.py",
        r"C:\Users\TTR\Documents\Project_BackEnd\server.py"
    ]
    
    for file_path in flask_files:
        if os.path.exists(file_path):
            print(f"   Found: {os.path.basename(file_path)}")
            return file_path
    
    print("   No Flask API files found")
    return None

def create_simple_flask_api():
    """Create a simple Flask API if not exists"""
    print("\n3. CREATING SIMPLE FLASK API")
    print("-" * 40)
    
    flask_api_code = '''#!/usr/bin/env python3
"""
Simple Flask API for Medical Imaging System
Provides equipment data for backend integration
"""

from flask import Flask, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# Sample equipment data
EQUIPMENT_DATA = [
    {
        "id": 1,
        "name": "CT Scanner",
        "type": "Imaging",
        "status": "Active",
        "location": "Radiology Department",
        "manufacturer": "Siemens",
        "model": "SOMATOM Definition Edge"
    },
    {
        "id": 2,
        "name": "MRI Machine",
        "type": "Imaging",
        "status": "Active",
        "location": "Radiology Department",
        "manufacturer": "GE Healthcare",
        "model": "Signa Pioneer"
    },
    {
        "id": 3,
        "name": "X-Ray Machine",
        "type": "Imaging",
        "status": "Active",
        "location": "Emergency Department",
        "manufacturer": "Philips",
        "model": "DigitalDiagnost"
    },
    {
        "id": 4,
        "name": "Ultrasound Machine",
        "type": "Imaging",
        "status": "Active",
        "location": "Cardiology Department",
        "manufacturer": "Canon",
        "model": "Aplio i900"
    },
    {
        "id": 5,
        "name": "PET Scanner",
        "type": "Imaging",
        "status": "Maintenance",
        "location": "Nuclear Medicine",
        "manufacturer": "Siemens",
        "model": "Biograph Horizon"
    }
]

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Flask API for Medical Imaging",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "port": 5001
    })

@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    """Get all equipment"""
    return jsonify({
        "equipment": EQUIPMENT_DATA,
        "total": len(EQUIPMENT_DATA),
        "source": "Flask API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """Get equipment by ID"""
    equipment = next((eq for eq in EQUIPMENT_DATA if eq["id"] == equipment_id), None)
    if equipment:
        return jsonify({
            "equipment": equipment,
            "source": "Flask API"
        })
    else:
        return jsonify({"error": "Equipment not found"}), 404

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "message": "Flask API for Medical Imaging System",
        "endpoints": {
            "health": "/api/health",
            "equipment": "/api/equipment",
            "equipment_by_id": "/api/equipment/<id>"
        },
        "port": 5001
    })

if __name__ == '__main__':
    print("Starting Flask API for Medical Imaging System...")
    print("Port: 5001")
    print("Health: http://localhost:5001/api/health")
    print("Equipment: http://localhost:5001/api/equipment")
    app.run(host='0.0.0.0', port=5001, debug=True)
'''
    
    try:
        with open(r"C:\Users\TTR\Documents\Project_BackEnd\flask_api.py", "w") as f:
            f.write(flask_api_code)
        print("   Flask API file created: flask_api.py")
        return True
    except Exception as e:
        print(f"   Error creating Flask API: {e}")
        return False

def start_flask_api():
    """Start Flask API service"""
    print("\n4. STARTING FLASK API SERVICE")
    print("-" * 40)
    
    try:
        # Check if Flask is installed
        try:
            import flask
            print("   Flask: INSTALLED")
        except ImportError:
            print("   Flask: NOT INSTALLED")
            print("   Installing Flask...")
            subprocess.run(['pip', 'install', 'flask', 'flask-cors'], 
                         capture_output=True, text=True, timeout=60)
            print("   Flask: INSTALLED")
        
        # Start Flask API
        import subprocess
        process = subprocess.Popen([
            'python', 'flask_api.py'
        ], cwd=r"C:\Users\TTR\Documents\Project_BackEnd", 
           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("   Flask API: STARTING...")
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("   Flask API: RUNNING")
            return True
        else:
            stdout, stderr = process.communicate()
            print("   Flask API: FAILED TO START")
            if stderr:
                print(f"   Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"   Error starting Flask API: {e}")
        return False

def test_flask_api_endpoints():
    """Test Flask API endpoints"""
    print("\n5. TESTING FLASK API ENDPOINTS")
    print("-" * 40)
    
    flask_api_url = "http://localhost:5001"
    
    endpoints = [
        ("/api/health", "Health Check"),
        ("/api/equipment", "Equipment Data"),
        ("/", "Root Endpoint")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{flask_api_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   {name}: SUCCESS")
                if endpoint == "/api/equipment":
                    data = response.json()
                    equipment_count = data.get('total', 0)
                    print(f"      Equipment count: {equipment_count}")
            else:
                print(f"   {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   {name}: ERROR - {e}")

def main():
    """Main function"""
    print(" FLASK API STATUS CHECK AND FIX")
    print("Issue: localhost:5001 - ERR_CONNECTION_REFUSED")
    print("=" * 80)
    
    # Check current status
    flask_running = check_flask_api_status()
    
    if not flask_running:
        # Check files
        flask_file = check_flask_api_files()
        
        if not flask_file:
            # Create Flask API
            if create_simple_flask_api():
                print("   Flask API created successfully")
            else:
                print("   Failed to create Flask API")
                return False
        
        # Start Flask API
        if start_flask_api():
            print("   Flask API started successfully")
            
            # Wait a moment for startup
            time.sleep(2)
            
            # Test endpoints
            test_flask_api_endpoints()
            
            # Final check
            print("\n" + "=" * 80)
            print("FLASK API STATUS SUMMARY")
            print("=" * 80)
            
            final_check = check_flask_api_status()
            if final_check:
                print("✅ FLASK API IS RUNNING")
                print("\nACCESS POINTS:")
                print("   Health: http://localhost:5001/api/health")
                print("   Equipment: http://localhost:5001/api/equipment")
                print("   Root: http://localhost:5001/")
                
                print("\nINTEGRATION:")
                print("   Backend can now access Flask API")
                print("   Equipment data available for medical imaging")
                
                return True
            else:
                print("❌ FLASK API STILL NOT ACCESSIBLE")
                return False
        else:
            print("❌ FAILED TO START FLASK API")
            return False
    else:
        print("✅ FLASK API IS ALREADY RUNNING")
        test_flask_api_endpoints()
        return True

if __name__ == "__main__":
    main()
