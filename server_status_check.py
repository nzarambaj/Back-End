#!/usr/bin/env python3
"""
Server Status Check and Dashboard Test
Check all servers and test dashboard functionality
"""

import subprocess
import requests
import json
from datetime import datetime

class ServerStatusChecker:
    def __init__(self):
        self.servers = {
            "Frontend": {"port": 3000, "url": "http://localhost:3000"},
            "Backend": {"port": 5000, "url": "http://localhost:5000"},
            "Calculus": {"port": 5001, "url": "http://localhost:5001"}
        }
        self.status = {}
        
    def check_server_port(self, port):
        """Check if a port is being used"""
        try:
            result = subprocess.run(['netstat', '-ano', '|', 'findstr', f':{port}'], 
                                  capture_output=True, text=True, shell=True)
            return result.returncode == 0 and str(port) in result.stdout
        except:
            return False
    
    def check_server_response(self, url, timeout=5):
        """Check if a server responds to HTTP requests"""
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200, response.status_code
        except requests.exceptions.ConnectionError:
            return False, "Connection refused"
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)
    
    def run_comprehensive_check(self):
        """Run comprehensive server status check"""
        print(" SERVER STATUS CHECK")
        print("=" * 80)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        all_running = True
        
        for server_name, server_info in self.servers.items():
            port = server_info["port"]
            url = server_info["url"]
            
            print(f"\n{server_name} Server:")
            print(f"   Port: {port}")
            print(f"   URL: {url}")
            
            # Check port
            port_active = self.check_server_port(port)
            print(f"   Port Status: {'ACTIVE' if port_active else 'INACTIVE'}")
            
            # Check HTTP response
            if port_active:
                response_ok, status = self.check_server_response(url)
                print(f"   HTTP Status: {'OK' if response_ok else status}")
                
                if response_ok:
                    self.status[server_name] = "RUNNING"
                    print(f"   Overall: RUNNING")
                else:
                    self.status[server_name] = "ERROR"
                    print(f"   Overall: ERROR - {status}")
                    all_running = False
            else:
                self.status[server_name] = "DOWN"
                print(f"   Overall: DOWN")
                all_running = False
        
        print(f"\n OVERALL STATUS:")
        print("-" * 50)
        if all_running:
            print(" ALL SERVERS: RUNNING")
        else:
            print(" SOME SERVERS: NOT RUNNING")
            for server, status in self.status.items():
                print(f"   {server}: {status}")
        
        return all_running
    
    def test_dashboard_access(self):
        """Test dashboard access on frontend"""
        print(f"\n DASHBOARD ACCESS TEST")
        print("-" * 50)
        
        dashboard_urls = [
            "http://localhost:3000",
            "http://localhost:3000/dashboard",
            "http://localhost:3000/login"
        ]
        
        for url in dashboard_urls:
            print(f"\nTesting: {url}")
            try:
                response = requests.get(url, timeout=5)
                print(f"   Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'html' in content_type.lower():
                        print(f"   Content: HTML page")
                        print(f"   Status: ACCESSIBLE")
                    else:
                        print(f"   Content: {content_type}")
                        print(f"   Status: RESPONDING")
                else:
                    print(f"   Status: HTTP {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print(f"   Status: CONNECTION REFUSED")
            except requests.exceptions.Timeout:
                print(f"   Status: TIMEOUT")
            except Exception as e:
                print(f"   Status: ERROR - {e}")
    
    def test_backend_endpoints(self):
        """Test backend API endpoints"""
        print(f"\n BACKEND API TEST")
        print("-" * 50)
        
        endpoints = [
            "http://localhost:5000/api/health",
            "http://localhost:5000/api/patients",
            "http://localhost:5000/api/doctors",
            "http://localhost:5000/api/studies"
        ]
        
        for endpoint in endpoints:
            print(f"\nTesting: {endpoint}")
            try:
                response = requests.get(endpoint, timeout=5)
                print(f"   Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'status' in data:
                            print(f"   Response: {data.get('status', 'OK')}")
                        elif 'patients' in data:
                            print(f"   Response: {len(data.get('patients', []))} patients")
                        elif 'doctors' in data:
                            print(f"   Response: {len(data.get('doctors', []))} doctors")
                        elif 'studies' in data:
                            print(f"   Response: {len(data.get('studies', []))} studies")
                        else:
                            print(f"   Response: JSON data")
                    except:
                        print(f"   Response: Non-JSON content")
                else:
                    print(f"   Status: HTTP {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print(f"   Status: CONNECTION REFUSED")
            except Exception as e:
                print(f"   Status: ERROR - {e}")
    
    def test_calculus_endpoints(self):
        """Test Calculus API endpoints"""
        print(f"\n CALCULUS API TEST")
        print("-" * 50)
        
        endpoints = [
            "http://localhost:5001/",
            "http://localhost:5001/api/data",
            "http://localhost:5001/api/equipment"
        ]
        
        for endpoint in endpoints:
            print(f"\nTesting: {endpoint}")
            try:
                response = requests.get(endpoint, timeout=5)
                print(f"   Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'equipment' in data:
                            print(f"   Response: {len(data.get('equipment', []))} equipment items")
                        elif 'status' in data:
                            print(f"   Response: {data.get('status', 'OK')}")
                        else:
                            print(f"   Response: JSON data")
                    except:
                        print(f"   Response: Non-JSON content")
                else:
                    print(f"   Status: HTTP {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print(f"   Status: CONNECTION REFUSED")
            except Exception as e:
                print(f"   Status: ERROR - {e}")
    
    def generate_report(self):
        """Generate comprehensive status report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "server_status": self.status,
            "overall_status": "RUNNING" if all(status == "RUNNING" for status in self.status.values()) else "PARTIAL"
        }
        
        with open("server_status_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n Report saved to: server_status_report.json")
        return report

if __name__ == "__main__":
    checker = ServerStatusChecker()
    
    # Check server status
    servers_running = checker.run_comprehensive_check()
    
    # Test dashboard access
    checker.test_dashboard_access()
    
    # Test backend endpoints
    checker.test_backend_endpoints()
    
    # Test calculus endpoints
    checker.test_calculus_endpoints()
    
    # Generate report
    checker.generate_report()
    
    print(f"\n" + "=" * 80)
    print(" SUMMARY:")
    if servers_running:
        print(" All servers are running and accessible!")
        print(" Dashboard should be available at: http://localhost:3000/dashboard")
    else:
        print(" Some servers are not running.")
        print(" Check the detailed status above for troubleshooting.")
    print("=" * 80)
