#!/usr/bin/env python3
"""
Analyze Redundant Files in Project_BackEnd
Identify duplicate and unnecessary files to reduce from 151 to manageable number
"""

import os
import hashlib
from pathlib import Path

def get_file_hash(file_path):
    """Get hash of file content for duplicate detection"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def analyze_redundant_files():
    """Analyze all files to identify redundancies"""
    print("ANALYZING REDUNDANT FILES IN PROJECT_BACKEND")
    print("=" * 60)
    print("Current file count: 151+ files - need to reduce")
    print("=" * 60)
    
    # Get all files in main folders
    main_folders = ["01_api", "02_services", "03_utils", "04_deployment"]
    all_files = []
    file_hashes = {}
    
    for folder in main_folders:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, '.')
                    
                    # Skip hidden files and cache files
                    if file.startswith('.') or file.endswith('.pyc'):
                        continue
                    
                    file_size = os.path.getsize(file_path)
                    file_hash = get_file_hash(file_path)
                    
                    file_info = {
                        'path': relative_path,
                        'full_path': file_path,
                        'name': file,
                        'size': file_size,
                        'hash': file_hash,
                        'folder': folder
                    }
                    
                    all_files.append(file_info)
                    
                    # Track duplicates by hash
                    if file_hash:
                        if file_hash not in file_hashes:
                            file_hashes[file_hash] = []
                        file_hashes[file_hash].append(file_info)
    
    print(f"\n📊 File Analysis Results:")
    print(f"  Total files analyzed: {len(all_files)}")
    print(f"  Unique files: {len(file_hashes)}")
    print(f"  Potential duplicates: {len(all_files) - len(file_hashes)}")
    
    # Identify duplicates
    duplicates = {hash_val: files for hash_val, files in file_hashes.items() if len(files) > 1}
    
    # Identify file types and patterns
    file_types = {}
    for file_info in all_files:
        ext = os.path.splitext(file_info['name'])[1].lower()
        if ext not in file_types:
            file_types[ext] = []
        file_types[ext].append(file_info)
    
    # Identify potentially unnecessary files
    unnecessary_patterns = [
        '.pyc', '.log', '.tmp', '.bak', '.old', '.orig',
        'test_', 'debug_', 'temp_', 'backup_',
        'copy_', 'duplicate_', 'sample_'
    ]
    
    unnecessary_files = []
    for file_info in all_files:
        file_name = file_info['name'].lower()
        if any(pattern in file_name for pattern in unnecessary_patterns):
            unnecessary_files.append(file_info)
    
    # Show duplicates
    if duplicates:
        print(f"\n🔄 DUPLICATE FILES (can be removed):")
        for hash_val, dup_files in duplicates.items():
            if len(dup_files) > 1:
                print(f"  Duplicate group ({len(dup_files)} files):")
                for i, file_info in enumerate(dup_files):
                    status = "KEEP" if i == 0 else "REMOVE"
                    print(f"    {status}: {file_info['path']}")
    
    # Show file types distribution
    print(f"\n📁 FILE TYPES DISTRIBUTION:")
    for ext, files in sorted(file_types.items()):
        print(f"  {ext or 'no extension'}: {len(files)} files")
        
        # Show large files of each type
        large_files = [f for f in files if f['size'] > 100000]  # > 100KB
        if large_files:
            print(f"    Large files (>100KB): {len(large_files)}")
            for f in large_files[:3]:  # Show top 3
                print(f"      {f['name']}: {f['size']/1024:.1f}KB")
    
    # Show unnecessary files
    if unnecessary_files:
        print(f"\n🗑️ UNNECESSARY FILES (can be removed):")
        for file_info in unnecessary_files:
            print(f"  {file_info['path']} ({file_info['size']/1024:.1f}KB)")
    
    # Identify similar files by name pattern
    similar_groups = {}
    for file_info in all_files:
        base_name = file_info['name'].lower()
        # Remove common prefixes/suffixes for grouping
        for prefix in ['test_', 'debug_', 'temp_', 'backup_', 'copy_']:
            if base_name.startswith(prefix):
                base_name = base_name[len(prefix):]
        for suffix in ['_backup', '_old', '_orig', '_tmp', '_bak']:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]
        
        if base_name not in similar_groups:
            similar_groups[base_name] = []
        similar_groups[base_name].append(file_info)
    
    # Show similar file groups
    similar_to_remove = []
    for base_name, files in similar_groups.items():
        if len(files) > 1:
            print(f"\n📋 SIMILAR FILES - {base_name}:")
            for i, file_info in enumerate(sorted(files, key=lambda x: x['size'], reverse=True)):
                status = "KEEP" if i == 0 else "REMOVE"
                if i > 0:
                    similar_to_remove.append(file_info)
                print(f"    {status}: {file_info['path']} ({file_info['size']/1024:.1f}KB)")
    
    return {
        'total_files': len(all_files),
        'unique_files': len(file_hashes),
        'duplicates': duplicates,
        'unnecessary_files': unnecessary_files,
        'similar_to_remove': similar_to_remove,
        'file_types': file_types
    }

def suggest_removal_plan(analysis):
    """Suggest which files to remove"""
    print(f"\n💡 FILE REMOVAL SUGGESTIONS:")
    print("=" * 60)
    
    # Count files to remove
    duplicates_to_remove = []
    for dup_files in analysis['duplicates'].values():
        duplicates_to_remove.extend(dup_files[1:])  # Keep first, remove rest
    
    total_to_remove = (
        len(analysis['unnecessary_files']) + 
        len(analysis['similar_to_remove']) + 
        len(duplicates_to_remove)
    )
    
    print(f"🎯 REMOVAL PLAN:")
    print(f"  Current files: {analysis['total_files']}")
    print(f"  Duplicate files to remove: {len(duplicates_to_remove)}")
    print(f"  Unnecessary files to remove: {len(analysis['unnecessary_files'])}")
    print(f"  Similar files to remove: {len(analysis['similar_to_remove'])}")
    print(f"  Total files to remove: {total_to_remove}")
    print(f"  Expected final count: {analysis['total_files'] - total_to_remove}")
    
    # Create removal list
    files_to_remove = []
    files_to_remove.extend(duplicates_to_remove)
    files_to_remove.extend(analysis['unnecessary_files'])
    files_to_remove.extend(analysis['similar_to_remove'])
    
    return files_to_remove

if __name__ == "__main__":
    analysis = analyze_redundant_files()
    files_to_remove = suggest_removal_plan(analysis)
    
    print(f"\n📄 Ready to remove {len(files_to_remove)} redundant files")
    print(f"🎯 This will reduce from {analysis['total_files']} to {analysis['total_files'] - len(files_to_remove)} files")
