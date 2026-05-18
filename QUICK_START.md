# MediRAG Deployment Quick Start

## 🎯 Quick Start (5 Steps)

### Step 1: Prepare GitHub
```powershell
cd c:\Users\Admin\Documents\medirag-ai-main

git init
git add .
git commit -m "Initial commit: MediRAG deployment"
git branch -M main

# Create repo on GitHub first: https://github.com/new
# Then connect:
git remote add origin https://github.com/YOUR_USERNAME/medirag-ai.git
git push -u origin main
```

### Step 2: Create Render Account
- Go to https://render.com
- Sign up with GitHub
- Authorize GitHub access

### Step 3: Deploy via Blueprint
1. Click **Blueprints** in Render dashboard
2. Click **+ New**
3. Select **GitHub**
4. Search for `medirag-ai` repo
5. Click **Connect**
6. Review settings (render.yaml configured automatically)
7. Click **Create Resources**

### Step 4: Wait for Deployment
- Backend: ~5-10 minutes (model loading)
- Frontend: ~2-3 minutes
- Database: ~1-2 minutes

### Step 5: Verify
```bash
# Check backend health
curl https://your-backend-name.onrender.com/api/health

# Visit frontend
https://your-frontend-name.onrender.com
```

---

## 📝 Files Already Created

✅ `render.yaml` - Infrastructure configuration
✅ `Procfile` - Backend startup command
✅ `.env.production` - Frontend production config
✅ `app.py` - Updated for environment variables
✅ `vite.config.ts` - Updated with API proxy

---

## 🔑 Key Environment Variables

| Variable | Backend | Frontend |
|----------|---------|----------|
| PORT | ✅ (auto: 5000) | — |
| FLASK_ENV | ✅ (production) | — |
| FLASK_DEBUG | ✅ (False) | — |
| DB_HOST | ✅ (auto) | — |
| DB_USER | ✅ (auto) | — |
| DB_PASSWORD | ✅ (auto) | — |
| VITE_API_URL | — | ✅ (auto) |

All auto-configured by render.yaml!

---

## 🆘 Troubleshooting

### Backend won't start
- Check logs: Render Dashboard → medirag-backend → Logs
- Look for model loading messages
- Wait 5-10 minutes for full initialization

### Frontend shows blank page
- Check browser console for errors
- Verify VITE_API_URL is correct
- Check if backend is healthy

### Database connection error
- Ensure DATABASE environment variables are set
- Wait 2-3 minutes for MySQL to initialize
- Verify database credentials in Render dashboard

### 502 Bad Gateway
- Backend initializing (normal, wait 2-3 min)
- Check backend logs
- Refresh page

---

## 📊 Deployment URLs

After deployment:
- **Backend:** https://**medirag-backend**.onrender.com
- **Frontend:** https://**medirag-frontend**.onrender.com
- **Database:** Auto-managed

Replace **medirag-backend** and **medirag-frontend** with actual service names shown in Render dashboard.

---

## 💡 After Deployment

### Update Code
```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main

# Render auto-deploys!
```

### Monitor Logs
1. Render Dashboard → Service → Logs
2. Check for errors or warnings

### Scale Services (if needed)
1. Upgrade from free to paid tier
2. Increase instance count
3. Upgrade database plan

---

## ✅ Deployment Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Blueprint deployment started
- [ ] Services showing "Live" status
- [ ] Backend health check passes
- [ ] Frontend loads successfully
- [ ] Can create account
- [ ] Can ask medical questions
- [ ] Chat history saves

---

**That's it! Your MediRAG is now deployed! 🎉**
