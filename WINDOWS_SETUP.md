# Live Proctoring System - Windows Setup Guide

## Prerequisites

1. **Python 3.10+** - Download from [python.org](https://www.python.org/downloads/)
2. **Git** (optional) - For cloning the repository
3. **Windows 10/11** - Latest updates recommended
4. **Administrator Access** - For initial setup

## Installation Steps

### 1. Initial Setup (One-time)

Run the setup batch file from Command Prompt (Admin):

```cmd
cd path\to\live_proctoring\backend
setup_env.bat
```

This will:
- Create a Python virtual environment
- Install all required dependencies from `requirements.txt`
- Verify installations

### 2. Starting the Backend Server

```cmd
cd path\to\live_proctoring\backend
start_server.bat
```

The server will start on `http://0.0.0.0:8000`

Log file: `%TEMP%\proctoring_server.log`

### 3. Starting the Frontend (Separate Terminal)

```cmd
cd path\to\live_proctoring\frontend
npm start
```

Frontend will open on `http://localhost:3000`

## Running Tests

### Test Backend API

```cmd
cd path\to\live_proctoring\backend
backend_env\Scripts\python.exe test_api.py
```

### Test Detection with Real Images

```cmd
cd path\to\live_proctoring\backend
backend_env\Scripts\python.exe ..\test_real_images.py
```

## Training YOLOv8 Model (Optional)

To train a custom detection model:

```cmd
cd path\to\live_proctoring\backend\training
train_yolo.bat
```

Or with custom parameters:

```cmd
cd path\to\live_proctoring\backend\training
train_yolo.bat "data_template.yaml" "yolov8n.pt" "50" "auto"
```

Arguments:
- `data_template.yaml` - Dataset configuration
- `yolov8n.pt` - Model size
- `50` - Number of epochs
- `auto` - Device (auto/0/1/cuda/cpu)

## Directory Structure

```
live_proctoring/
├── backend/
│   ├── start_server.bat        ← Start server (Windows)
│   ├── setup_env.bat           ← Setup environment (Windows)
│   ├── requirements.txt        ← Python dependencies
│   ├── app/
│   │   ├── main.py            ← FastAPI server
│   │   ├── detector.py        ← AI detection logic
│   │   ├── db.py              ← Database handling
│   │   └── utils.py           ← Utilities
│   ├── models/                ← Pre-trained models
│   ├── data/evidence/         ← Violation evidence storage
│   ├── training/              ← Training scripts
│   └── backend_env/           ← Python virtual environment (auto-created)
│
└── frontend/
    ├── src/
    │   ├── App.js             ← React main component
    │   ├── App.css            ← Styling
    │   └── utils.js           ← Frontend utilities
    ├── package.json
    └── public/
```

## Troubleshooting

### Virtual Environment Issues

If you see "python is not recognized":

```cmd
REM Manually create venv
python -m venv path\to\live_proctoring\backend\backend_env

REM Activate it
path\to\live_proctoring\backend\backend_env\Scripts\activate.bat

REM Then install dependencies
pip install -r requirements.txt
```

### Port 8000 Already in Use

Change the port in `start_server.bat`:
```bat
%PYTHON_BIN% -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

And update frontend to connect to port 8001 in `App.js`:
```javascript
const WS_URL = `ws://127.0.0.1:8001/ws/${clientId}`;
```

### Models Not Found

Ensure these files exist in `backend/models/`:
- `yolov8n.pt`
- `deploy.prototxt`
- `res10_300x300_ssd_iter_140000.caffemodel`

If missing, download from:
- [YOLOv8 Models](https://github.com/ultralytics/assets/releases)
- [SSD Face Detection](https://github.com/opencv/opencv_3rdparty/tree/dnn_samples_face_detector_20170830)

### Database Issues

If you see database errors, delete the old database and let it recreate:

```cmd
cd path\to\live_proctoring\backend
del proctoring.db
```

The database will be recreated on next server start with fresh schema.

## Cross-Platform Notes

All paths in the codebase use `os.path.join()` for cross-platform compatibility:
- Database paths are relative (no `/tmp/` hardcoding)
- Model paths use `Path(__file__).resolve()`
- Evidence storage uses OS-appropriate paths (`data\evidence\`)

## Useful Commands

### Check if Server is Running

```cmd
netstat -ano | findstr :8000
```

### Kill Server Process

```cmd
taskkill /F /IM python.exe
```

### View Server Logs

```cmd
type %TEMP%\proctoring_server.log
```

### Check Python Version

```cmd
backend_env\Scripts\python.exe --version
```

## Next Steps

1. Run `setup_env.bat` to create the environment
2. Run `start_server.bat` to start the backend
3. In another terminal, run `npm start` in the frontend folder
4. Open your browser to `http://localhost:3000`
5. Start a proctoring session!

## Contact Support

For issues specific to Windows deployment, check:
- Event Viewer for system errors
- Python package compatibility (some packages require Visual C++ build tools)
- Antivirus/Firewall settings for port 8000

---

**Last Updated**: December 8, 2025
**Python Version**: 3.10+
**OS**: Windows 10/11
