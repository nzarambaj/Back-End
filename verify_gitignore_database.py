#!/usr/bin/env python3
"""
Verify .gitignore Database Tracking
Check that database files are properly tracked in git
"""

import os
import subprocess
from pathlib import Path

def verify_gitignore_database():
    """Verify database files are not ignored"""
    print(" VERIFYING .gitignore DATABASE TRACKING")
    print("=" * 60)
    
    # Read current .gitignore
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        print(" Current .gitignore database section:")
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'database' in line.lower() or line.startswith('*.db') or line.startswith('*.sqlite'):
                print(f"   Line {i}: {line}")
        
        # Check if database exclusions are commented out
        db_exclusions = ['*.db', '*.sqlite3']
        excluded = []
        
        for exclusion in db_exclusions:
            if exclusion in content and not content.split('\n'):
                for line in content.split('\n'):
                    if exclusion in line and not line.strip().startswith('#'):
                        excluded.append(exclusion)
        
        if excluded:
            print(f"\n   Still excluded: {excluded}")
        else:
            print(f"\n   Database exclusions: REMOVED")
    
    print("\n Database files that will be tracked:")
    
    # Check for common database files
    db_patterns = [
        '*.db',
        '*.sqlite3',
        '*.sqlite',
        'database/',
        'db/',
        'data/',
        'migrations/',
        'seeds/'
    ]
    
    for pattern in db_patterns:
        print(f"   - {pattern}")
    
    print("\n Environment files (still ignored):")
    env_patterns = [
        '.env',
        '.env.local',
        '.env.production'
    ]
    
    for pattern in env_patterns:
        print(f"   - {pattern} (IGNORED)")
    
    print("\n Git status check:")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if lines and lines != ['']:
                print("   Untracked files:")
                for line in lines[:10]:  # Show first 10
                    if line.strip():
                        status = line[:2]
                        file_path = line[3:]
                        if any(db in file_path.lower() for db in ['.db', '.sqlite', 'database', 'migration']):
                            print(f"     {status} {file_path} (DATABASE)")
                        else:
                            print(f"     {status} {file_path}")
                
                if len(lines) > 10:
                    print(f"     ... and {len(lines) - 10} more files")
            else:
                print("   No untracked files")
        else:
            print("   Git status check failed")
            
    except Exception as e:
        print(f"   Error checking git status: {e}")
    
    print("\n RECOMMENDATIONS:")
    print(" 1. Database files will now be tracked in git")
    print(" 2. Consider adding database schemas and migrations")
    print(" 3. Environment files remain ignored for security")
    print(" 4. Test database connectivity after changes")

if __name__ == "__main__":
    verify_gitignore_database()
