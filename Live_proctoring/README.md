# Live Proctoring System

A comprehensive, production-ready online proctoring system built with Python FastAPI backend and React frontend. Detects and logs student violations during exams including tab switching, multiple face detection, and suspicious activities.

## 🚀 Features

- **Real-time Face Detection**: Multiple detection engines (YOLOv8, RetinaFace, MediaPipe, DNN)
- **Tab Switch Detection**: Monitors and logs when students switch tabs/windows
- **Full Frame Monitoring**: Continuous camera feed analysis
- **Offline Ready**: Works completely offline after initial setup
- **Database Logging**: All violations logged to SQLite with evidence images
- **3-Warning System**: Auto-end session after 3 warnings with 8-second grace period
- **Windows & macOS Support**: Platform-agnostic deployment scripts
- **Evidence Annotation**: Violation evidence saved as JPG with detection boxes and confidence scores

## �� System Requirements

### Windows (Office Target)
- Windows 10/11 (64-bit)
- Python 3.8+ 
- 4GB RAM minimum (6GB+ recommended)
- 2GB free disk space
- Webcam/camera device

### macOS
- macOS 10.14+
- Python 3.8+
- 4GB RAM minimum
- 2GB free disk space
- Webcam/camera device

## 🔧 Quick Start - Windows

### Step 1: Extract Files
```bash
# Extract live_proctoring.zip to your desired location
# Example: C:\Users\YourName\live_proctoring
```

### Step 2: Start Backend
```bash
# Double-click: START_BACKEND.bat
```

### Step 3: Start Frontend
```bash
# Double-click: START_FRONTEND.bat
```

### Step 4: Access System
```
Open browser: http://localhost:3000
```

## 🔧 Quick Start - macOS

### Step 1: Extract Files
```bash
unzip live_proctoring.zip
cd live_proctoring
```

### Step 2: Start Everything
```bash
chmod +x START_ALL.sh
./START_ALL.sh
```

## 📁 Project Structure

```
live_proctoring/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI server + WebSocket
│   │   ├── detector.py      # Multi-detector integration
│   │   ├── db.py            # Database operations
│   │   └── utils.py         # Utility functions
│   ├── models/              # Pre-trained models
│   ├── data/evidence/       # Evidence images
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   └── utils.js         # Frontend utilities
│   └── package.json         # Dependencies
│
├── START_BACKEND.bat        # Windows backend launcher
├── START_FRONTEND.bat       # Windows frontend launcher
├── START_ALL.sh             # macOS launcher
├── proctoring.db            # SQLite database (auto-created)
└── README.md                # This file
```

## 🎯 Usage

1. **Start Session**: Enter student ID and click "Start Session"
2. **Grant Camera Access**: Allow camera permission when prompted
3. **Monitoring**: System monitors:
   - Tab switching
   - Face presence and count
   - Suspicious activities
4. **Warnings**: 3-warning limit with auto-end

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```

### Tab Switch Detection
```
POST /api/tab_switch?client_id=ID&state=hidden|visible
```

### Session Info
```
GET /api/session/summary?client_id=ID
```

### Violations Report
```
GET /api/violations?client_id=ID&v_type=tab_switch
```

## 🐛 Troubleshooting

### Backend Won't Start
```bash
python --version  # Should be 3.8+
netstat -ano | findstr :8000  # Windows - check port 8000
```

### Frontend Won't Start
```bash
node --version  # Should be 14+
cd frontend && npm install
```

### Camera Not Working
- Grant browser camera permission
- Try different browser (Chrome/Edge recommended)
- Check camera not in use by another app

### Frames Not Sending
- Verify backend running: `curl http://127.0.0.1:8000/api/health`
- Check browser console (F12) for errors
- Review backend terminal for error logs

## 📊 Database

All violations stored in SQLite: `proctoring.db`

**Tables:**
- `sessions`: Client ID, warning count, session status
- `violations`: Violation type, timestamp, evidence path, details

## 🔒 Security

- **Offline**: Works completely offline (no cloud calls)
- **Local Storage**: Data stored locally only
- **Evidence**: Images stored with timestamps
- **No External Dependencies**: All processing local

## 📝 Logging

**Backend**: Check terminal window for real-time logs
**Frontend**: Browser console (F12) shows connection status

## 📄 For Detailed Setup

See `README_OFFICE_SETUP.md` for comprehensive office deployment guide covering:
- Requirements
- Step-by-step setup
- Troubleshooting (11 solutions)
- API documentation
- Performance optimization
- Security notes

## 📄 License

Proprietary. All rights reserved.

## 👨‍💻 Author

Live Proctoring Development Team  
Version: 1.0.0  
Updated: December 2025
