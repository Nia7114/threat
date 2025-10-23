#!/usr/bin/env python3
"""
Test script to verify backend API and web frontend presence without starting external processes.
Uses Flask's test client for backend checks and validates the index.html file for UI hooks.
"""

import os
import sys
from pathlib import Path
from typing import Tuple

from app import app

def test_backend_connection() -> bool:
    """Test backend endpoints using Flask test client."""
    print("🔧 Testing backend API (test client)...")
    try:
        with app.test_client() as c:
            r = c.get('/healthz')
            payload = r.get_json(silent=True) or {}
            assert r.status_code == 200 and payload.get('status') == 'ok'

            r = c.post('/api/scan')
            assert r.status_code == 200
            scan_results = r.get_json(silent=True) or []
            print(f"✅ /api/scan returned {len(scan_results)} threats")

            r = c.post('/api/mitigate', json={'threat_ids': [1, 2]})
            assert r.status_code == 200
            print("✅ /api/mitigate succeeded")

        # Basic SSE generator smoke test
        with app.test_request_context('/api/stream'):
            from app import stream_endpoint
            resp = stream_endpoint()
            gen = resp.response
            got_event = False
            for i, chunk in enumerate(gen):
                s = chunk.decode() if isinstance(chunk, (bytes, bytearray)) else str(chunk)
                if 'event: threat' in s:
                    got_event = True
                    break
                if i > 50:
                    break
            assert got_event, "No threat event seen in SSE stream sample"
            print("✅ /api/stream yields threat events")
        return True
    except AssertionError as e:
        print(f"❌ Backend assertion failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend_presence() -> bool:
    """Validate that the web frontend file exists and includes live monitor hooks."""
    print("\n🎨 Testing web frontend presence...")
    try:
        index_path = Path(__file__).parent / 'index.html'
        if not index_path.is_file():
            print("❌ index.html not found")
            return False
        content = index_path.read_text(encoding='utf-8')
        # Check for key UI elements introduced
        assert 'Start Live Monitor' in content
        assert '/api/stream' in content
        assert '/api/scan' in content
        print("✅ index.html contains required UI and API references")
        return True
    except AssertionError as e:
        print(f"❌ Frontend content assertion failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 TTPXHunter Integration Test")
    print("=" * 40)
    
    # Test backend
    backend_ok = test_backend_connection()
    
    # Test frontend presence
    frontend_ok = test_frontend_presence()
    
    print("\n📊 Test Results:")
    print(f"   Backend API: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"   Frontend Integration: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Integration test PASSED!")
        print("💡 You can now run the integrated system:")
        print("   python3 run_integrated_system.py")
        return 0
    else:
        print("\n❌ Integration test FAILED!")
        if not backend_ok:
            print("💡 Install Flask: python3 -m pip install flask flask-cors")
        if not frontend_ok:
            print("💡 Ensure index.html exists at project root")
        return 1

if __name__ == "__main__":
    sys.exit(main())
