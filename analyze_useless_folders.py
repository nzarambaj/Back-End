#!/usr/bin/env python3
"""
Analyze Useless Folders in Project_BackEnd
Identify folders that should be replaced with meaningful ones
"""

import os
from pathlib import Path

def analyze_folder_importance():
    """Analyze which folders are useful vs useless"""
    print("ANALYZING FOLDER IMPORTANCE IN PROJECT_BACKEND")
    print("=" * 60)
    
    # Get all directories
    all_dirs = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for d in dirs:
            dir_path = os.path.join(root, d)
            all_dirs.append(dir_path)
    
    # Analyze each directory
    folder_analysis = {}
    
    for dir_path in all_dirs:
        # Count files and subdirectories
        file_count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
        dir_count = len([d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))])
        
        # Check for important file types
        important_files = []
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    if file.endswith(('.js', '.py', '.json', '.md', '.txt', '.env', '.sql')):
                        important_files.append(file)
        
        # Determine importance
        total_items = file_count + dir_count
        has_important_files = len(important_files) > 0
        
        # Categorize folder
        if total_items == 0:
            importance = "USELESS - Empty"
        elif not has_important_files and file_count < 3:
            importance = "LOW - Few unimportant files"
        elif has_important_files or file_count >= 5:
            importance = "IMPORTANT - Contains valuable files"
        else:
            importance = "MEDIUM - Some content"
        
        folder_analysis[dir_path] = {
            'file_count': file_count,
            'dir_count': dir_count,
            'total_items': total_items,
            'important_files': important_files,
            'importance': importance
        }
    
    # Sort folders by importance
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
    print(f"\n📊 Folder Analysis Results:")
    print(f"  Total folders analyzed: {len(folder_analysis)}")
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
    
    # Show important folders
    if important_folders:
        print(f"\n✅ IMPORTANT FOLDERS (keep these):")
        for folder in important_folders[:10]:  # Show first 10
            analysis = folder_analysis[folder]
            print(f"  - {folder} ({analysis['total_items']} items, {len(analysis['important_files'])} important files)")
        
        if len(important_folders) > 10:
            print(f"  ... and {len(important_folders) - 10} more")
    
    return {
        'useless': useless_folders,
        'low_importance': low_importance,
        'important': important_folders,
        'analysis': folder_analysis
    }

def suggest_folder_optimization():
    """Suggest optimizations for folder structure"""
    print(f"\n💡 FOLDER OPTIMIZATION SUGGESTIONS:")
    print("=" * 60)
    
    suggestions = [
        "1. Remove completely empty folders",
        "2. Consolidate folders with < 3 files into parent directories",
        "3. Merge similar functionality folders",
        "4. Create meaningful folder names that describe purpose",
        "5. Keep only folders with substantial content or specific purpose"
    ]
    
    for suggestion in suggestions:
        print(f"  {suggestion}")
    
    print(f"\n🎯 RECOMMENDED ACTIONS:")
    print(f"  • Remove empty folders to clean up structure")
    print(f"  • Consolidate small folders into logical groups")
    print(f"  • Rename vague folders to be more descriptive")
    print(f"  • Keep folders that serve specific backend purposes")

if __name__ == "__main__":
    analysis = analyze_folder_importance()
    suggest_folder_optimization()
    
    print(f"\n📄 Analysis complete. Ready to optimize folder structure.")
