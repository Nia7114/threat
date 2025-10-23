#!/usr/bin/env python3
"""
TTPXHunter Integrated System Launcher
Starts the Flask backend and serves the web frontend as a static site.

Backend: Flask (app.py) -> http://localhost:5000
Frontend: Python http.server -> http://localhost:8000/index.html
"""

import os
import sys
import time
import subprocess
from pathlib import Path
import signal
import threading

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

def start_static_frontend(port: int = 8000):
    """Start a simple static file server for the web frontend."""
    print("🎨 Starting static web frontend server...")
    try:
        frontend_process = subprocess.Popen([
            sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1'
        ], cwd=Path(__file__).parent)
        print(f"✅ Frontend server started: http://localhost:{port}/index.html")
        return frontend_process
    except Exception as e:
        print(f"❌ Failed to start static frontend server: {e}")
        return None

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📋 Checking dependencies...")

    # Map package names to their import names
    package_imports = {
        'flask': 'flask',
        'flask-cors': 'flask_cors',
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
        time.sleep(2)
        
        # Start static web frontend
        frontend_process = start_static_frontend(port=8000)
        if not frontend_process:
            print("❌ Cannot start frontend")
            if backend_process:
                backend_process.terminate()
            sys.exit(1)
        
        print("\n🎉 TTPXHunter System Started Successfully!")
        print("📊 Backend API: http://localhost:5000")
        print("🖥️  Frontend UI: http://localhost:8000/index.html")
        print("🔗 Integration: Frontend (static) ↔ Backend API")
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
                print("ℹ️  Frontend server stopped")
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
