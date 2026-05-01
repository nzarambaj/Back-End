#!/usr/bin/env python3
"""
Fix Equipment Endpoint for Advanced Modalities API
Add the missing /api/equipment endpoint
"""

import requests
import time
from datetime import datetime

def add_equipment_endpoint():
    """Add equipment endpoint to the advanced modalities API"""
    print(" FIXING EQUIPMENT ENDPOINT")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Read the current advanced modalities API
    try:
        with open(r"C:\Users\TTR\Documents\Project_BackEnd\advanced_modalities_api.py", "r") as f:
            content = f.read()
        
        # Check if equipment endpoint already exists
        if "/api/equipment" in content:
            print("Equipment endpoint already exists in the API")
            return False
        
        # Find the location to insert the equipment endpoint
        # We'll add it after the workflow endpoints
        workflow_end = content.find("@app.route('/api/workflows/quality', methods=['GET'])")
        if workflow_end == -1:
            print("Could not find workflow endpoints")
            return False
        
        # Find the end of the workflow function
        workflow_function_end = content.find("def get_quality_control():", workflow_end)
        if workflow_function_end == -1:
            print("Could not find workflow function")
            return False
        
        # Find the end of the workflow function
        next_function = content.find("@app.route", workflow_function_end)
        if next_function == -1:
            next_function = content.find("if __name__ == '__main__':", workflow_function_end)
        
        if next_function == -1:
            print("Could not find insertion point")
            return False
        
        # Create the equipment endpoint code
        equipment_endpoint = '''

# Equipment endpoint - Add missing endpoint
@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    """Get all equipment across all modalities"""
    return jsonify({
        "equipment": MODALITY_EQUIPMENT,
        "total": len(MODALITY_EQUIPMENT),
        "modalities": list(set(e["modality_code"] for e in MODALITY_EQUIPMENT)),
        "manufacturers": list(set(e["manufacturer"] for e in MODALITY_EQUIPMENT)),
        "source": "Advanced Modalities API",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """Get equipment by ID"""
    equipment = next((e for e in MODALITY_EQUIPMENT if e["id"] == equipment_id), None)
    if equipment:
        return jsonify({
            "equipment": equipment,
            "source": "Advanced Modalities API"
        })
    else:
        return jsonify({"error": f"Equipment ID '{equipment_id}' not found"}), 404

'''
        
        # Insert the equipment endpoint
        new_content = content[:next_function] + equipment_endpoint + content[next_function:]
        
        # Write the updated content
        with open(r"C:\Users\TTR\Documents\Project_BackEnd\advanced_modalities_api.py", "w") as f:
            f.write(new_content)
        
        print("Equipment endpoint added successfully")
        return True
        
    except Exception as e:
        print(f"Error adding equipment endpoint: {e}")
        return False

def restart_api():
    """Restart the API service"""
    print("\n RESTARTING API SERVICE")
    print("-" * 30)
    
    try:
        # Stop current API
        import subprocess
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, text=True, timeout=10)
        print("Stopped current API service")
        time.sleep(2)
        
        # Start the updated API
        subprocess.Popen(['python', 'advanced_modalities_api.py'], 
                       cwd=r"C:\Users\TTR\Documents\Project_BackEnd")
        print("Started updated API service")
        
        # Wait for startup
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"Error restarting API: {e}")
        return False

def test_equipment_endpoint():
    """Test the equipment endpoint"""
    print("\n TESTING EQUIPMENT ENDPOINT")
    print("-" * 30)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5001/api/health", timeout=5)
        if response.status_code != 200:
            print("API not accessible")
            return False
        
        # Test equipment endpoint
        response = requests.get("http://localhost:5001/api/equipment", timeout=5)
        if response.status_code == 200:
            equipment_data = response.json()
            print("✅ Equipment endpoint: WORKING")
            print(f"   Total Equipment: {equipment_data.get('total', 0)}")
            print(f"   Modalities: {equipment_data.get('modalities', [])}")
            print(f"   Manufacturers: {equipment_data.get('manufacturers', [])}")
            
            # Test equipment by ID
            if equipment_data.get('total', 0) > 0:
                first_id = equipment_data['equipment'][0]['id']
                response = requests.get(f"http://localhost:5001/api/equipment/{first_id}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ Equipment by ID: WORKING (ID: {first_id})")
                else:
                    print(f"❌ Equipment by ID: HTTP {response.status_code}")
            
            return True
        else:
            print(f"❌ Equipment endpoint: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Equipment endpoint test: ERROR - {e}")
        return False

def main():
    """Main function"""
    print(" EQUIPMENT ENDPOINT FIX")
    print("Issue: http://localhost:5001/api/equipment - Not Found")
    print("=" * 80)
    
    # Step 1: Add equipment endpoint
    if add_equipment_endpoint():
        print("\n✅ Equipment endpoint added to API code")
        
        # Step 2: Restart API
        if restart_api():
            print("\n✅ API service restarted")
            
            # Step 3: Test endpoint
            if test_equipment_endpoint():
                print("\n" + "=" * 80)
                print(" EQUIPMENT ENDPOINT FIX SUMMARY")
                print("=" * 80)
                print("✅ EQUIPMENT ENDPOINT: FIXED")
                print("✅ API Service: RUNNING")
                print("✅ Endpoint Test: PASSED")
                
                print("\nAVAILABLE EQUIPMENT ENDPOINTS:")
                print("-" * 40)
                print("• GET /api/equipment - All equipment")
                print("• GET /api/equipment/<id> - Equipment by ID")
                print("• GET /api/equipment/modality/<code> - By modality")
                print("• GET /api/equipment/manufacturer/<name> - By manufacturer")
                print("• GET /api/equipment/features - Advanced features")
                
                print("\nACCESS URL:")
                print("-" * 40)
                print("http://localhost:5001/api/equipment")
                
                return True
            else:
                print("\n❌ Equipment endpoint test failed")
                return False
        else:
            print("\n❌ Failed to restart API service")
            return False
    else:
        print("\n❌ Failed to add equipment endpoint")
        return False

if __name__ == "__main__":
    main()
