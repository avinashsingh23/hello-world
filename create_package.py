#!/usr/bin/env python3
"""
Create a downloadable package of the Concertiv Travel Ops Portal
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_package():
    """Create a ZIP package with all necessary files"""
    
    package_name = f"concertiv-travel-ops-portal-{datetime.now().strftime('%Y%m%d')}.zip"
    
    # Files to include in the package
    files_to_include = [
        # Main application files
        'app.py',
        'requirements.txt', 
        'init_db.py',
        'demo.py',
        'interact.py',
        
        # Documentation
        'README.md',
        'LOCAL_SETUP_GUIDE.md',
        'DOWNLOAD_INSTRUCTIONS.md',
        'DEPLOYMENT_SUMMARY.md',
        
        # Setup scripts
        'setup.bat',
        'setup.sh', 
        'start.bat',
        'start.sh',
        
        # Demo file
        'demo.html'
    ]
    
    # Directories to include
    directories_to_include = [
        'templates',
        'static'
    ]
    
    print("📦 Creating Concertiv Travel Ops Portal Package...")
    print("=" * 50)
    
    try:
        with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add individual files
            for file_name in files_to_include:
                if os.path.exists(file_name):
                    zipf.write(file_name)
                    print(f"✅ Added: {file_name}")
                else:
                    print(f"⚠️  Missing: {file_name}")
            
            # Add directories
            for dir_name in directories_to_include:
                if os.path.exists(dir_name):
                    for root, dirs, files in os.walk(dir_name):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path)
                            print(f"✅ Added: {file_path}")
                else:
                    print(f"⚠️  Missing directory: {dir_name}")
        
        # Get package size
        package_size = os.path.getsize(package_name)
        size_mb = package_size / (1024 * 1024)
        
        print(f"\n🎉 Package created successfully!")
        print(f"📦 File: {package_name}")
        print(f"📏 Size: {size_mb:.2f} MB")
        print(f"📍 Location: {os.path.abspath(package_name)}")
        
        print(f"\n📋 Package Contents:")
        print(f"   • Complete Flask application")
        print(f"   • HTML templates with Bootstrap 5 UI")
        print(f"   • CSS and JavaScript files") 
        print(f"   • Database initialization scripts")
        print(f"   • Setup and start scripts for Windows/Linux/macOS")
        print(f"   • Complete documentation")
        print(f"   • Sample data (13 TMCs, hotel audit data)")
        
        print(f"\n🚀 Ready for local deployment!")
        print(f"   Extract the ZIP file and run setup.bat (Windows) or ./setup.sh (Linux/macOS)")
        
        return package_name
        
    except Exception as e:
        print(f"❌ Error creating package: {str(e)}")
        return None

def list_package_contents():
    """List all files that would be included in the package"""
    
    print("📋 Concertiv Travel Ops Portal - File Inventory")
    print("=" * 50)
    
    # Count lines of code
    total_lines = 0
    
    # Main Python files
    python_files = ['app.py', 'init_db.py', 'demo.py', 'interact.py']
    for file_name in python_files:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
                total_lines += lines
                print(f"📄 {file_name}: {lines} lines")
    
    # Template files
    template_dir = 'templates'
    if os.path.exists(template_dir):
        template_lines = 0
        template_files = os.listdir(template_dir)
        for file_name in template_files:
            file_path = os.path.join(template_dir, file_name)
            if file_name.endswith('.html'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    template_lines += lines
                    print(f"🌐 templates/{file_name}: {lines} lines")
        total_lines += template_lines
    
    # Static files
    static_files = ['static/css/style.css', 'static/js/app.js']
    for file_path in static_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
                total_lines += lines
                print(f"🎨 {file_path}: {lines} lines")
    
    print(f"\n📊 Total Code: {total_lines:,} lines")
    print(f"🎯 Complete full-stack web application ready for deployment!")

if __name__ == '__main__':
    print("🎯 Concertiv Travel Ops Portal - Package Creator")
    print("=" * 50)
    
    # List contents first
    list_package_contents()
    
    print("\n" + "=" * 50)
    
    # Create package
    package_file = create_package()
    
    if package_file:
        print(f"\n✨ SUCCESS! Package ready for download and local deployment.")
    else:
        print(f"\n❌ Package creation failed.")