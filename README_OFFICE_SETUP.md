# Live Proctoring System - Office Deployment Guide

## System Requirements

### Minimum Requirements:
- **OS**: Windows 7+ or macOS 10.12+
- **RAM**: 4GB
- **Storage**: 1GB free space
- **Processor**: Intel Core i5 or equivalent
- **Camera**: USB or built-in webcam

### Software Requirements:
- **Python 3.8+** (Download from: https://www.python.org/downloads/)
- **Node.js 14+** (Download from: https://nodejs.org/)
- **Modern web browser**: Chrome, Firefox, Safari, or Edge

---

## Quick Start Guide

### Option 1: Windows (Recommended for Office)

#### Step 1: Install Python and Node.js
1. Download Python from https://www.python.org/downloads/
   - **IMPORTANT**: Check "Add Python to PATH" during installation
2. Download Node.js from https://nodejs.org/ (LTS version)
3. Verify installations by opening Command Prompt and typing:
   ```
   python --version
   node --version
   ```

#### Step 2: Start the System
1. Extract the `live_proctoring.zip` to your desired location
2. Open two Command Prompt windows in the extracted folder
3. **Window 1 - Backend Server**:
   - Double-click `START_BACKEND.bat`
   - Wait until you see: `Uvicorn running on http://127.0.0.1:8000`
4. **Window 2 - Frontend**:
   - Double-click `START_FRONTEND.bat`
   - Browser will automatically open http://localhost:3000
5. Allow camera access when prompted

#### Step 3: Use the System
1. Enter a Student ID (or keep the default)
2. Click "Start Session"
3. Allow camera access
4. System will automatically:
   - Capture frames every 500ms
   - Detect violations (looking away, phone, multiple faces, etc.)
   - Issue warnings (max 3 per session)
   - Log all data to database

#### Step 4: Stop the System
- Press `Ctrl+C` in both Command Prompt windows
- Or close the windows

---

### Option 2: macOS

#### Step 1: Install Python and Node.js
```bash
# Using Homebrew (https://brew.sh/)
brew install python@3.11
brew install node
```

#### Step 2: Start the System
```bash
# Terminal 1: Backend
cd /path/to/live_proctoring
source backend/backend_env/bin/activate
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend
cd /path/to/live_proctoring/frontend
npm start
```

---

## System Architecture

### Backend (FastAPI - Python)
- **Location**: `backend/` folder
- **Port**: 8000
- **Purpose**: Video analysis, violation detection, database logging
- **Database**: SQLite (`proctoring.db`)

### Frontend (React - JavaScript)
- **Location**: `frontend/` folder
- **Port**: 3000
- **Purpose**: Camera capture, user interface, session management

### Communication
```
Frontend (Localhost:3000)
    ↓
WebSocket (ws://127.0.0.1:8000/ws/{clientId})
    ↓
Backend (127.0.0.1:8000)
    ↓
SQLite Database (proctoring.db)
```

---

## Features & Behavior

### Violation Types Detected:
1. **Looking Away** - Student looking away from screen
2. **Face Out of Box** - Face outside allowed area
3. **No Face** - No face detected in frame
4. **Multiple Persons** - More than one person detected
5. **Prohibited Items** - Phone or other items detected

### Warning System:
- **Grace Period**: 8 seconds between warnings
- **Max Warnings**: 3 per session
- **Auto Session End**: Session automatically ends after 3rd warning
- **Persistence**: Requires 2+ consecutive frames to trigger warning

### Tab Switching:
- Monitored via HTTP endpoint
- Issues warning if student leaves the tab (hidden/blur states)
- Triggers when visibility changes

### Database Logging:
- All violations logged with timestamp
- Evidence images stored with annotations
- Session summary with violation counts
- All data queryable via API endpoints

---

## Troubleshooting

### Issue: "Python not found" or "node not found"
**Solution**:
- Restart after installing Python/Node
- Ensure "Add to PATH" was checked during installation
- Run `python --version` to verify

### Issue: Port 8000 or 3000 already in use
**Solution**:
- Find and close other applications using these ports
- Or modify port numbers in scripts (advanced)

### Issue: Camera access denied
**Solution**:
- Check browser permissions
- Allow camera access when prompted
- Restart browser if permission was previously denied

### Issue: No frames being captured
**Solution**:
- Check browser console (F12) for errors
- Ensure WebSocket is connecting (should see "Connected" status)
- Try refreshing the page
- Check backend logs for "Frame from" messages

### Issue: Database locked error
**Solution**:
- Close all instances of the application
- Delete `proctoring.db` (will recreate on next start)
- Restart the system

---

## API Endpoints

### Session Management
- `POST /api/session/start?client_id=XXXX` - Start new session
- `POST /api/session/end?client_id=XXXX` - End session and get summary
- `POST /api/session/rebind?new_client_id=XXXX` - Rebind session

### Violation Tracking
- `GET /api/violations/{client_id}` - Get all violations for a client
- `POST /api/tab_switch?client_id=XXXX&state=hidden` - Report tab switch

### Reports
- `GET /api/report/{client_id}` - Get session report
- `GET /api/health` - System health check

---

## File Structure

```
live_proctoring/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main API server
│   │   ├── detector.py     # Detection logic
│   │   ├── db.py           # Database operations
│   │   └── utils.py        # Utilities
│   ├── models/             # Pre-trained models
│   ├── data/               # Session data & evidence
│   ├── requirements.txt    # Python dependencies
│   └── backend_env/        # Virtual environment
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Styling
│   │   └── index.js       # Entry point
│   ├── package.json       # Dependencies
│   └── node_modules/      # Installed packages
│
├── START_BACKEND.bat      # Windows backend startup
├── START_FRONTEND.bat     # Windows frontend startup
└── proctoring.db         # SQLite database (created on first run)
```

---

## Performance Optimization

For office environments with limited resources:

1. **Reduce Frame Rate**: Modify `captureFrames()` timeout from 500ms to 1000ms
2. **Lower Video Quality**: Change `ideal` resolution in `startVideoCapture()`
3. **Disable Annotations**: Remove bounding box drawing in detector
4. **Database**: Clear old sessions periodically: `DELETE FROM sessions WHERE created_at < date('now', '-30 days')`

---

## Security Notes

1. **Local Network Only**: System runs on localhost (127.0.0.1)
2. **Database**: Not exposed to internet
3. **Client IDs**: Generated randomly - not tied to student names
4. **Evidence Images**: Stored locally in `data/evidence/` folder

---

## Support & Logs

### Viewing Logs:
- **Backend**: Check the backend command prompt window (shows all "Frame from", violations, warnings)
- **Frontend**: Open browser console (F12) and check for JavaScript errors
- **Database**: Queries available via API endpoints

### Debugging:
- Backend logs show frame reception, detection results, and database operations
- Frontend console shows WebSocket connection status and frame sending
- Check `proctoring.db` using SQLite viewer for raw data

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Blank video feed | Restart browser, check camera permissions |
| No detections | Ensure good lighting, camera is properly positioned |
| Warnings not recording | Check backend logs for "persisted to DB" messages |
| Session won't end | Reload page, check if warning_count reached 3 in database |
| Slow performance | Reduce frame rate, lower resolution, close other apps |

---

## Technical Support

For issues or questions:
1. Check the logs in the command prompt windows
2. Review browser console (F12)
3. Verify Python and Node versions match requirements
4. Ensure ports 8000 and 3000 are available
5. Check internet connection (should work offline)

---

## Version Information
- **System Version**: 1.0
- **Last Updated**: December 2025
- **Tested On**: Windows 10/11, macOS 12+
