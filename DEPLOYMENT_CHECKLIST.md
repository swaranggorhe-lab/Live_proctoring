# Windows Deployment Checklist

## Pre-Deployment (Office Computer Preparation)

- [ ] Windows 10 or Windows 11 installed
- [ ] Internet connection available
- [ ] Administrator access to the computer
- [ ] At least 2GB free disk space
- [ ] At least 4GB RAM (8GB+ recommended)

## Download & Extract

- [ ] Download Python 3.10+ installer from https://www.python.org/downloads/
- [ ] Download Node.js 14+ from https://nodejs.org/
- [ ] Extract `live_proctoring` folder to desired location (e.g., `C:\Users\YourName\Documents\`)

## Install Python

- [ ] Run Python installer
- [ ] ✅ **CHECK**: "Add Python to PATH"
- [ ] ✅ **CHECK**: "Install pip"
- [ ] Click "Install Now"
- [ ] Restart computer (recommended)

## Install Node.js

- [ ] Run Node.js installer
- [ ] ✅ **CHECK**: "npm package manager"
- [ ] Click "Next" through prompts
- [ ] Click "Install"
- [ ] Restart computer (recommended)

## Verify Installations

Open Command Prompt and run:

```cmd
python --version
npm --version
node --version
```

Should show version numbers (not "command not found").

- [ ] Python version ≥ 3.10
- [ ] npm version ≥ 6.0
- [ ] Node version ≥ 14.0

## Setup Backend

Open Command Prompt and navigate to backend:

```cmd
cd C:\path\to\live_proctoring\backend
setup_env.bat
```

Wait for completion (might take 5-10 minutes for first-time installation).

- [ ] setup_env.bat completed without errors
- [ ] See "✅ Setup complete!" message
- [ ] `backend_env\` folder created
- [ ] `backend_env\Lib\site-packages\` has dependencies

## Verify Model Files

Check that these files exist in `backend\models\`:

- [ ] `yolov8n.pt` (exists)
- [ ] `deploy.prototxt` (exists)
- [ ] `res10_300x300_ssd_iter_140000.caffemodel` (exists)

If missing, download from:
- YOLOv8: https://github.com/ultralytics/assets/releases
- SSD: https://github.com/opencv/opencv_3rdparty

## Test Backend Startup

Open Command Prompt in `backend\` and run:

```cmd
start_server.bat
```

Watch for these messages:

- [ ] "🚀 Starting Live Proctoring Backend..."
- [ ] "✅ All services initialized successfully"
- [ ] "Uvicorn running on http://0.0.0.0:8000"
- [ ] "DNN model loaded" or similar
- [ ] No error messages

**Don't close this window!** Let it run.

## Test Backend Health

Open another Command Prompt and run:

```cmd
curl http://127.0.0.1:8000/api/health
```

Should see JSON response with:
- [ ] `"status": "healthy"`
- [ ] `"models": { ... }`
- [ ] `"database": "ok"`

## Setup Frontend

Open a new Command Prompt in `frontend\`:

```cmd
cd C:\path\to\live_proctoring\frontend
npm install
```

Wait for completion (might take 5-10 minutes).

- [ ] npm install completed without errors
- [ ] `node_modules\` folder created
- [ ] No "ERR!" messages

## Test Frontend Startup

In the same frontend Command Prompt, run:

```cmd
npm start
```

Watch for:

- [ ] "webpack compiled successfully"
- [ ] "Compiled successfully!"
- [ ] Browser opens to `http://localhost:3000`

If browser doesn't open:
- [ ] Manually open http://localhost:3000 in Chrome/Firefox

## Test System

In the browser:

- [ ] Page loads without errors
- [ ] "Allow camera access" prompt appears
- [ ] Click "Allow"
- [ ] See webcam video on page
- [ ] No red error messages

## Verify Frame Streaming

In backend Command Prompt, you should see:

- [ ] "📥 Frame from [client_id]" messages appearing
- [ ] Status shows frame count increasing
- [ ] No "Error" or "Exception" messages

## Verify Detection

In the browser:

- [ ] Canvas overlay shows face box (if face visible)
- [ ] Colors indicate detection status:
  - Green = face detected, looking straight
  - Orange = looking away
  - Gold = face out of box
  - Red = phone detected

## Test Warning System

Once system detects a violation:

- [ ] Warning counter shows "⚠️ Warnings: 1/3"
- [ ] Frame snapshot saved (check `backend\data\evidence\`)
- [ ] WebSocket message received in browser console (F12)

## Final Checks

- [ ] Both backend and frontend terminals showing active logs
- [ ] No repeated error messages
- [ ] Database file exists: `backend\proctoring.db`
- [ ] Evidence directory exists: `backend\data\evidence\`
- [ ] Configuration can be adjusted with sliders
- [ ] Session can be ended and restarted

## Shutdown Procedure

When done testing:

1. **Close browser** or go to `http://localhost:3000/api/session/end?client_id=test`
2. **Stop frontend**: Press `Ctrl+C` in frontend terminal
3. **Stop backend**: Press `Ctrl+C` in backend terminal
4. **Verify**: No "Address already in use" errors next time

## Documentation

After successful setup, read:

- [ ] `README.md` - System overview
- [ ] `WINDOWS_SETUP.md` - Detailed Windows guide
- [ ] `USAGE_GUIDE.md` - How to use the system
- [ ] `QUICK_START_WINDOWS.txt` - Quick reference

## Troubleshooting Reference

| Issue | Check |
|-------|-------|
| "python not found" | Python not in PATH, reinstall |
| "npm not found" | Node.js not in PATH, reinstall |
| "Port 8000 in use" | Another app using port, kill process or change port |
| "Connection refused" | Backend not running, run `start_server.bat` |
| "Models not found" | Files missing from `backend\models\` folder |
| "Camera not working" | Windows privacy settings, grant app permission |
| "WebSocket connection failed" | Backend not running or firewall blocking |

## Support

If issues occur:

1. Check `WINDOWS_SETUP.md` → Troubleshooting section
2. Check Command Prompt error messages
3. Check backend log: `type %TEMP%\proctoring_server.log`
4. Delete database and try again: `del backend\proctoring.db`

---

## Sign-Off

- [ ] System setup completed successfully
- [ ] All tests passed
- [ ] Documentation reviewed
- [ ] Ready for office computer deployment

**Date Completed**: _______________  
**Tested By**: _______________  
**System Status**: ✅ Ready for Production

---

**Version**: 1.0  
**Last Updated**: December 8, 2025
