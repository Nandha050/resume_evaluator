#!/usr/bin/env python3
"""
Final cleanup script before committing to GitHub
"""

import os
import shutil

def final_cleanup():
    """Final cleanup before commit"""
    print("🧹 FINAL CLEANUP FOR GITHUB COMMIT")
    print("=" * 50)
    
    # Files to remove
    files_to_remove = [
        "__pycache__",
        "src/__pycache__",
        "src/matching/__pycache__",
        "src/models/__pycache__",
        "src/parsers/__pycache__",
        "src/scoring/__pycache__",
        "src/utils/__pycache__",
        "resume_evaluation.db",
        "final_cleanup.py"  # Remove this script itself
    ]
    
    removed_count = 0
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"🗑️ Removed directory: {file_path}")
            else:
                os.remove(file_path)
                print(f"🗑️ Removed file: {file_path}")
            removed_count += 1
    
    print(f"\n✅ Cleanup complete! Removed {removed_count} items")
    
    # Show final structure
    print("\n📋 FINAL PROJECT STRUCTURE:")
    print("=" * 40)
    
    important_files = [
        "streamlit_app.py",
        "dashboard.py", 
        "main.py",
        "requirements_streamlit.txt",
        "packages.txt",
        "runtime.txt",
        ".streamlit/config.toml",
        "DEPLOYMENT_GUIDE.md",
        "README.md",
        "env_example.txt",
        ".gitignore",
        "src/",
        "tests/",
        "data/uploads/"
    ]
    
    for file_path in important_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
    
    print("\n🚀 READY FOR GITHUB COMMIT!")
    print("=" * 40)
    print("Run these commands:")
    print("git add .")
    print("git commit -m 'Ready for Streamlit Cloud deployment'")
    print("git push origin main")

if __name__ == "__main__":
    final_cleanup()
