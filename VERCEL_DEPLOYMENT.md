# 🚀 Vercel Deployment Guide for Terabytes Legal AI

## Quick Deployment Steps:

### 1. **Go to Vercel**
- Visit [vercel.com](https://vercel.com)
- Sign up/Login with GitHub

### 2. **Import Project**
- Click "New Project"
- Import from GitHub: `lokeshwaraprasad/Terabytes-Legalai`
- Select the repository

### 3. **Configure Project**
- **Framework Preset**: Other
- **Build Command**: Leave empty (Vercel auto-detects)
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

### 4. **Add Environment Variables**
Click "Environment Variables" and add:

**GEMINI_API_KEY**
- Value: Your Google Gemini API key
- Environment: Production, Preview, Development

**FLASK_SECRET_KEY**
- Value: `terabytes-legal-ai-secret-key-2024-hackathon`
- Environment: Production, Preview, Development

### 5. **Deploy**
- Click "Deploy"
- Wait 2-3 minutes for deployment
- Get your live URL!

## 🎉 **Your Live URL will be:**
`https://terabytes-legal-ai-[random].vercel.app`

## ✅ **Features Ready:**
- ✨ Stunning animated frontend
- 🤖 AI-powered document analysis
- 💬 Interactive Q&A chat
- 📄 PDF/DOCX/Image upload
- 📱 Mobile responsive
- 🎪 Hackathon presentation ready

## 🔧 **Troubleshooting:**
- If deployment fails, check environment variables
- Make sure Gemini API key is valid
- Check Vercel logs for any errors

## 🏆 **For Hackathon:**
- Share the Vercel URL with judges
- Demonstrate all features
- Show the stunning animations
- Highlight AI capabilities

**Good luck with the Google Gen AI Exchange Hackathon!** 🚀
