# 🚀 Quick Start Guide - Medical RAG

## Prerequisites Check

- ✅ **Node.js v22.18.0** - Installed
- ✅ **npm v11.6.1** - Installed  
- ⚠️ **Python 3.10+** - **NOT INSTALLED** → [Download Here](https://www.python.org/downloads/)

## Step 1: Install Python (Required)

1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. ✅ Check **"Add Python to PATH"** during installation
3. Restart terminal
4. Verify: `python --version`

## Step 2: Start Backend (Terminal 1)

```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Backend\Backend"
.\start_backend.ps1
```

Wait for:
```
✅ Medical RAG backend is running successfully
 * Running on http://0.0.0.0:5000
```

## Step 3: Start Frontend (Terminal 2)

```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Frontend"
.\start_frontend.ps1
```

## Step 4: Open Browser

Navigate to: **http://localhost:5173**

## First Time Setup

⏳ **Expect 20-30 minutes for:**
- Python packages installation
- ML models download (~10GB)
- Medical datasets loading

## Test Questions

Try these in the UI:
- "What causes chest pain?"
- "What are symptoms of diabetes?"
- "How to prevent infections?"
- "Explain heart disease"

## Troubleshooting

### PowerShell Script Error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python Not Found
1. Restart terminal after Python installation
2. Try `py` instead of `python`

### Backend Not Responding
- Check Terminal 1 for errors
- Ensure port 5000 is free
- Wait for model loading to complete

## Quick Help

📖 **Full Documentation**: `SETUP_INSTRUCTIONS.md`
📋 **Setup Status**: `SETUP_COMPLETE.md`
🔧 **Backend Server**: http://localhost:5000
🌐 **Frontend UI**: http://localhost:5173

---

**⚡ After Python is installed, you're 2 commands away from success!**
