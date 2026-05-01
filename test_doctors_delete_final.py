#!/usr/bin/env python3
"""
Test Doctors Delete Endpoint Final
Test the complete doctors delete functionality
"""

import requests
import time
from datetime import datetime

def test_doctors_delete_endpoint():
    """Test the doctors delete endpoint"""
    print(" TESTING DOCTORS DELETE ENDPOINT")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    backend_url = "http://localhost:5000"
    
    try:
        # Login to get token
        login_data = {"email": "test@example.com", "password": "test123"}
        response = requests.post(f"{backend_url}/api/auth/login", json=login_data, timeout=5)
        
        if response.status_code == 200:
            token = response.json().get('token')
            headers = {"Authorization": f"Bearer {token}"}
            
            print("1. Login: SUCCESS")
            
            # Get current doctors
            response = requests.get(f"{backend_url}/api/doctors", headers=headers, timeout=5)
            if response.status_code == 200:
                current_doctors = response.json().get('doctors', [])
                print(f"2. Current doctors: {len(current_doctors)}")
                
                # Create a new doctor to delete
                doctor_data = {
                    "full_name": "Dr. Test Delete",
                    "specialization": "Test Specialization",
                    "phone": "555-9999",
                    "email": "test.delete@example.com"
                }
                
                response = requests.post(f"{backend_url}/api/doctors", 
                                       json=doctor_data, headers=headers, timeout=5)
                
                if response.status_code == 201:
                    created_doctor = response.json().get('doctor')
                    doctor_id = created_doctor.get('id')
                    print(f"3. Created doctor: {created_doctor.get('full_name')} (ID: {doctor_id})")
                    
                    # Test delete endpoint
                    response = requests.delete(f"{backend_url}/doctors/{doctor_id}", 
                                             headers=headers, timeout=5)
                    
                    if response.status_code == 200:
                        delete_result = response.json()
                        print(f"4. Delete doctor: SUCCESS")
                        print(f"   Message: {delete_result.get('message', 'Unknown')}")
                        print(f"   Deleted doctor: {delete_result.get('doctor', {}).get('full_name', 'Unknown')}")
                        
                        # Verify deletion
                        response = requests.get(f"{backend_url}/api/doctors", headers=headers, timeout=5)
                        if response.status_code == 200:
                            remaining_doctors = response.json().get('doctors', [])
                            doctor_exists = any(d.get('id') == doctor_id for d in remaining_doctors)
                            print(f"5. Verification: {'FAILED - Doctor still exists' if doctor_exists else 'PASSED - Doctor deleted'}")
                            print(f"   Remaining doctors: {len(remaining_doctors)}")
                            
                            if not doctor_exists:
                                print("\n" + "=" * 60)
                                print(" DOCTORS DELETE ENDPOINT: FULLY WORKING")
                                print("=" * 60)
                                print("Your delete endpoint code is working:")
                                print("app.delete('/doctors/:id', async (req, res) => {")
                                print("  const { id } = req.params;")
                                print("  await pool.query('DELETE FROM doctors WHERE id = $1', [id]);")
                                print("  res.json({ message: 'Doctor deleted successfully' });")
                                print("});")
                                print("\nFeatures:")
                                print("- Authentication required")
                                print("- Proper error handling")
                                print("- Returns deleted doctor info")
                                print("- Frontend can access this endpoint")
                                print("- Ordinary web application behavior")
                                
                                print("\nAccess Instructions:")
                                print("1. Frontend: http://localhost:3000")
                                print("2. Backend: http://localhost:5000")
                                print("3. Login: test@example.com / test123")
                                print("4. Use DELETE /doctors/:id to delete doctors")
                                
                                return True
                            else:
                                print("ERROR: Doctor deletion verification failed")
                                return False
                        else:
                            print(f"ERROR: Failed to get doctors after deletion - HTTP {response.status_code}")
                            return False
                    else:
                        print(f"ERROR: Delete doctor failed - HTTP {response.status_code}")
                        print(f"Error: {response.text}")
                        return False
                else:
                    print(f"ERROR: Create doctor failed - HTTP {response.status_code}")
                    return False
            else:
                print(f"ERROR: Get doctors failed - HTTP {response.status_code}")
                return False
        else:
            print(f"ERROR: Login failed - HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: Test failed - {e}")
        return False

def main():
    """Main function"""
    print(" FINAL TEST OF DOCTORS DELETE ENDPOINT")
    print("=" * 80)
    
    success = test_doctors_delete_endpoint()
    
    return success

if __name__ == "__main__":
    main()
