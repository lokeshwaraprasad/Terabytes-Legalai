# 🚀 Deployment Guide for Terabytes Legal AI

## Option 1: Railway (Recommended - Easiest)

### Step 1: Go to Railway
1. Visit **[railway.app](https://railway.app)**
2. **Sign up/Login** with GitHub

### Step 2: Deploy from GitHub
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `lokeshwaraprasad/Terabytes-Legalai`
4. Railway will automatically detect it's a Python app

### Step 3: Configure Environment Variables (Optional)
- **GEMINI_API_KEY**: Your Gemini API key (or leave empty to use fallback)
- **FLASK_SECRET_KEY**: Any random string

### Step 4: Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes
3. Get your live URL!

---

## Option 2: Render (Alternative)

### Step 1: Go to Render
1. Visit **[render.com](https://render.com)**
2. **Sign up/Login** with GitHub

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `lokeshwaraprasad/Terabytes-Legalai`

### Step 3: Configure
- **Name**: `terabytes-legal-ai`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes
3. Get your live URL!

---

## Option 3: Vercel (If you want to try again)

### Step 1: Go to Vercel
1. Visit **[vercel.com](https://vercel.com)**
2. **Sign up/Login** with GitHub

### Step 2: Import Project
1. Click **"New Project"**
2. Import: `lokeshwaraprasad/Terabytes-Legalai`

### Step 3: Configure
- **Framework Preset**: `Other`
- **Build Command**: Leave empty
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

### Step 4: Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes

---

## 🎯 Recommended: Use Railway

**Railway is the easiest and most reliable option for Flask apps!**

1. ✅ **Automatic detection** of Python apps
2. ✅ **No complex configuration** needed
3. ✅ **Free tier** available
4. ✅ **Easy environment variables** setup
5. ✅ **Automatic deployments** from GitHub

---

## 🔧 Troubleshooting

### If Vercel still shows "Serverless Function Crashed":
1. Try **Railway** instead (recommended)
2. Or try **Render** as alternative
3. Both are more reliable for Flask apps

### If you get API key errors:
- The app has a **fallback API key** built-in
- It will work even without setting environment variables
- You can add your own API key later for better performance

---

## 🎉 After Deployment

Your app will be live at:
- **Railway**: `https://your-project-name.railway.app`
- **Render**: `https://your-project-name.onrender.com`
- **Vercel**: `https://your-project-name.vercel.app`

**The app includes:**
- ✅ Document upload (PDF, DOCX, Images)
- ✅ AI-powered legal analysis
- ✅ Q&A chat functionality
- ✅ Beautiful, responsive UI
- ✅ Tamil and English support
