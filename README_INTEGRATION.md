# TTPXHunter Integrated System

## 🔗 Frontend-Backend Integration Complete!

The TTPXHunter Security System now features full integration between the PyQt6 frontend and Flask backend API.

## 🚀 Quick Start

### Option 1: Automated Launch (Recommended)
```bash
cd threat_app
python run_integrated_system.py
```

### Option 2: Manual Launch
**Terminal 1 (Backend):**
```bash
cd threat_app
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd threat_app
source venv/bin/activate
python ui/dashboard_window.py
```

## 📋 Prerequisites

### Install Dependencies
```bash
cd threat_app
pip install -r requirements.txt
```

### Required Packages
- `flask` - Backend API server
- `flask-cors` - Cross-origin resource sharing
- `requests` - HTTP client for API calls
- `PyQt6` - GUI framework
- `psutil` - System monitoring
- Other packages for ML and security features

## 🔧 Integration Features

### ✅ Real Backend API Calls
- **Threat Scanning**: Frontend calls `POST /api/scan` for real threat detection
- **Threat Mitigation**: Frontend calls `POST /api/mitigate` with threat IDs
- **Error Handling**: Graceful fallback to simulated data if backend unavailable
- **Threading**: Non-blocking API calls in background threads

### ✅ Smart Fallback System
- **Backend Available**: Uses real API responses
- **Backend Offline**: Shows warning and uses simulated data
- **Connection Monitoring**: Automatic backend status checking
- **User Notifications**: Clear feedback about backend status

### ✅ Data Flow Integration
```
PyQt6 Frontend ←→ HTTP Requests ←→ Flask Backend
     ↓                                    ↓
UI Components                        API Endpoints
Search/Filter                        /api/scan
Export/Download                      /api/mitigate
Notifications                        JSON Responses
```

## 🧪 Testing Integration

### Test Backend Connection
```bash
cd threat_app
python test_integration.py
```

### Manual API Testing
```bash
# Test scan endpoint
curl -X POST http://localhost:5000/api/scan

# Test mitigation endpoint
curl -X POST http://localhost:5000/api/mitigate \
  -H "Content-Type: application/json" \
  -d '{"threat_ids": [1, 2]}'
```

## 📊 System Architecture

### Backend (Flask API)
- **File**: `app.py`
- **Port**: 5000
- **Endpoints**:
  - `POST /api/scan` - Returns detected threats
  - `POST /api/mitigate` - Mitigates specified threats
- **Features**: CORS enabled, JSON responses, error handling

### Frontend (PyQt6 GUI)
- **File**: `ui/dashboard_window.py`
- **Features**: All 20 steps implemented with backend integration
- **API Client**: Built-in HTTP client with retry logic
- **Threading**: Non-blocking API calls

### Integration Layer
- **HTTP Requests**: `requests` library for API communication
- **Threading**: Background API calls to prevent UI freezing
- **Error Handling**: Graceful degradation when backend unavailable
- **Data Mapping**: Converts backend JSON to frontend data structures

## 🎯 Usage Examples

### 1. Start Integrated System
```bash
python run_integrated_system.py
```
- Starts both backend and frontend
- Shows connection status
- Handles graceful shutdown

### 2. Threat Scanning with Backend
1. Click "🔍 Start Security Scan" in frontend
2. Frontend calls backend API
3. Real threats returned from backend
4. Results displayed in modern UI

### 3. Threat Mitigation with Backend
1. Select threats in scan results
2. Click "🛡️ Mitigate Selected"
3. Frontend sends threat IDs to backend
4. Backend processes mitigation
5. Success/failure reported to frontend

## 🔍 Troubleshooting

### Backend Not Starting
```bash
# Check if port 5000 is available
lsof -i :5000

# Install Flask dependencies
pip install flask flask-cors
```

### Frontend Connection Issues
- Ensure backend is running on `http://localhost:5000`
- Check firewall settings
- Verify `requests` package is installed

### Integration Test Failures
```bash
# Run comprehensive test
python test_integration.py

# Check individual components
python app.py  # Test backend
python ui/dashboard_window.py  # Test frontend
```

## 📈 Performance Notes

- **API Calls**: Non-blocking with 30-second timeout
- **Retry Logic**: 3 attempts with 1-second delay
- **Threading**: Background workers for API operations
- **Fallback**: Immediate switch to simulated data if backend fails

## 🛡️ Security Features

- **CORS**: Properly configured for frontend-backend communication
- **Input Validation**: Backend validates all API inputs
- **Error Handling**: No sensitive information leaked in error messages
- **Timeout Protection**: Prevents hanging API calls

## 🎉 Complete Feature Set

With integration complete, the system now provides:

1. ✅ **Real Threat Detection** via backend API
2. ✅ **Actual Threat Mitigation** through backend services
3. ✅ **Live Data Integration** between frontend and backend
4. ✅ **Graceful Fallback** when backend unavailable
5. ✅ **Professional UI** with all 20 implemented features
6. ✅ **Search and Filter** with real backend data
7. ✅ **Export/Download** with actual scan results
8. ✅ **Real-time Notifications** for API operations
9. ✅ **Error Handling** and user feedback
10. ✅ **Production-Ready** architecture

The TTPXHunter Security System is now a fully integrated, production-ready cybersecurity application!
