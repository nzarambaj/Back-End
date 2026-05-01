#!/usr/bin/env python3
"""
Check Again for Remaining Redundant Files
Final verification after removing 29 redundant files
"""

import os
import hashlib
from pathlib import Path

def check_remaining_redundant():
    """Check for any remaining redundant files"""
    print("CHECKING AGAIN FOR REMAINING REDUNDANT FILES")
    print("=" * 60)
    print("Final verification after reducing from 151 to 122 files")
    print("=" * 60)
    
    # Get all files in current structure
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
                    if file.startswith('.') or file.endswith('.pyc') or '__pycache__' in file_path:
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
    
    print(f"\n📊 Current File Analysis:")
    print(f"  Total files: {len(all_files)}")
    print(f"  Unique files: {len(file_hashes)}")
    
    # Check for duplicates
    duplicates = {hash_val: files for hash_val, files in file_hashes.items() if len(files) > 1}
    
    # Check for potentially unnecessary files
    unnecessary_patterns = [
        'test_', 'debug_', 'temp_', 'backup_', 'copy_', 'duplicate_',
        'sample_', 'example_', 'demo_', 'old_', 'orig_', 'bak_',
        'tmp_', 'temp', 'backup', 'old', 'orig', 'bak', 'tmp'
    ]
    
    potentially_unnecessary = []
    for file_info in all_files:
        file_name = file_info['name'].lower()
        if any(pattern in file_name for pattern in unnecessary_patterns):
            potentially_unnecessary.append(file_info)
    
    # Check for very small files (likely empty or placeholder)
    very_small_files = [f for f in all_files if f['size'] < 100]  # < 100 bytes
    
    # Check for very large files that might be unnecessary
    very_large_files = [f for f in all_files if f['size'] > 1000000]  # > 1MB
    
    # Show results
    print(f"\n🔄 REMAINING DUPLICATES:")
    if duplicates:
        for hash_val, dup_files in duplicates.items():
            if len(dup_files) > 1:
                print(f"  Duplicate group ({len(dup_files)} files):")
                for i, file_info in enumerate(dup_files):
                    status = "KEEP" if i == 0 else "REMOVE"
                    print(f"    {status}: {file_info['path']}")
    else:
        print("  No duplicates found")
    
    print(f"\n⚠️ POTENTIALLY UNNECESSARY FILES:")
    if potentially_unnecessary:
        for file_info in potentially_unnecessary:
            print(f"  {file_info['path']} ({file_info['size']} bytes)")
    else:
        print("  No obviously unnecessary files found")
    
    print(f"\n📏 VERY SMALL FILES (<100 bytes):")
    if very_small_files:
        for file_info in very_small_files:
            print(f"  {file_info['path']} ({file_info['size']} bytes)")
    else:
        print("  No very small files found")
    
    print(f"\n📦 VERY LARGE FILES (>1MB):")
    if very_large_files:
        for file_info in very_large_files:
            print(f"  {file_info['path']} ({file_info['size']/1024/1024:.1f}MB)")
    else:
        print("  No very large files found")
    
    # File type analysis
    file_types = {}
    for file_info in all_files:
        ext = os.path.splitext(file_info['name'])[1].lower()
        if ext not in file_types:
            file_types[ext] = []
        file_types[ext].append(file_info)
    
    print(f"\n📁 FILE TYPE DISTRIBUTION:")
    for ext, files in sorted(file_types.items()):
        print(f"  {ext or 'no extension'}: {len(files)} files")
    
    return {
        'total_files': len(all_files),
        'duplicates': duplicates,
        'unnecessary': potentially_unnecessary,
        'small_files': very_small_files,
        'large_files': very_large_files,
        'file_types': file_types
    }

def get_file_hash(file_path):
    """Get hash of file content for duplicate detection"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def suggest_final_optimizations(analysis):
    """Suggest any final optimizations"""
    print(f"\n💡 FINAL OPTIMIZATION SUGGESTIONS:")
    print("=" * 60)
    
    suggestions = []
    
    if analysis['duplicates']:
        suggestions.append(f"Remove {len(analysis['duplicates'])} duplicate file groups")
    
    if analysis['unnecessary']:
        suggestions.append(f"Review {len(analysis['unnecessary'])} potentially unnecessary files")
    
    if analysis['small_files']:
        suggestions.append(f"Review {len(analysis['small_files'])} very small files (may be empty)")
    
    if analysis['large_files']:
        suggestions.append(f"Review {len(analysis['large_files'])} large files (may contain unnecessary data)")
    
    if not suggestions:
        suggestions.append("File structure appears well optimized")
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")
    
    return suggestions

def generate_final_verification_report(analysis, suggestions):
    """Generate final verification report"""
    report = {
        "verification_type": "Final Redundant File Check",
        "project": "Project_BackEnd",
        "timestamp": str(Path(__file__).stat().st_mtime),
        "current_status": {
            "total_files": analysis['total_files'],
            "duplicates": len(analysis['duplicates']),
            "unnecessary_files": len(analysis['unnecessary']),
            "small_files": len(analysis['small_files']),
            "large_files": len(analysis['large_files'])
        },
        "optimization_results": {
            "original_count": 151,
            "current_count": analysis['total_files'],
            "files_removed": 151 - analysis['total_files'],
            "reduction_percentage": ((151 - analysis['total_files']) / 151) * 100
        },
        "final_suggestions": suggestions,
        "status": "Optimized" if len(suggestions) <= 2 else "Needs Review"
    }
    
    with open("final_redundant_check.json", "w") as f:
        import json
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Final verification report saved to: final_redundant_check.json")

if __name__ == "__main__":
    analysis = check_remaining_redundant()
    suggestions = suggest_final_optimizations(analysis)
    
    generate_final_verification_report(analysis, suggestions)
    
    print(f"\n🎯 FINAL VERIFICATION COMPLETE")
    print(f"✅ Current file count: {analysis['total_files']}")
    print(f"✅ Reduction from 151: {151 - analysis['total_files']} files")
    print(f"✅ Optimization percentage: {((151 - analysis['total_files']) / 151) * 100:.1f}%")
