#!/usr/bin/env python3
"""
Test script to verify frontend-backend integration
"""

import requests
import json
import time
import sys

def test_backend_connection():
    """Test if backend server is running and responding"""
    print("🔧 Testing backend connection...")
    
    try:
        # Test scan endpoint
        response = requests.post('http://localhost:5000/api/scan', timeout=10)
        
        if response.status_code == 200:
            scan_results = response.json()
            print(f"✅ Backend scan endpoint working: {len(scan_results)} threats returned")
            
            # Test mitigation endpoint if we have threats
            if scan_results:
                threat_ids = [threat['id'] for threat in scan_results[:2]]  # Test with first 2 threats
                
                mitigation_response = requests.post(
                    'http://localhost:5000/api/mitigate',
                    json={'threat_ids': threat_ids},
                    timeout=10
                )
                
                if mitigation_response.status_code == 200:
                    mitigation_result = mitigation_response.json()
                    print(f"✅ Backend mitigation endpoint working: {mitigation_result.get('message', 'Success')}")
                    return True
                else:
                    print(f"❌ Mitigation endpoint failed: {mitigation_response.status_code}")
                    return False
            else:
                print("⚠️  No threats returned from scan, but endpoint is working")
                return True
        else:
            print(f"❌ Backend scan endpoint failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("💡 Make sure Flask backend is running: python app.py")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend_backend_integration():
    """Test the integration by running a quick frontend test"""
    print("\n🎨 Testing frontend-backend integration...")
    
    try:
        # Import the dashboard to test integration
        from ui.dashboard_window import ModernDashboard
        
        print("✅ Frontend can import backend integration modules")
        
        # Create dashboard instance (without showing GUI)
        import os
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # Headless mode
        
        from PyQt6 import QtWidgets
        app = QtWidgets.QApplication(sys.argv)
        
        dashboard = ModernDashboard()
        
        # Test backend configuration
        if hasattr(dashboard, 'backend_config'):
            print(f"✅ Backend configuration loaded: {dashboard.backend_config['base_url']}")
        
        if hasattr(dashboard, 'check_backend_connection'):
            print("✅ Backend connection check method available")
        
        if hasattr(dashboard, 'make_api_request'):
            print("✅ API request method available")
        
        if hasattr(dashboard, 'start_backend_scan'):
            print("✅ Backend scan integration available")
        
        if hasattr(dashboard, 'start_backend_mitigation'):
            print("✅ Backend mitigation integration available")
        
        app.quit()
        print("✅ Frontend-backend integration test completed")
        return True
        
    except ImportError as e:
        print(f"❌ Frontend import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Frontend integration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 TTPXHunter Integration Test")
    print("=" * 40)
    
    # Test backend
    backend_ok = test_backend_connection()
    
    # Test frontend integration
    frontend_ok = test_frontend_backend_integration()
    
    print("\n📊 Test Results:")
    print(f"   Backend API: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"   Frontend Integration: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Integration test PASSED!")
        print("💡 You can now run the integrated system:")
        print("   python run_integrated_system.py")
        return 0
    else:
        print("\n❌ Integration test FAILED!")
        if not backend_ok:
            print("💡 Start the backend first: python app.py")
        if not frontend_ok:
            print("💡 Check frontend dependencies: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
