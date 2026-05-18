# MediRAG Deployment Guide - Render.com

## 📋 Prerequisites
- GitHub account
- Render.com account (free tier available)
- MySQL database (provided by Render)

---

## 🚀 STEP 1: Prepare Your GitHub Repository

### 1.1 Initialize Git (if not already done)

```powershell
cd c:\Users\Admin\Documents\medirag-ai-main

# Initialize git repo
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: MediRAG deployment setup"

# Create main branch
git branch -M main
```

### 1.2 Push to GitHub

```powershell
# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/medirag-ai.git

# Push to GitHub
git push -u origin main
```

**Note:** You may need to create a GitHub Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when git prompts for credentials

---

## 🌍 STEP 2: Deploy on Render

### 2.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (recommended for easy integration)
3. Authorize GitHub access

### 2.2 Create Blueprint Deployment

1. In Render Dashboard, click **Blueprints** (or **New +**)
2. Select **GitHub** as source
3. Search and select your `medirag-ai` repository
4. Click **Connect**
5. Review configuration from `render.yaml`:
   - Backend service: `medirag-backend`
   - Frontend service: `medirag-frontend`
   - Database: `medirag-db`
6. Click **Create Resources**

**Deployment Time:** 10-15 minutes

---

## 🔧 STEP 3: Configure Environment Variables

Once deployment starts, Render will auto-detect environment variables from `render.yaml`. 

### Manual Configuration (if needed):

**Backend Service → Environment:**
```
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

Database credentials will be auto-populated from the MySQL database service.

---

## 🗄️ STEP 4: Handle Model Checkpoints

Your model checkpoints (~2GB) are handled automatically:

1. **Render Disk Storage** (25GB allocated)
   - Path: `/var/data` in container
   - Used for FAISS indexes

2. **First Deployment:**
   - Models copied to persistent disk
   - Subsequent deployments reuse same models
   - No re-download needed

---

## ✅ STEP 5: Verify Deployment

### 5.1 Check Service Status
1. Go to Render Dashboard
2. View each service:
   - **medirag-backend** - Should be "Live"
   - **medirag-frontend** - Should be "Live"
   - **medirag-db** - Should be "Available"

### 5.2 Test Backend Health
```bash
curl https://your-backend-name.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "pipeline_initialized": true,
  "available_domains": 11,
  "domain_names": [
    "general_medical", "mental_health", "ophthalmology", ...
  ]
}
```

### 5.3 Test Frontend
1. Visit: `https://your-frontend-name.onrender.com`
2. Should load the MediRAG interface
3. Try creating an account and asking a medical question

### 5.4 Test Chat Functionality
```bash
curl -X POST https://your-backend-name.onrender.com/api/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What causes diabetes?", "user_id": 1, "session_id": "test"}'
```

---

## 🌐 Access Your Deployment

Once live:
- **Backend API:** `https://your-backend-name.onrender.com`
- **Frontend App:** `https://your-frontend-name.onrender.com`
- **Database:** Auto-managed by Render

Update frontend `.env.production` if backend URL differs:
```
VITE_API_URL=https://your-backend-name.onrender.com
```

---

## 📊 Monitoring & Logs

### View Backend Logs
1. Render Dashboard → medirag-backend → Logs
2. Check for initialization messages and errors

### View Frontend Build Logs
1. Render Dashboard → medirag-frontend → Logs
2. Check for build errors or deployment issues

### Common Issues & Fixes

#### Issue: "502 Bad Gateway"
- Backend may still be initializing (takes ~2-3 min)
- Check logs for model loading progress
- Refresh page after 2-3 minutes

#### Issue: "Cannot connect to database"
- Verify DATABASE environment variables
- Check MySQL service status in Render dashboard
- Wait 2-3 minutes for database to initialize

#### Issue: "Model not found"
- Persistent disk may not have models
- Redeploy backend service to trigger fresh setup
- Check `/var/data` has sufficient space (25GB allocated)

---

## 🔄 Redeploying After Changes

### Method 1: Automatic (Recommended)
```bash
# Make changes locally
git add .
git commit -m "Update: description of changes"
git push origin main

# Render automatically redeploys!
```

### Method 2: Manual
1. Render Dashboard → medirag-backend → Manual Deploy
2. Or redeploy via GitHub webhook

---

## 💰 Cost Breakdown

| Service | Free | Paid |
|---------|------|------|
| Backend | $0 (pauses after 15min inactivity) | $7/mo (always on) |
| Frontend | $0 | $7/mo |
| Database | — | $15/mo |
| Storage | — | $0.50/GB (25GB = $12.50) |
| **TOTAL** | ~$0 | **~$42/month** |

**For production:** Upgrade to paid tier to prevent service pauses.

---

## 🚨 Important Notes

1. **Model Size:** First deployment takes longer due to model loading
2. **Cold Starts:** Free tier pauses after 15min; paid tier stays active
3. **Database:** MySQL starter tier supports ~10 concurrent connections
4. **Storage:** 25GB allocated for models; may need upgrade for larger datasets

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **GitHub Issues:** Post in your repo
- **Logs:** Check Render dashboard logs for detailed errors

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create Render account
3. ✅ Deploy via blueprint
4. ✅ Monitor logs and test endpoints
5. ✅ Configure custom domain (optional)
6. ✅ Set up monitoring alerts (optional)
