# 🎯 Complete MediRAG Setup - Everything You Need

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         YOUR SYSTEM                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐       ┌──────────┐ │
│  │   Frontend   │   API   │   Backend    │  SQL  │  MySQL   │ │
│  │  React+Vite  │◄───────►│    Flask     │◄─────►│ Database │ │
│  │              │         │              │       │          │ │
│  │ Port: 5173   │         │ Port: 5000   │       │Port: 3306│ │
│  └──────────────┘         └──────────────┘       └──────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**NO server.js needed!** Backend is Flask (Python), not Node.js/Express.

---

## ✅ Status Check

### Backend Files ✅
- [x] `app.py` - Flask server with **authentication endpoints added**
- [x] `multi_domains_medical_final_rag_model.py` - RAG pipeline
- [x] `requirements.txt` - **Updated with all dependencies**
- [x] `.env` - Database configuration
- [x] `medical_qa_checkpoints/` - ML models and FAISS indexes
- [x] `venv/` - Python virtual environment

### Frontend Files ✅
- [x] `src/pages/Login.tsx` - Login page
- [x] `src/pages/Signup.tsx` - Signup page
- [x] `src/contexts/AuthContext.tsx` - Authentication state
- [x] `src/App.tsx` - Main app routing
- [x] `.env` - API URL configuration

### Database ✅
- [x] MySQL Server (must be running)
- [x] Database: `user_auth`
- [x] Tables: `users`, `chat_history` (auto-created by backend)

---

## 🚀 Complete Startup Guide

### Prerequisites
```powershell
# Verify MySQL is running
Get-Service MySQL*

# If not running, start it
Start-Service MySQL80  # or your MySQL service name

# Verify database exists
mysql -u root -p
> SHOW DATABASES;
> # Should see 'user_auth'
```

### Step 1: Start Backend (Flask)
```powershell
# Open Terminal 1
cd "c:\Users\Admin\Downloads\medirag-ai-main\Backend\Backend"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install/update dependencies (if not done)
pip install -r requirements.txt

# Start Flask server
python app.py
```

**✅ Backend is ready when you see:**
```
================================================================================
*** STARTING MEDIRAG BACKEND SERVER ***
================================================================================

Available Endpoints:
   POST /api/auth/login       - User login
   POST /api/auth/signup      - User registration
   POST /api/ask              - Main RAG query endpoint
   ...
 * Running on http://0.0.0.0:5000
```

### Step 2: Start Frontend (React)
```powershell
# Open Terminal 2 (NEW TERMINAL)
cd "c:\Users\Admin\Downloads\medirag-ai-main\Frontend"

# Install dependencies (if not done)
npm install

# Start dev server
npm run dev
```

**✅ Frontend is ready when you see:**
```
  VITE ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Step 3: Access the App
Open your browser:
```
http://localhost:5173
```

---

## 👤 Login Process

### First Time Users
1. Click **"Sign Up"** at bottom of login page
2. Enter your details:
   - Name: `Your Name`
   - Email: `your@email.com`
   - Password: `yourpassword`
3. Click **"Sign Up"**
4. Automatically logged in → Redirected to chat

### Returning Users
1. Enter your **email** and **password**
2. Click **"Sign In"**
3. Redirected to chat interface

---

## 🔧 What Was Fixed

### 1. Backend Dependencies ✅
**Added to `requirements.txt`:**
- `mysql-connector-python` - Database connection
- `python-dotenv` - Environment variables
- `rank-bm25` - Text ranking
- `nltk` - Natural language processing

**Fixed:**
- `torch==2.9.0` → `torch==2.5.1` (invalid version)

### 2. Authentication Endpoints ✅
**Added to `app.py`:**
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User authentication
- `users` table creation - Auto-creates on startup

### 3. Checkpoint Path ✅
**Fixed path detection in `multi_domains_medical_final_rag_model.py`:**
- Handles nested `medical_qa_checkpoints/medical_qa_checkpoints/` structure
- Auto-detects correct path

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | Login user |

### Medical RAG
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ask` | Ask medical question |
| POST | `/api/rag/query` | Legacy RAG endpoint |
| GET | `/api/health` | System health check |
| GET | `/api/domains` | Get medical domains |

