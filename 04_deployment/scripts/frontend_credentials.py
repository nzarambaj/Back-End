#!/usr/bin/env python3
"""
Frontend Credentials Information
Display all available login credentials for the frontend
"""

from datetime import datetime

def show_frontend_credentials():
    """Display all frontend login credentials"""
    print(" FRONTEND LOGIN CREDENTIALS")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    print("PRIMARY LOGIN CREDENTIALS:")
    print("-" * 40)
    print("Email: test@example.com")
    print("Password: test123")
    print("Role: admin")
    print("First Name: Test")
    print("Last Name: User")
    
    print("\nADDITIONAL LOGIN CREDENTIALS:")
    print("-" * 40)
    print("Email: doctor@medical.com")
    print("Password: doctor123")
    print("Role: doctor")
    print("First Name: John")
    print("Last Name: Doe")
    
    print("\nEmail: radiologist@medical.com")
    print("Password: rad123")
    print("Role: radiologist")
    print("First Name: Sarah")
    print("Last Name: Wilson")
    
    print("\nFRONTEND ACCESS INFORMATION:")
    print("-" * 40)
    print("Frontend URL: http://localhost:3000")
    print("Dashboard URL: http://localhost:3000/dashboard")
    print("Login Page: http://localhost:3000/login")
    
    print("\nACCESS INSTRUCTIONS:")
    print("-" * 40)
    print("1. Open browser and go to: http://localhost:3000")
    print("2. Click on Login or Dashboard")
    print("3. Enter email and password from above")
    print("4. Click Login button")
    print("5. Access medical imaging features")
    
    print("\nFEATURES AVAILABLE AFTER LOGIN:")
    print("-" * 40)
    print("Patient Management (Create, Read, Update, Delete)")
    print("Doctor Management (Create, Read, Update, Delete)")
    print("Study Management (Medical studies tracking)")
    print("Equipment Data (From Flask API)")
    print("Dashboard with real-time data")
    print("Medical database access")
    
    print("\nSYSTEM ARCHITECTURE:")
    print("-" * 40)
    print("Frontend (3000) -> Backend (5000) -> medical_db (5432) -> Flask API (5001)")
    
    print("\nBACKEND CONFIGURATION:")
    print("-" * 40)
    print("Database: medical_db")
    print("Backend URL: http://localhost:5000")
    print("Flask API URL: http://localhost:5001")
    print("Authentication: JWT-based")
    
    print("\nTROUBLESHOOTING:")
    print("-" * 40)
    print("If login fails:")
    print("1. Check frontend is running on port 3000")
    print("2. Check backend is running on port 5000")
    print("3. Verify email and password are correct")
    print("4. Check network connectivity")
    print("5. Try refreshing the page")
    
    print("\nSUPPORTED BROWSERS:")
    print("-" * 40)
    print("Chrome, Firefox, Edge, Safari")
    print("JavaScript must be enabled")
    print("Cookies must be enabled for authentication")

if __name__ == "__main__":
    show_frontend_credentials()
