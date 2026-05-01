#!/usr/bin/env python3
"""
Backend Organization Analysis
Analyze and organize the Project_BackEnd folder structure
"""

import os
import json
from pathlib import Path
from datetime import datetime

class BackendOrganizationAnalyzer:
    def __init__(self):
        self.base_path = Path(r"C:\Users\TTR\Documents\Project_BackEnd")
        self.organization_score = 0
        self.max_score = 100
        self.issues = []
        self.strengths = []
        
    def analyze_current_structure(self):
        """Analyze the current backend structure"""
        print(" BACKEND ORGANIZATION ANALYSIS")
        print("=" * 80)
        print(f"Location: {self.base_path}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Get current structure
        try:
            items = list(self.base_path.iterdir())
            
            folders = []
            files = []
            
            for item in items:
                if item.is_dir():
                    folders.append(item.name)
                elif item.is_file():
                    files.append(item.name)
            
            print(f"\n CURRENT STRUCTURE:")
            print(f"Total folders: {len(folders)}")
            print(f"Total files: {len(files)}")
            
            print(f"\n FOLDERS:")
            for folder in sorted(folders):
                folder_path = self.base_path / folder
                try:
                    sub_items = list(folder_path.iterdir())
                    print(f"   {folder}/ - {len(sub_items)} items")
                    
                    # Show key subfolders for important folders
                    if folder in ['app', 'controllers', 'models', 'routes', 'config', 'middleware']:
                        subfolders = [i.name for i in sub_items if i.is_dir()]
                        if subfolders:
                            print(f"      Subfolders: {', '.join(subfolders[:5])}")
                            if len(subfolders) > 5:
                                print(f"      ... and {len(subfolders) - 5} more")
                    
                except Exception as e:
                    print(f"   {folder}/ - Error accessing: {e}")
            
            print(f"\n FILES:")
            for file in sorted(files):
                file_path = self.base_path / file
                try:
                    size = file_path.stat().st_size
                    size_str = self.format_size(size)
                    print(f"   {file} ({size_str})")
                except:
                    print(f"   {file} (size unknown)")
            
            # Analyze key components
            self.analyze_express_structure(folders, files)
            self.analyze_essential_files(files)
            self.analyze_mvc_structure(folders)
            self.analyze_database_integration(folders, files)
            self.analyze_api_structure(folders)
            self.analyze_documentation(files)
            
            # Calculate final score and recommendations
            self.calculate_organization_score()
            self.generate_recommendations()
            
            return True
            
        except Exception as e:
            print(f"Error analyzing structure: {e}")
            return False
    
    def format_size(self, size_bytes):
        """Format file size"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def analyze_express_structure(self, folders, files):
        """Analyze Express.js specific structure"""
        print(f"\n EXPRESS.JS STRUCTURE ANALYSIS:")
        print("-" * 50)
        
        # Essential Express.js folders
        express_folders = {
            "app": "Main application folder",
            "controllers": "Request handlers",
            "models": "Database models",
            "routes": "API routes",
            "middleware": "Custom middleware",
            "config": "Configuration files"
        }
        
        print(" Essential Express.js Folders:")
        for folder, description in express_folders.items():
            if folder in folders:
                print(f"   {folder}/: PRESENT - {description}")
                self.strengths.append(f"Express.js folder present: {folder}/")
                self.organization_score += 8
            else:
                print(f"   {folder}/: MISSING - {description}")
                self.issues.append(f"Missing Express.js folder: {folder}/")
        
        # Essential Express.js files
        express_files = {
            "app.js": "Main application entry point",
            "package.json": "Dependencies and scripts",
            "requirements.txt": "Python dependencies",
            ".env.example": "Environment variables template"
        }
        
        print("\n Essential Express.js Files:")
        for file, description in express_files.items():
            if file in files:
                print(f"   {file}: PRESENT - {description}")
                self.strengths.append(f"Express.js file present: {file}")
                self.organization_score += 5
            else:
                print(f"   {file}: MISSING - {description}")
                self.issues.append(f"Missing Express.js file: {file}")
    
    def analyze_essential_files(self, files):
        """Analyze essential project files"""
        print(f"\n ESSENTIAL FILES ANALYSIS:")
        print("-" * 50)
        
        # Check for package.json content
        package_json_path = self.base_path / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                
                dependencies = package_data.get('dependencies', {})
                scripts = package_data.get('scripts', {})
                
                print(f" Package.json Analysis:")
                print(f"   Dependencies: {len(dependencies)}")
                print(f"   Scripts: {len(scripts)}")
                
                # Check for essential dependencies
                essential_deps = ['express', 'cors', 'dotenv']
                found_deps = [dep for dep in essential_deps if dep in dependencies]
                
                if len(found_deps) >= 2:
                    print(f"   Essential dependencies: PRESENT")
                    self.strengths.append("Essential Express.js dependencies present")
                    self.organization_score += 10
                else:
                    missing = set(essential_deps) - set(found_deps)
                    print(f"   Essential dependencies: MISSING {missing}")
                    self.issues.append(f"Missing essential dependencies: {missing}")
                
                # Check for essential scripts
                essential_scripts = ['start', 'dev', 'test']
                found_scripts = [script for script in essential_scripts if script in scripts]
                
                if len(found_scripts) >= 1:
                    print(f"   Essential scripts: PRESENT")
                    self.strengths.append("Essential npm scripts present")
                    self.organization_score += 5
                else:
                    missing = set(essential_scripts) - set(found_scripts)
                    print(f"   Essential scripts: MISSING {missing}")
                    self.issues.append(f"Missing essential scripts: {missing}")
                
            except Exception as e:
                print(f"   Error reading package.json: {e}")
                self.issues.append("Invalid package.json file")
        
        # Check for Python requirements
        requirements_path = self.base_path / "requirements.txt"
        if requirements_path.exists():
            try:
                with open(requirements_path, 'r', encoding='utf-8') as f:
                    requirements = f.read().strip().split('\n')
                
                python_deps = [req.strip() for req in requirements if req.strip()]
                print(f" Python Requirements.txt Analysis:")
                print(f"   Dependencies: {len(python_deps)}")
                
                essential_python_deps = ['psycopg2-binary', 'python-dotenv', 'flask']
                found_python_deps = [dep for dep in essential_python_deps if any(dep in req for req in python_deps)]
                
                if len(found_python_deps) >= 1:
                    print(f"   Essential Python dependencies: PRESENT")
                    self.strengths.append("Essential Python dependencies present")
                    self.organization_score += 5
                else:
                    print(f"   Essential Python dependencies: LIMITED")
                
            except Exception as e:
                print(f"   Error reading requirements.txt: {e}")
    
    def analyze_mvc_structure(self, folders):
        """Analyze MVC (Model-View-Controller) structure"""
        print(f"\n MVC STRUCTURE ANALYSIS:")
        print("-" * 50)
        
        mvc_folders = {
            "models": "Data models and schemas",
            "controllers": "Request controllers",
            "routes": "API routes (views)",
            "app": "Application entry point"
        }
        
        mvc_present = 0
        for folder, description in mvc_folders.items():
            if folder in folders:
                print(f"   {folder}/: PRESENT - {description}")
                mvc_present += 1
                
                # Analyze folder content
                folder_path = self.base_path / folder
                try:
                    items = list(folder_path.iterdir())
                    if folder == "controllers":
                        controller_files = [i.name for i in items if i.suffix == '.js']
                        print(f"      Controller files: {len(controller_files)}")
                        if len(controller_files) > 0:
                            self.strengths.append(f"Controllers implemented: {len(controller_files)} files")
                            self.organization_score += 3
                    
                    elif folder == "models":
                        model_files = [i.name for i in items if i.suffix == '.js']
                        print(f"      Model files: {len(model_files)}")
                        if len(model_files) > 0:
                            self.strengths.append(f"Models implemented: {len(model_files)} files")
                            self.organization_score += 3
                    
                    elif folder == "routes":
                        route_files = [i.name for i in items if i.suffix == '.js']
                        print(f"      Route files: {len(route_files)}")
                        if len(route_files) > 0:
                            self.strengths.append(f"Routes implemented: {len(route_files)} files")
                            self.organization_score += 3
                    
                except Exception as e:
                    print(f"      Error analyzing {folder}: {e}")
            else:
                print(f"   {folder}/: MISSING - {description}")
        
        if mvc_present >= 3:
            self.strengths.append("Good MVC structure implementation")
            self.organization_score += 10
        elif mvc_present >= 2:
            self.organization_score += 5
    
    def analyze_database_integration(self, folders, files):
        """Analyze database integration"""
        print(f"\n DATABASE INTEGRATION ANALYSIS:")
        print("-" * 50)
        
        # Check for database configuration
        db_files = [f for f in files if any(db in f.lower() for db in ['database', 'db', 'postgres', 'sql'])]
        config_files = [f for f in files if 'config' in f.lower()]
        
        print(f" Database-related files: {len(db_files)}")
        print(f" Configuration files: {len(config_files)}")
        
        # Check for database setup files
        setup_files = ['setup_postgresql.bat', 'create_database.bat']
        found_setup = [f for f in setup_files if f in files]
        
        if found_setup:
            print(f" Database setup files: PRESENT")
            self.strengths.append("Database setup automation present")
            self.organization_score += 5
            print(f"   Found: {', '.join(found_setup)}")
        
        # Check for documentation
        db_docs = [f for f in files if 'postgresql' in f.lower() or 'database' in f.lower()]
        if db_docs:
            print(f" Database documentation: PRESENT")
            self.strengths.append("Database documentation present")
            self.organization_score += 3
            print(f"   Found: {', '.join(db_docs)}")
        
        # Check for sample data
        sample_files = [f for f in files if 'sample' in f.lower() or 'populate' in f.lower()]
        if sample_files:
            print(f" Sample data files: PRESENT")
            self.strengths.append("Sample data population present")
            self.organization_score += 3
            print(f"   Found: {', '.join(sample_files)}")
    
    def analyze_api_structure(self, folders):
        """Analyze API structure"""
        print(f"\n API STRUCTURE ANALYSIS:")
        print("-" * 50)
        
        # Check for API-related folders
        api_folders = ["routes", "controllers", "middleware"]
        api_present = [f for f in api_folders if f in folders]
        
        print(f" API structure folders: {len(api_present)}/{len(api_folders)}")
        
        if "routes" in folders:
            routes_path = self.base_path / "routes"
            try:
                route_files = list(routes_path.iterdir())
                print(f"   Route files: {len(route_files)}")
                
                # Look for medical imaging specific routes
                medical_routes = []
                for route_file in route_files:
                    if route_file.is_file():
                        name = route_file.name.lower()
                        if any(medical in name for medical in ['patient', 'doctor', 'study', 'image', 'medical']):
                            medical_routes.append(route_file.name)
                
                if medical_routes:
                    print(f"   Medical imaging routes: {len(medical_routes)}")
                    self.strengths.append(f"Medical imaging API routes: {len(medical_routes)}")
                    self.organization_score += 5
                    print(f"      {', '.join(medical_routes)}")
                
            except Exception as e:
                print(f"   Error analyzing routes: {e}")
        
        # Check for middleware
        if "middleware" in folders:
            middleware_path = self.base_path / "middleware"
            try:
                middleware_files = list(middleware_path.iterdir())
                print(f"   Middleware files: {len(middleware_files)}")
                
                if len(middleware_files) > 0:
                    self.strengths.append("Middleware implementation present")
                    self.organization_score += 3
                
            except Exception as e:
                print(f"   Error analyzing middleware: {e}")
    
    def analyze_documentation(self, files):
        """Analyze documentation files"""
        print(f"\n DOCUMENTATION ANALYSIS:")
        print("-" * 50)
        
        # Check for documentation files
        doc_files = [f for f in files if f.endswith('.md')]
        
        print(f" Documentation files: {len(doc_files)}")
        
        if len(doc_files) >= 3:
            print(f"   Documentation: EXCELLENT")
            self.strengths.append("Excellent documentation coverage")
            self.organization_score += 5
        elif len(doc_files) >= 1:
            print(f"   Documentation: GOOD")
            self.organization_score += 3
        else:
            print(f"   Documentation: MISSING")
            self.issues.append("No documentation files")
        
        # Show key documentation files
        key_docs = ['README.md', 'DEPLOYMENT_GUIDE.md', 'POSTGRESQL_CONNECTION.md']
        found_docs = [doc for doc in key_docs if doc in files]
        
        if found_docs:
            print(f"   Key docs found: {', '.join(found_docs)}")
        
        # Check for Postman collection
        if 'Medical_Imaging_API.postman_collection.json' in files:
            print(f"   Postman collection: PRESENT")
            self.strengths.append("API testing collection present")
            self.organization_score += 5
    
    def calculate_organization_score(self):
        """Calculate final organization score"""
        print(f"\n ORGANIZATION SCORE CALCULATION:")
        print("-" * 50)
        
        # Cap the score at max_score
        if self.organization_score > self.max_score:
            self.organization_score = self.max_score
        
        percentage = (self.organization_score / self.max_score) * 100
        
        # Grade
        if percentage >= 90:
            grade = "A+ (Excellent)"
            assessment = "Excellent organization, ready for production"
        elif percentage >= 80:
            grade = "A (Very Good)"
            assessment = "Very good organization, minor improvements needed"
        elif percentage >= 70:
            grade = "B (Good)"
            assessment = "Good organization, some improvements recommended"
        elif percentage >= 60:
            grade = "C (Fair)"
            assessment = "Fair organization, significant improvements needed"
        else:
            grade = "D (Poor)"
            assessment = "Poor organization, restructuring required"
        
        print(f"Score: {self.organization_score}/{self.max_score} ({percentage:.1f}%)")
        print(f"Grade: {grade}")
        print(f"Assessment: {assessment}")
    
    def generate_recommendations(self):
        """Generate improvement recommendations"""
        print(f"\n RECOMMENDATIONS:")
        print("-" * 50)
        
        if len(self.issues) > 0:
            print(" Priority Issues to Address:")
            for i, issue in enumerate(self.issues[:5], 1):
                print(f"   {i}. {issue}")
        
        if len(self.strengths) > 0:
            print(f"\n Current Strengths:")
            for i, strength in enumerate(self.strengths[:5], 1):
                print(f"   {i}. {strength}")
        
        print(f"\n Suggested Improvements:")
        
        # Specific recommendations based on common Express.js best practices
        recommendations = [
            "Ensure all MVC folders are present and properly structured",
            "Implement proper error handling middleware",
            "Add comprehensive API documentation",
            "Set up proper environment configuration",
            "Implement database connection pooling",
            "Add API validation and sanitization",
            "Implement proper logging system",
            "Add comprehensive testing suite",
            "Set up proper security measures",
            "Implement rate limiting and caching"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
        print(f"\n NEXT STEPS:")
        print("   1. Address critical missing MVC components")
        print("   2. Implement proper API structure")
        print("   3. Set up comprehensive testing")
        print("   4. Add security middleware")
        print("   5. Optimize for production deployment")
    
    def save_report(self):
        """Save analysis report"""
        report_data = {
            "score": self.organization_score,
            "max_score": self.max_score,
            "strengths": self.strengths,
            "issues": self.issues,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.base_path / "backend_organization_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\nReport saved to: backend_organization_report.json")

if __name__ == "__main__":
    analyzer = BackendOrganizationAnalyzer()
    analyzer.analyze_current_structure()
    analyzer.save_report()
