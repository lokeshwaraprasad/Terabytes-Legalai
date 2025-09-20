# 🚀 Deployment Instructions for Terabytes Legal AI

## Option 1: Render (Recommended - Free)

1. **Go to [Render.com](https://render.com)**
2. **Sign up/Login** with your GitHub account
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repository**: `lokeshwaraprasad/Terabytes-Legalai`
5. **Configure the service:**
   - **Name**: `terabytes-legal-ai`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. **Add Environment Variables:**
   - `GEMINI_API_KEY`: Your Gemini API key
   - `FLASK_SECRET_KEY`: Any random string (Render can generate this)
7. **Click "Create Web Service"**
8. **Wait for deployment** (5-10 minutes)
9. **Get your live URL** from the dashboard

## Option 2: Railway (Alternative)

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login** with GitHub
3. **Click "Deploy from GitHub repo"**
4. **Select**: `lokeshwaraprasad/Terabytes-Legalai`
5. **Add Environment Variables:**
   - `GEMINI_API_KEY`: Your Gemini API key
   - `FLASK_SECRET_KEY`: Any random string
6. **Deploy automatically**

## Option 3: Heroku (Alternative)

1. **Go to [Heroku.com](https://heroku.com)**
2. **Create new app**
3. **Connect GitHub repository**
4. **Add environment variables**
5. **Deploy**

## Environment Variables Needed:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `FLASK_SECRET_KEY`: Any random string for security

## Your GitHub Repository:
https://github.com/lokeshwaraprasad/Terabytes-Legalai

## Features Ready for Demo:
✅ Stunning animated frontend
✅ PDF/DOCX/Image upload
✅ AI-powered document analysis
✅ Interactive Q&A chat
✅ Mobile responsive design
✅ Professional hackathon presentation
