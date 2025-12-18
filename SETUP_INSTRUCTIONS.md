# Medical RAG Full-Stack Setup Instructions

## Prerequisites

### Required Software
1. **Python 3.10 or higher** - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANT**: During installation, check "Add Python to PATH"
2. **Node.js v16 or higher** - ✅ Already installed (v22.18.0)
3. **npm** - ✅ Already installed (v11.6.1)

## Project Structure
```
medirag-ai-main/
├── Backend/Backend/
│   ├── app.py                    # Flask server (CREATED)
│   ├── medical_rag_colab.py      # Original RAG implementation
│   ├── requirements.txt          # Python dependencies (UPDATED)
│   └── venv/                     # Virtual environment (to be created)
└── Frontend/
    ├── src/
    ├── package.json
    ├── .env                      # Environment config (CREATED)
    └── node_modules/             # ✅ Already installed
```

## Backend Setup

### Step 1: Install Python
If Python is not installed, download and install from [python.org](https://www.python.org/downloads/)

Verify installation:
```powershell
python --version
# or
py --version
```

### Step 2: Create Virtual Environment
```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Backend\Backend"
python -m venv venv
```

### Step 3: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: This will download several large ML models (~10GB):
- sentence-transformers/all-MiniLM-L6-v2
- microsoft/BioGPT
- google/flan-t5-large
- jkhan447/t5-medical-text-simplification

The first run will take 20-30 minutes to download these models.

### Step 5: Run Backend Server
```powershell
python app.py
```

You should see:
```
🚀 Starting Medical RAG Backend...
🔄 Loading models and datasets...
📚 Loading medical datasets...
🔍 Building vector indexes...
✅ Medical RAG backend is running successfully
 * Running on http://0.0.0.0:5000
```

Keep this terminal open. The backend is now running on **http://localhost:5000**

## Frontend Setup

### Step 1: Navigate to Frontend Directory
Open a **NEW** terminal/PowerShell window:
```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Frontend"
```

### Step 2: Install Dependencies (Already Done)
✅ Dependencies are already installed. If needed:
```powershell
npm install
```

### Step 3: Verify Environment Configuration
✅ The `.env` file is already created with:
```
VITE_API_URL=http://localhost:5000
```

### Step 4: Start Frontend Development Server
```powershell
npm run dev
```

The React app will start on **http://localhost:5173** (Vite default) or another available port.

## Accessing the Application

1. **Backend API**: http://localhost:5000
2. **Frontend UI**: http://localhost:5173 (or the port shown in terminal)

## API Endpoints

### Health Check
```
GET http://localhost:5000/health
```

### Ask Medical Question
```
POST http://localhost:5000/ask
Content-Type: application/json

{
  "question": "What causes chest pain?"
}
```

Response:
```json
{
  "status": "success",
  "question": "What causes chest pain?",
  "answer": "Detailed medical answer...",
  "simplified_answer": "Simplified explanation...",
  "hypothesis": "HyDE hypothesis..."
}
```

## Troubleshooting

### Backend Issues

#### Python Not Found
**Error**: `python: command not found`
**Solution**: 
1. Install Python from python.org
2. Restart your terminal
3. Verify with `python --version`

#### Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'flask'`
**Solution**:
1. Ensure virtual environment is activated (you should see `(venv)` in terminal)
2. Run `pip install -r requirements.txt`

#### Model Download Failures
**Error**: Connection timeout or download errors
**Solution**:
1. Check internet connection
2. Clear HuggingFace cache: Delete `~/.cache/huggingface/`
3. Retry: `python app.py`

#### Port Already in Use
**Error**: `Address already in use: Port 5000`
**Solution**:
1. Find process using port: `netstat -ano | findstr :5000`
2. Kill process: `taskkill /PID <process_id> /F`
3. Or change port in `app.py`: `app.run(port=5001)`

### Frontend Issues

#### CORS Errors
**Error**: CORS policy blocking requests
**Solution**: 
✅ Already handled! The Flask backend includes CORS middleware.

#### Environment Variables Not Loading
**Error**: API calls going to wrong URL
**Solution**:
1. Verify `.env` file exists in Frontend directory
2. Restart the dev server: Stop with Ctrl+C, then `npm run dev`
3. Ensure variable starts with `VITE_` prefix

#### Port Already in Use
**Error**: Port 5173 is already in use
**Solution**:
Vite will automatically use the next available port (5174, 5175, etc.)

## Testing the Setup

### 1. Test Backend Health
Open browser or use curl:
```powershell
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "initialized": true
}
```

### 2. Test Medical Query
```powershell
curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d "{\"question\": \"What is hypertension?\"}"
```

### 3. Test Frontend
1. Open http://localhost:5173 in browser
2. You should see the Medical RAG interface
3. Try asking a medical question

## Medical Domains Supported

The RAG system supports queries in these medical domains:
- 🫀 **Cardiology**: Heart diseases, blood pressure, cardiac conditions
- 🧠 **Neurology**: Brain, nervous system, strokes, seizures
- 🩺 **Dermatology**: Skin conditions, rashes, dermatitis
- 🎗️ **Cancer/Oncology**: Tumors, cancer treatments, oncology
- 🦠 **Disease Control & Prevention**: Infectious diseases, vaccines, hygiene

## Performance Notes

- **First Query**: Takes 30-60 seconds (model loading)
- **Subsequent Queries**: 5-10 seconds
- **Memory Usage**: ~8GB RAM recommended
- **GPU**: Optional but recommended for faster inference

## Next Steps

1. ✅ Install Python (if not already installed)
2. ✅ Create virtual environment
3. ✅ Install backend dependencies
4. ✅ Run backend server
5. ✅ Frontend dependencies already installed
6. ✅ Environment configured
7. ✅ Run frontend server
8. 🎯 Test the application!

## Support

If you encounter issues:
1. Check the terminal logs for error messages
2. Verify all prerequisites are installed
3. Ensure both backend (port 5000) and frontend (port 5173) are running
4. Check firewall settings if connection issues persist

---

## Quick Start Commands

### Terminal 1 (Backend):
```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Backend\Backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

### Terminal 2 (Frontend):
```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Frontend"
npm run dev
```

**🎯 Setup Complete! Your Medical RAG application is ready to use!**
