#!/usr/bin/env python3
"""
Focused Analysis of Project Folders
Exclude venv and node_modules, focus on actual project structure
"""

import os
from pathlib import Path

def analyze_project_folders():
    """Analyze only the actual project folders, not dependencies"""
    print("FOCUSED PROJECT FOLDER ANALYSIS")
    print("=" * 50)
    print("Excluding venv, node_modules, and hidden folders")
    print("=" * 50)
    
    # Get only project directories (exclude venv, node_modules, hidden folders)
    project_dirs = []
    exclude_patterns = ['venv', '.venv', 'node_modules', '__pycache__', '.git']
    
    for item in os.listdir('.'):
        if os.path.isdir(item) and not any(pattern in item for pattern in exclude_patterns):
            project_dirs.append(item)
    
    # Sort directories
    project_dirs.sort()
    
    print(f"\n📁 Project Directories Found: {len(project_dirs)}")
    
    folder_analysis = {}
    
    for dir_name in project_dirs:
        dir_path = dir_name
        
        try:
            # Count files and subdirectories
            all_items = os.listdir(dir_path)
            files = [f for f in all_items if os.path.isfile(os.path.join(dir_path, f))]
            subdirs = [d for d in all_items if os.path.isdir(os.path.join(dir_path, d))]
            
            # Filter out dependency folders from subdirs
            subdirs = [d for d in subdirs if not any(pattern in d for pattern in exclude_patterns)]
            
            # Check for important file types
            important_extensions = ['.js', '.py', '.json', '.md', '.txt', '.env', '.sql', '.yaml', '.yml']
            important_files = [f for f in files if any(f.endswith(ext) for ext in important_extensions)]
            
            # Determine importance
            total_items = len(files) + len(subdirs)
            
            if total_items == 0:
                importance = "USELESS - Empty"
            elif len(important_files) == 0 and total_items < 3:
                importance = "LOW - No important files"
            elif len(important_files) >= 3 or total_items >= 10:
                importance = "IMPORTANT - Contains valuable files"
            else:
                importance = "MEDIUM - Some content"
            
            folder_analysis[dir_name] = {
                'file_count': len(files),
                'dir_count': len(subdirs),
                'total_items': total_items,
                'important_files': important_files,
                'importance': importance
            }
            
        except PermissionError:
            folder_analysis[dir_name] = {
                'file_count': 0,
                'dir_count': 0,
                'total_items': 0,
                'important_files': [],
                'importance': "ACCESS DENIED"
            }
    
    # Categorize folders
    useless_folders = []
    low_importance = []
    important_folders = []
    
    for folder, analysis in folder_analysis.items():
        if "USELESS" in analysis['importance']:
            useless_folders.append(folder)
        elif "LOW" in analysis['importance']:
            low_importance.append(folder)
        else:
            important_folders.append(folder)
    
    # Display results
    print(f"\n📊 Analysis Results:")
    print(f"  Total project folders: {len(folder_analysis)}")
    print(f"  Useless folders: {len(useless_folders)}")
    print(f"  Low importance: {len(low_importance)}")
    print(f"  Important folders: {len(important_folders)}")
    
    # Show useless folders
    if useless_folders:
        print(f"\n🗑️ USELESS FOLDERS (should be removed):")
        for folder in useless_folders:
            print(f"  - {folder}")
    
    # Show low importance folders
    if low_importance:
        print(f"\n⚠️ LOW IMPORTANCE FOLDERS (consider consolidating):")
        for folder in low_importance:
            analysis = folder_analysis[folder]
            print(f"  - {folder} ({analysis['total_items']} items)")
            if analysis['important_files']:
                print(f"    Files: {', '.join(analysis['important_files'][:3])}")
    
    # Show important folders
    if important_folders:
        print(f"\n✅ IMPORTANT FOLDERS (keep these):")
        for folder in important_folders:
            analysis = folder_analysis[folder]
            print(f"  - {folder} ({analysis['total_items']} items, {len(analysis['important_files'])} important files)")
    
    return {
        'useless': useless_folders,
        'low_importance': low_importance,
        'important': important_folders,
        'analysis': folder_analysis
    }

def suggest_replacements():
    """Suggest replacements for useless folders"""
    print(f"\n💡 REPLACEMENT SUGGESTIONS:")
    print("=" * 50)
    
    suggestions = [
        {
            'useless': 'Empty folders',
            'replace_with': 'Remove completely',
            'reason': 'Empty folders serve no purpose'
        },
        {
            'useless': 'Folders with 1-2 unimportant files',
            'replace_with': 'Consolidate into parent folders',
            'reason': 'Better organization and easier navigation'
        },
        {
            'useless': 'Vague folder names',
            'replace_with': 'Descriptive names based on content',
            'reason': 'Clearer purpose and better maintainability'
        }
    ]
    
    for suggestion in suggestions:
        print(f"• {suggestion['useless']} → {suggestion['replace_with']}")
        print(f"  Reason: {suggestion['reason']}")
        print()

if __name__ == "__main__":
    analysis = analyze_project_folders()
    suggest_replacements()
    
    print(f"🎯 READY TO OPTIMIZE FOLDER STRUCTURE")
