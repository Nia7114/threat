#!/usr/bin/env python3
"""
TTPXHunter Integrated System Launcher
Starts both the Flask backend and PyQt6 frontend with proper integration
"""

import os
import sys
import time
import subprocess
import threading
import signal
from pathlib import Path

def start_backend():
    """Start the Flask backend server"""
    print("🔧 Starting Flask backend server...")
    try:
        # Start Flask app
        backend_process = subprocess.Popen([
            sys.executable, 'app.py'
        ], cwd=Path(__file__).parent)
        
        print("✅ Backend server started successfully")
        return backend_process
    except Exception as e:
        print(f"❌ Failed to start backend server: {e}")
        return None

def start_frontend():
    """Start the PyQt6 frontend"""
    print("🎨 Starting PyQt6 frontend...")
    try:
        # Start frontend
        frontend_process = subprocess.Popen([
            sys.executable, 'ui/dashboard_window.py'
        ], cwd=Path(__file__).parent)
        
        print("✅ Frontend started successfully")
        return frontend_process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📋 Checking dependencies...")

    # Map package names to their import names
    package_imports = {
        'flask': 'flask',
        'flask-cors': 'flask_cors',
        'requests': 'requests',
        'PyQt6': 'PyQt6'
    }

    missing_packages = []

    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required dependencies are installed")
    return True

def main():
    """Main launcher function"""
    print("🚀 TTPXHunter Integrated System Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend server
        backend_process = start_backend()
        if not backend_process:
            print("❌ Cannot start system without backend")
            sys.exit(1)
        
        # Wait for backend to start
        print("⏳ Waiting for backend to initialize...")
        time.sleep(3)
        
        # Start frontend
        frontend_process = start_frontend()
        if not frontend_process:
            print("❌ Cannot start frontend")
            if backend_process:
                backend_process.terminate()
            sys.exit(1)
        
        print("\n🎉 TTPXHunter System Started Successfully!")
        print("📊 Backend API: http://localhost:5000")
        print("🖥️  Frontend GUI: PyQt6 Dashboard")
        print("🔗 Integration: Frontend ↔ Backend API")
        print("\n💡 Features Available:")
        print("   • Real-time threat scanning via backend API")
        print("   • Threat mitigation through backend services")
        print("   • Complete 20-step dashboard functionality")
        print("   • Search and filter with backend data")
        print("   • Export/download with real scan results")
        print("\n⚠️  Press Ctrl+C to stop both services")
        
        # Wait for processes to complete
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("ℹ️  Frontend closed by user")
                break
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n🛑 Shutting down TTPXHunter system...")
    
    finally:
        # Clean up processes
        if backend_process and backend_process.poll() is None:
            print("🔧 Stopping backend server...")
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()
        
        if frontend_process and frontend_process.poll() is None:
            print("🎨 Stopping frontend...")
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
        
        print("✅ TTPXHunter system stopped successfully")

if __name__ == "__main__":
    main()
