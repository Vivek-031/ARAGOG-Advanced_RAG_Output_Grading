# 🔐 Login & Authentication Guide

## ✅ Authentication System Ready!

I've added the missing authentication endpoints to your backend. Now you can login and signup!

---

## 🏗️ Architecture

Your app uses a **2-tier architecture**:

```
Frontend (React + Vite)  ←→  Backend (Flask + MySQL)
Port: 5173                   Port: 5000
```

**NO separate Node.js server.js needed!** Authentication is handled by the Flask backend.

---

## 📋 What I Fixed

### ❌ **Problem**
- Frontend was calling `/api/auth/login` and `/api/auth/signup`
- Backend didn't have these endpoints
- Login would fail with "Unable to connect to the server"

### ✅ **Solution**
Added to `Backend/Backend/app.py`:
1. **`POST /api/auth/signup`** - User registration
2. **`POST /api/auth/login`** - User login
3. **`users` table** - Stores user accounts in MySQL

---

## 🚀 How to Run & Login

### Step 1: Start Backend Server
```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Backend\Backend"
.\venv\Scripts\Activate.ps1
python app.py
```

**Wait for:**
```
Available Endpoints:
   POST /api/auth/login       - User login
   POST /api/auth/signup      - User registration
   ...
 * Running on http://0.0.0.0:5000
```

### Step 2: Start Frontend
Open a **new terminal**:
```powershell
cd "c:\Users\Admin\Downloads\medirag-ai-main\Frontend"
npm run dev
```

**Wait for:**
```
  VITE ready in XXX ms
  ➜  Local:   http://localhost:5173/
```

### Step 3: Access the App
Open your browser:
```
http://localhost:5173
```

---

## 👤 How to Login

### Option 1: Create New Account
1. Go to `http://localhost:5173`
2. Click **"Sign Up"** link at the bottom
3. Enter:
   - **Name:** Your Name
   - **Email:** your@email.com
   - **Password:** YourPassword123
4. Click **"Sign Up"**
5. You'll be automatically logged in and redirected to `/main`

### Option 2: Login with Existing Account
1. Go to `http://localhost:5173`
2. Enter your **email** and **password**
3. Click **"Sign In"**
4. You'll be redirected to the main chat interface

---

## 🗄️ Database Tables

The backend automatically creates these MySQL tables in the `user_auth` database:

### `users` table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,      -- SHA256 hashed
    avatar VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### `chat_history` table
```sql
CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    session_id VARCHAR(100),
    role VARCHAR(20),
    message TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Authentication Flow

```
1. User enters email/password on Login page
   ↓
2. Frontend sends POST to http://localhost:5000/api/auth/login
   ↓
3. Backend checks user credentials in MySQL
   ↓
4. Backend returns user data + auth token
   ↓
5. Frontend stores token in localStorage
   ↓
6. Frontend redirects to /main (chat interface)
   ↓
7. User is authenticated across the app
```

---

## 🧪 Test Authentication Endpoints

### Test Signup
```powershell
curl -X POST http://localhost:5000/api/auth/signup `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Test User\",\"email\":\"test@example.com\",\"password\":\"password123\"}'
```

**Expected Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com",
    "avatar": null
  },
  "token": "..."
}
```

### Test Login
```powershell
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"password123\"}'
```

**Expected Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com",
    "avatar": null
  },
  "token": "..."
}
```

---

## ⚙️ Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | Login existing user |

### Request Body (Signup)
```json
{
  "name": "Your Name",
  "email": "your@email.com",
  "password": "yourpassword"
}
```

### Request Body (Login)
```json
{
  "email": "your@email.com",
  "password": "yourpassword"
}
```

---

## ⚠️ Important Notes

### Passwords
- Currently uses **SHA256 hashing** (simple but not production-ready)
- For production, use **bcrypt** or **Argon2**
- Passwords are NEVER stored in plain text

### Tokens
- Currently uses **simple random tokens**
- For production, use **JWT (JSON Web Tokens)**
- Tokens stored in browser `localStorage`

### Security
- ✅ CORS enabled for local development
- ✅ Passwords hashed before storage
- ⚠️ Use HTTPS in production
- ⚠️ Implement token expiration
- ⚠️ Add rate limiting for login attempts

---

## 🛠️ Prerequisites

Before you can login:

1. ✅ **MySQL Server** must be running
2. ✅ **Database `user_auth`** must exist
   ```sql
   CREATE DATABASE IF NOT EXISTS user_auth;
   ```
3. ✅ **Backend** must be running on port 5000
4. ✅ **Frontend** must be running on port 5173

---

## 🐛 Troubleshooting

### Issue: "Unable to connect to the server"
**Cause:** Backend is not running
**Solution:** Start the Flask backend first

### Issue: "Invalid email or password"
**Cause:** Wrong credentials or user doesn't exist
**Solution:** Try signing up first or check your password

### Issue: "Email already registered"
**Cause:** You're trying to signup with an existing email
**Solution:** Use the login page instead

### Issue: Database connection error
**Cause:** MySQL not running or wrong credentials
**Solution:** 
1. Start MySQL server
2. Check credentials in `Backend/Backend/.env`
3. Ensure database `user_auth` exists

---

## 📂 Files Modified

- ✅ `Backend/Backend/app.py` - Added authentication endpoints
- ✅ `Frontend/src/pages/Login.tsx` - Already configured (no changes needed)
- ✅ `Frontend/src/pages/Signup.tsx` - Already configured (no changes needed)
- ✅ `Frontend/src/contexts/AuthContext.tsx` - Already configured (no changes needed)

---

## 🎯 Quick Start Summary

```powershell
# Terminal 1 - Start Backend
cd "c:\Users\Admin\Downloads\medirag-ai-main\Backend\Backend"
.\venv\Scripts\Activate.ps1
python app.py

# Terminal 2 - Start Frontend
cd "c:\Users\Admin\Downloads\medirag-ai-main\Frontend"
npm run dev

# Browser
# Go to http://localhost:5173
# Click "Sign Up" to create an account
# Login and start chatting!
```

---

## ✅ System Ready!

Your authentication system is now fully configured and ready to use. You can:
- ✅ Create new accounts
- ✅ Login with existing accounts
- ✅ Stay logged in (token stored in localStorage)
- ✅ Access the medical RAG chat interface
- ✅ Save and retrieve chat history

🎉 **No server.js needed! Everything runs through Flask backend on port 5000.**