### Chat History
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chat/sessions/<user_id>` | Get user's chat sessions |
| GET | `/api/chat/sessions/<session_id>/messages` | Get session messages |
| POST | `/api/chat/save` | Save chat message |
| POST | `/api/chat/new` | Create new session |
| DELETE | `/api/chat/sessions/<session_id>` | Delete session |

---

## 🗄️ Database Schema

### `users` table
```sql
id          INT AUTO_INCREMENT PRIMARY KEY
name        VARCHAR(255)
email       VARCHAR(255) UNIQUE NOT NULL
password    VARCHAR(255) NOT NULL  -- SHA256 hashed
avatar      VARCHAR(500)
created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### `chat_history` table
```sql
id          INT AUTO_INCREMENT PRIMARY KEY
user_id     INT
session_id  VARCHAR(100)
role        VARCHAR(20)
message     TEXT
image_url   TEXT
created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

---

## 🧪 Testing

### Test Backend Health
```powershell
curl http://localhost:5000/api/health
```

### Test Login (after creating account)
```powershell
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"password123\"}'
```

### Test Medical RAG
```powershell
curl -X POST http://localhost:5000/api/ask `
  -H "Content-Type: application/json" `
  -d '{\"query\":\"What is diabetes?\",\"user_id\":1}'
```

---

## 🔐 Security Features

### Current Implementation
- ✅ Password hashing (SHA256)
- ✅ Email uniqueness validation
- ✅ Token-based authentication
- ✅ CORS enabled for local dev
- ✅ Input validation

### Production Recommendations
- ⚠️ Use **bcrypt** or **Argon2** for passwords
- ⚠️ Implement **JWT tokens** with expiration
- ⚠️ Add **rate limiting** on auth endpoints
- ⚠️ Enable **HTTPS only**
- ⚠️ Add **CSRF protection**
- ⚠️ Implement **session management**

---

## 📂 Project Structure

```
medirag-ai-main/
├── Backend/
│   └── Backend/
│       ├── app.py                          ✅ Flask server (AUTH ADDED)
│       ├── multi_domains_medical_final_rag_model.py  ✅ RAG pipeline
│       ├── requirements.txt                ✅ Dependencies (UPDATED)
│       ├── .env                            ✅ DB config
│       ├── venv/                           ✅ Virtual environment
│       └── medical_qa_checkpoints/         ✅ ML models
│
├── Frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.tsx                   ✅ Login page
│   │   │   └── Signup.tsx                  ✅ Signup page
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx             ✅ Auth state
│   │   └── App.tsx                         ✅ Main app
│   ├── .env                                ✅ API URL
│   └── package.json                        ✅ Dependencies
│
├── LOGIN_GUIDE.md                          📘 How to login
├── BACKEND_FIXES.md                        📘 Backend fixes
├── RUN_BACKEND.md                          📘 Backend startup
└── COMPLETE_SETUP.md                       📘 This file
```

---

## 🐛 Common Issues & Solutions

### ❌ "Unable to connect to the server"
**Solution:** Backend not running
```powershell
cd Backend\Backend
python app.py
```

### ❌ MySQL connection error
**Solution:** Start MySQL service
```powershell
Start-Service MySQL80
```

### ❌ "Email already registered"
**Solution:** Use login instead of signup, or use different email

### ❌ Port 5000 already in use
**Solution:** Kill the process
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### ❌ Frontend won't start
**Solution:** Install dependencies
```powershell
cd Frontend
npm install
```

### ❌ Import errors in backend
**Solution:** Reinstall dependencies
```powershell
pip install -r requirements.txt --force-reinstall
```

---

## ⚡ Quick Commands

### Check if Backend is Running
```powershell
curl http://localhost:5000/api/health
```

### Check if Frontend is Running
Open browser: `http://localhost:5173`

### Restart Backend
```powershell
# Press Ctrl+C in backend terminal
python app.py
```

### Restart Frontend
```powershell
# Press Ctrl+C in frontend terminal
npm run dev
```

---

## 🎯 Next Steps

After login, you can:
1. ✅ Ask medical questions in natural language
2. ✅ Get AI-powered answers from 5 medical domains
3. ✅ View chat history organized by sessions
4. ✅ Create new chat sessions
5. ✅ Delete old sessions
6. ✅ Get detailed medical information with sources

---

## 📚 Documentation Files

- 📘 **LOGIN_GUIDE.md** - Detailed authentication guide
- 📘 **BACKEND_FIXES.md** - What was fixed in backend
- 📘 **RUN_BACKEND.md** - Backend startup guide
- 📘 **COMPLETE_SETUP.md** - This file (complete overview)

---

## ✅ Summary

**Your MediRAG system is fully configured and ready!**

- ✅ Backend authentication endpoints added
- ✅ All dependencies installed and updated
- ✅ Database tables auto-created
- ✅ Frontend properly configured
- ✅ No server.js needed (Flask handles everything)

**Just run backend → run frontend → open browser → login → start chatting!**

🎉 **Happy Chatting with MediRAG AI!** 🎉
