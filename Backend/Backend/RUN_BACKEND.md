# 🚀 Quick Start - Run Backend

## ✅ All Issues Fixed!

All necessary files are present and configured correctly.

---

## 🔧 Prerequisites Checklist

Before running, ensure:

- [ ] **Python 3.10+** installed
- [ ] **MySQL Server** running on localhost
- [ ] **Database `user_auth`** exists in MySQL
- [ ] **Port 5000** is available

---

## ▶️ Run Backend (3 Steps)

### Step 1: Open PowerShell
```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Backend\Backend"
```

### Step 2: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install/Update Dependencies & Run
```powershell
pip install -r requirements.txt
python app.py
```

---

## 🎯 Alternative: Use Startup Script

The easiest way to run the backend:

```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Backend\Backend"
.\start_backend.ps1
```

This script will:
1. Check Python installation
2. Create/activate virtual environment
3. Install all dependencies
4. Start the Flask server

---

## ✅ Success Indicators

When running successfully, you'll see:
```
================================================================================
*** STARTING MEDIRAG BACKEND SERVER ***
================================================================================

Server Configuration:
   Host: 0.0.0.0
   Port: 5000
   Debug: True
================================================================================

 * Running on http://0.0.0.0:5000
```

---

## 🧪 Test the Backend

Once running, open a new terminal and test:

```powershell
# Test health endpoint
curl http://localhost:5000/api/health

# Test domains endpoint
curl http://localhost:5000/api/domains
```

---

## ⚠️ Common Issues

### Issue: MySQL Connection Error
**Solution:** Ensure MySQL is running and database `user_auth` exists
```sql
CREATE DATABASE IF NOT EXISTS user_auth;
```

### Issue: Port 5000 Already in Use
**Solution:** Kill the process using port 5000 or change port in `app.py`
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue: Import Errors
**Solution:** Reinstall dependencies
```powershell
pip install -r requirements.txt --force-reinstall
```

---

## 📊 What Was Fixed

1. ✅ Added missing dependencies:
   - `mysql-connector-python`
   - `python-dotenv`
   - `rank-bm25`
   - `nltk`

2. ✅ Fixed PyTorch version (2.9.0 → 2.5.1)

3. ✅ Fixed checkpoint directory path detection

---

## 🌐 Backend Endpoints

Once running, the following endpoints will be available:

- `POST http://localhost:5000/api/ask` - Main RAG query
- `GET http://localhost:5000/api/health` - Health check
- `GET http://localhost:5000/api/domains` - Available medical domains
- `GET http://localhost:5000/api/chat/sessions/<user_id>` - Get chat sessions
- `POST http://localhost:5000/api/chat/save` - Save chat message
- `DELETE http://localhost:5000/api/chat/sessions/<session_id>` - Delete session

---

## 📝 Notes

- **First run takes 10-30 minutes** (downloads ~10GB of ML models)
- Backend runs on **http://0.0.0.0:5000**
- Accessible from **http://localhost:5000**
- **5 medical domains** available: Cancer, Cardiology, Dermatology, Diabetes-Digestive-Kidney, Neurology
