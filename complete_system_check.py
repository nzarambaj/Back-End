#!/usr/bin/env python3
"""
Complete System Status Check
Frontend, Backend, Calculus, and PostgreSQL Database verification
"""

import requests
import subprocess
import time
import os
from datetime import datetime

def check_frontend():
    """Check frontend status"""
    print(" FRONTEND STATUS CHECK")
    print("-" * 30)
    
    frontend_results = {}
    
    try:
        # Check frontend health
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            frontend_results["status"] = "✅ RUNNING"
            frontend_results["url"] = "http://localhost:3000"
            frontend_results["http_status"] = response.status_code
            
            # Check if it's a React app
            if "React" in response.text or "react" in response.text.lower():
                frontend_results["type"] = "React Application"
            else:
                frontend_results["type"] = "Web Application"
            
            print(f"   Frontend: ✅ RUNNING")
            print(f"   URL: http://localhost:3000")
            print(f"   Type: {frontend_results['type']}")
            print(f"   HTTP Status: {response.status_code}")
            
            # Check backend connectivity from frontend
            try:
                backend_response = requests.get("http://localhost:3000/api/health", timeout=5)
                if backend_response.status_code == 200:
                    frontend_results["backend_connectivity"] = "✅ CONNECTED"
                    print(f"   Backend Connectivity: ✅ CONNECTED")
                else:
                    frontend_results["backend_connectivity"] = f"⚠️ HTTP {backend_response.status_code}"
                    print(f"   Backend Connectivity: ⚠️ HTTP {backend_response.status_code}")
            except:
                frontend_results["backend_connectivity"] = "❌ NO CONNECTION"
                print(f"   Backend Connectivity: ❌ NO CONNECTION")
            
        else:
            frontend_results["status"] = f"❌ HTTP {response.status_code}"
            frontend_results["url"] = "http://localhost:3000"
            print(f"   Frontend: ❌ HTTP {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        frontend_results["status"] = "❌ CONNECTION REFUSED"
        frontend_results["url"] = "http://localhost:3000"
        print(f"   Frontend: ❌ CONNECTION REFUSED")
        
    except Exception as e:
        frontend_results["status"] = f"❌ ERROR - {str(e)}"
        frontend_results["url"] = "http://localhost:3000"
        print(f"   Frontend: ❌ ERROR - {e}")
    
    return frontend_results

def check_backend():
    """Check backend Express server status"""
    print("\n BACKEND EXPRESS SERVER STATUS")
    print("-" * 40)
    
    backend_results = {}
    
    try:
        # Check backend health
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            backend_results["status"] = "✅ RUNNING"
            backend_results["url"] = "http://localhost:5000"
            backend_results["http_status"] = response.status_code
            backend_results["database_status"] = health_data.get("database", "Unknown")
            
            print(f"   Backend: ✅ RUNNING")
            print(f"   URL: http://localhost:5000")
            print(f"   HTTP Status: {response.status_code}")
            print(f"   Database Status: {health_data.get('database', 'Unknown')}")
            
            # Check doctors endpoint
            try:
                doctors_response = requests.get("http://localhost:5000/api/doctors", timeout=5)
                if doctors_response.status_code == 200:
                    doctors_data = doctors_response.json()
                    backend_results["doctors_endpoint"] = "✅ WORKING"
                    backend_results["doctors_count"] = len(doctors_data.get("doctors", []))
                    print(f"   Doctors Endpoint: ✅ WORKING ({len(doctors_data.get('doctors', []))} doctors)")
                else:
                    backend_results["doctors_endpoint"] = f"⚠️ HTTP {doctors_response.status_code}"
                    print(f"   Doctors Endpoint: ⚠️ HTTP {doctors_response.status_code}")
            except:
                backend_results["doctors_endpoint"] = "❌ ERROR"
                print(f"   Doctors Endpoint: ❌ ERROR")
            
            # Check patients endpoint
            try:
                patients_response = requests.get("http://localhost:5000/api/patients", timeout=5)
                if patients_response.status_code == 200:
                    patients_data = patients_response.json()
                    backend_results["patients_endpoint"] = "✅ WORKING"
                    backend_results["patients_count"] = len(patients_data.get("patients", []))
                    print(f"   Patients Endpoint: ✅ WORKING ({len(patients_data.get('patients', []))} patients)")
                else:
                    backend_results["patients_endpoint"] = f"⚠️ HTTP {patients_response.status_code}"
                    print(f"   Patients Endpoint: ⚠️ HTTP {patients_response.status_code}")
            except:
                backend_results["patients_endpoint"] = "❌ ERROR"
                print(f"   Patients Endpoint: ❌ ERROR")
            
        else:
            backend_results["status"] = f"❌ HTTP {response.status_code}"
            backend_results["url"] = "http://localhost:5000"
            print(f"   Backend: ❌ HTTP {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        backend_results["status"] = "❌ CONNECTION REFUSED"
        backend_results["url"] = "http://localhost:5000"
        print(f"   Backend: ❌ CONNECTION REFUSED")
        
    except Exception as e:
        backend_results["status"] = f"❌ ERROR - {str(e)}"
        backend_results["url"] = "http://localhost:5000"
        print(f"   Backend: ❌ ERROR - {e}")
    
    return backend_results

def check_postgresql():
    """Check PostgreSQL database status"""
    print("\n POSTGRESQL DATABASE STATUS")
    print("-" * 35)
    
    db_results = {}
    
    try:
        # Check if PostgreSQL is running via backend
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            db_status = health_data.get("database", "").lower()
            
            if "connected" in db_status or "healthy" in db_status:
                db_results["status"] = "✅ CONNECTED"
                db_results["connection"] = health_data.get("database", "Unknown")
                print(f"   PostgreSQL: ✅ CONNECTED")
                print(f"   Connection: {health_data.get('database', 'Unknown')}")
                
                # Check database tables
                try:
                    tables_response = requests.get("http://localhost:5000/api/database/tables", timeout=5)
                    if tables_response.status_code == 200:
                        tables_data = tables_response.json()
                        db_results["tables"] = "✅ ACCESSIBLE"
                        db_results["table_count"] = len(tables_data.get("tables", []))
                        print(f"   Tables: ✅ ACCESSIBLE ({len(tables_data.get('tables', []))} tables)")
                    else:
                        db_results["tables"] = f"⚠️ HTTP {tables_response.status_code}"
                        print(f"   Tables: ⚠️ HTTP {tables_response.status_code}")
                except:
                    db_results["tables"] = "❌ ERROR"
                    print(f"   Tables: ❌ ERROR")
                
                # Check medical_db specifically
                try:
                    medical_db_response = requests.get("http://localhost:5000/api/medical_db/status", timeout=5)
                    if medical_db_response.status_code == 200:
                        medical_data = medical_db_response.json()
                        db_results["medical_db"] = "✅ AVAILABLE"
                        db_results["medical_db_status"] = medical_data.get("status", "Unknown")
                        print(f"   Medical DB: ✅ AVAILABLE ({medical_data.get('status', 'Unknown')})")
                    else:
                        db_results["medical_db"] = f"⚠️ HTTP {medical_db_response.status_code}"
                        print(f"   Medical DB: ⚠️ HTTP {medical_db_response.status_code}")
                except:
                    db_results["medical_db"] = "❌ ERROR"
                    print(f"   Medical DB: ❌ ERROR")
                    
            elif "error" in db_status or "failed" in db_status:
                db_results["status"] = "⚠️ CONNECTION ISSUES"
                db_results["connection"] = health_data.get("database", "Unknown")
                print(f"   PostgreSQL: ⚠️ CONNECTION ISSUES")
                print(f"   Connection: {health_data.get('database', 'Unknown')}")
            else:
                db_results["status"] = "❌ UNKNOWN STATUS"
                db_results["connection"] = health_data.get("database", "Unknown")
                print(f"   PostgreSQL: ❌ UNKNOWN STATUS")
                print(f"   Connection: {health_data.get('database', 'Unknown')}")
        else:
            db_results["status"] = "❌ BACKEND NOT ACCESSIBLE"
            print(f"   PostgreSQL: ❌ BACKEND NOT ACCESSIBLE")
            
    except requests.exceptions.ConnectionError:
        db_results["status"] = "❌ BACKEND CONNECTION REFUSED"
        print(f"   PostgreSQL: ❌ BACKEND CONNECTION REFUSED")
        
    except Exception as e:
        db_results["status"] = f"❌ ERROR - {str(e)}"
        print(f"   PostgreSQL: ❌ ERROR - {e}")
    
    return db_results

def check_calculus_system():
    """Check Calculus multi-brand system status"""
    print("\n CALCULUS MULTI-BRAND SYSTEM STATUS")
    print("-" * 45)
    
    calculus_results = {}
    
    try:
        # Check Calculus API health
        response = requests.get("http://localhost:5001/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            calculus_results["status"] = "✅ RUNNING"
            calculus_results["url"] = "http://localhost:5001"
            calculus_results["http_status"] = response.status_code
            calculus_results["equipment_count"] = health_data.get("total_equipment", 0)
            calculus_results["manufacturers_count"] = len(health_data.get("manufacturers", []))
            calculus_results["modalities_count"] = len(health_data.get("modalities", []))
            calculus_results["protocols_count"] = health_data.get("total_protocols", 0)
            
            print(f"   Calculus API: ✅ RUNNING")
            print(f"   URL: http://localhost:5001")
            print(f"   Equipment Systems: {health_data.get('total_equipment', 0)}")
            print(f"   Manufacturers: {len(health_data.get('manufacturers', []))}")
            print(f"   Modalities: {len(health_data.get('modalities', []))}")
            print(f"   Protocols: {health_data.get('total_protocols', 0)}")
            
            # Check equipment endpoint
            try:
                equipment_response = requests.get("http://localhost:5001/api/equipment", timeout=5)
                if equipment_response.status_code == 200:
                    equipment_data = equipment_response.json()
                    calculus_results["equipment_endpoint"] = "✅ WORKING"
                    calculus_results["equipment_verified"] = equipment_data.get("total", 0)
                    print(f"   Equipment Endpoint: ✅ WORKING ({equipment_data.get('total', 0)} systems)")
                else:
                    calculus_results["equipment_endpoint"] = f"⚠️ HTTP {equipment_response.status_code}"
                    print(f"   Equipment Endpoint: ⚠️ HTTP {equipment_response.status_code}")
            except:
                calculus_results["equipment_endpoint"] = "❌ ERROR"
                print(f"   Equipment Endpoint: ❌ ERROR")
            
            # Check manufacturer endpoints
            try:
                manufacturers_response = requests.get("http://localhost:5001/api/manufacturers", timeout=5)
                if manufacturers_response.status_code == 200:
                    manufacturers_data = manufacturers_response.json()
                    calculus_results["manufacturers_endpoint"] = "✅ WORKING"
                    calculus_results["manufacturers_verified"] = manufacturers_data.get("total_manufacturers", 0)
                    print(f"   Manufacturers Endpoint: ✅ WORKING ({manufacturers_data.get('total_manufacturers', 0)} brands)")
                else:
                    calculus_results["manufacturers_endpoint"] = f"⚠️ HTTP {manufacturers_response.status_code}"
                    print(f"   Manufacturers Endpoint: ⚠️ HTTP {manufacturers_response.status_code}")
            except:
                calculus_results["manufacturers_endpoint"] = "❌ ERROR"
                print(f"   Manufacturers Endpoint: ❌ ERROR")
            
            # Check protocols endpoint
            try:
                protocols_response = requests.get("http://localhost:5001/api/protocols", timeout=5)
                if protocols_response.status_code == 200:
                    protocols_data = protocols_response.json()
                    calculus_results["protocols_endpoint"] = "✅ WORKING"
                    calculus_results["protocols_verified"] = protocols_data.get("total", 0)
                    print(f"   Protocols Endpoint: ✅ WORKING ({protocols_data.get('total', 0)} protocols)")
                else:
                    calculus_results["protocols_endpoint"] = f"⚠️ HTTP {protocols_response.status_code}"
                    print(f"   Protocols Endpoint: ⚠️ HTTP {protocols_response.status_code}")
            except:
                calculus_results["protocols_endpoint"] = "❌ ERROR"
                print(f"   Protocols Endpoint: ❌ ERROR")
                
        else:
            calculus_results["status"] = f"❌ HTTP {response.status_code}"
            calculus_results["url"] = "http://localhost:5001"
            print(f"   Calculus API: ❌ HTTP {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        calculus_results["status"] = "❌ CONNECTION REFUSED"
        calculus_results["url"] = "http://localhost:5001"
        print(f"   Calculus API: ❌ CONNECTION REFUSED")
        
    except Exception as e:
        calculus_results["status"] = f"❌ ERROR - {str(e)}"
        calculus_results["url"] = "http://localhost:5001"
        print(f"   Calculus API: ❌ ERROR - {e}")
    
    return calculus_results

def check_system_integration():
    """Check system integration between components"""
    print("\n SYSTEM INTEGRATION CHECK")
    print("-" * 30)
    
    integration_results = {}
    
    # Check Frontend to Backend
    try:
        response = requests.get("http://localhost:3000/api/health", timeout=5)
        if response.status_code == 200:
            integration_results["frontend_backend"] = "✅ CONNECTED"
            print(f"   Frontend → Backend: ✅ CONNECTED")
        else:
            integration_results["frontend_backend"] = f"⚠️ HTTP {response.status_code}"
            print(f"   Frontend → Backend: ⚠️ HTTP {response.status_code}")
    except:
        integration_results["frontend_backend"] = "❌ NO CONNECTION"
        print(f"   Frontend → Backend: ❌ NO CONNECTION")
    
    # Check Backend to Database
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            db_status = health_data.get("database", "").lower()
            if "connected" in db_status or "healthy" in db_status:
                integration_results["backend_database"] = "✅ CONNECTED"
                print(f"   Backend → Database: ✅ CONNECTED")
            else:
                integration_results["backend_database"] = "⚠️ CONNECTION ISSUES"
                print(f"   Backend → Database: ⚠️ CONNECTION ISSUES")
        else:
            integration_results["backend_database"] = "❌ BACKEND NOT ACCESSIBLE"
            print(f"   Backend → Database: ❌ BACKEND NOT ACCESSIBLE")
    except:
        integration_results["backend_database"] = "❌ NO CONNECTION"
        print(f"   Backend → Database: ❌ NO CONNECTION")
    
    # Check Calculus System Independence
    try:
        response = requests.get("http://localhost:5001/api/health", timeout=5)
        if response.status_code == 200:
            integration_results["calculus_independent"] = "✅ INDEPENDENT"
            print(f"   Calculus System: ✅ INDEPENDENT")
        else:
            integration_results["calculus_independent"] = f"⚠️ HTTP {response.status_code}"
            print(f"   Calculus System: ⚠️ HTTP {response.status_code}")
    except:
        integration_results["calculus_independent"] = "❌ NOT ACCESSIBLE"
        print(f"   Calculus System: ❌ NOT ACCESSIBLE")
    
    return integration_results

def generate_system_report(frontend, backend, database, calculus, integration):
    """Generate comprehensive system status report"""
    print("\n" + "=" * 80)
    print(" COMPLETE SYSTEM STATUS REPORT")
    print("=" * 80)
    
    # Overall system status
    print("\n🎯 OVERALL SYSTEM STATUS:")
    print("-" * 30)
    
    system_components = [
        ("Frontend", frontend.get("status", "❌ UNKNOWN")),
        ("Backend", backend.get("status", "❌ UNKNOWN")),
        ("PostgreSQL", database.get("status", "❌ UNKNOWN")),
        ("Calculus System", calculus.get("status", "❌ UNKNOWN"))
    ]
    
    running_count = 0
    for component, status in system_components:
        print(f"   {component}: {status}")
        if "✅" in status:
            running_count += 1
    
    overall_status = f"✅ {running_count}/4 RUNNING" if running_count >= 3 else f"⚠️ {running_count}/4 RUNNING"
    print(f"\n   Overall: {overall_status}")
    
    # Service URLs
    print("\n🌐 SERVICE URLS:")
    print("-" * 20)
    print(f"   Frontend: {frontend.get('url', 'http://localhost:3000')}")
    print(f"   Backend: {backend.get('url', 'http://localhost:5000')}")
    print(f"   Calculus API: {calculus.get('url', 'http://localhost:5001')}")
    
    # Database information
    print("\n💾 DATABASE STATUS:")
    print("-" * 25)
    print(f"   Connection: {database.get('connection', 'Unknown')}")
    print(f"   Tables: {database.get('tables', 'Unknown')}")
    print(f"   Medical DB: {database.get('medical_db', 'Unknown')}")
    
    # Calculus system details
    print("\n🏥 CALCULUS SYSTEM DETAILS:")
    print("-" * 35)
    print(f"   Equipment: {calculus.get('equipment_count', 0)} systems")
    print(f"   Manufacturers: {calculus.get('manufacturers_count', 0)} brands")
    print(f"   Modalities: {calculus.get('modalities_count', 0)} types")
    print(f"   Protocols: {calculus.get('protocols_count', 0)} protocols")
    
    # Integration status
    print("\n🔗 INTEGRATION STATUS:")
    print("-" * 25)
    print(f"   Frontend → Backend: {integration.get('frontend_backend', '❌ UNKNOWN')}")
    print(f"   Backend → Database: {integration.get('backend_database', '❌ UNKNOWN')}")
    print(f"   Calculus Independence: {integration.get('calculus_independent', '❌ UNKNOWN')}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    print("-" * 25)
    
    if "❌" in frontend.get("status", ""):
        print("   • Start frontend service (npm start)")
    
    if "❌" in backend.get("status", ""):
        print("   • Start backend Express server")
    
    if "❌" in database.get("status", ""):
        print("   • Check PostgreSQL service status")
        print("   • Verify database connection string")
    
    if "❌" in calculus.get("status", ""):
        print("   • Start Calculus multi-brand API")
        print("   • Run: cd C:\\Users\\TTR\\Documents\\Calculus\\medical_imaging_system\\api")
        print("   • Run: python multi_brand_medical_api.py")
    
    if "❌" in integration.get("frontend_backend", ""):
        print("   • Check frontend backend configuration")
    
    if "❌" in integration.get("backend_database", ""):
        print("   • Verify database credentials and connection")
    
    # Quick start commands
    print("\n🚀 QUICK START COMMANDS:")
    print("-" * 30)
    print("   Frontend: cd frontend && npm start")
    print("   Backend: cd backend && node medical_db_backend.js")
    print("   Calculus: cd C:\\Users\\TTR\\Documents\\Calculus\\medical_imaging_system\\api && python multi_brand_medical_api.py")
    print("   Database: Ensure PostgreSQL service is running")
    
    print("\n" + "=" * 80)
    print("END OF SYSTEM STATUS REPORT")
    print("=" * 80)

def main():
    """Main system check function"""
    print(" COMPLETE SYSTEM STATUS CHECK")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Checking: Frontend, Backend, PostgreSQL, Calculus System")
    print("=" * 80)
    
    # Run all checks
    frontend_status = check_frontend()
    backend_status = check_backend()
    database_status = check_postgresql()
    calculus_status = check_calculus_system()
    integration_status = check_system_integration()
    
    # Generate comprehensive report
    generate_system_report(frontend_status, backend_status, database_status, calculus_status, integration_status)

if __name__ == "__main__":
    main()
