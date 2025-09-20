# Deployment Guide - Terabytes Legal AI

This guide covers multiple deployment options for the Terabytes Legal AI application.

## 🚀 Quick Deploy Options

### 1. Railway (Recommended - Free Tier Available)

1. **Connect Repository**
   - Go to [Railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `Terabytes-Legalai` repository

2. **Set Environment Variables**
   - Go to your project dashboard
   - Click on your service
   - Go to "Variables" tab
   - Add the following variables:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     FLASK_SECRET_KEY=your_secret_key_here
     ```

3. **Deploy**
   - Railway will automatically deploy your app
   - Your app will be available at `https://your-app-name.railway.app`

### 2. Render (Free Tier Available)

1. **Connect Repository**
   - Go to [Render.com](https://render.com)
   - Sign up with GitHub
   - Click "New" → "Web Service"
   - Connect your `Terabytes-Legalai` repository

2. **Configure Service**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.11.0

3. **Set Environment Variables**
   - Go to "Environment" tab
   - Add:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     FLASK_SECRET_KEY=your_secret_key_here
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Your app will be available at `https://your-app-name.onrender.com`

### 3. Heroku (Free Tier Discontinued)

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set GEMINI_API_KEY=your_gemini_api_key_here
   heroku config:set FLASK_SECRET_KEY=your_secret_key_here
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### 4. Vercel (Serverless)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Create vercel.json**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

### 5. DigitalOcean App Platform

1. **Connect Repository**
   - Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
   - Click "Create App"
   - Connect your GitHub repository

2. **Configure App**
   - **Source**: GitHub repository
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `gunicorn app:app`

3. **Set Environment Variables**
   - Add in the environment section:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     FLASK_SECRET_KEY=your_secret_key_here
     ```

### 6. Docker Deployment

1. **Build Docker Image**
   ```bash
   docker build -t terabytes-legal-ai .
   ```

2. **Run Container**
   ```bash
   docker run -p 5000:5000 \
     -e GEMINI_API_KEY=your_gemini_api_key_here \
     -e FLASK_SECRET_KEY=your_secret_key_here \
     terabytes-legal-ai
   ```

3. **Docker Compose**
   ```bash
   # Create .env file with your variables
   docker-compose up -d
   ```

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `FLASK_SECRET_KEY` | Flask secret key for sessions | Yes |
| `TESSERACT_CMD` | Path to Tesseract OCR (optional) | No |

## 📝 Pre-Deployment Checklist

- [ ] Update `GEMINI_API_KEY` in environment variables
- [ ] Generate a secure `FLASK_SECRET_KEY`
- [ ] Test the application locally
- [ ] Ensure all dependencies are in `requirements.txt`
- [ ] Check file upload limits (16MB max)
- [ ] Verify Tesseract OCR installation (for image processing)

## 🚨 Common Issues & Solutions

### Issue: Tesseract OCR not found
**Solution**: Install Tesseract OCR on your system or use a Docker image with Tesseract pre-installed.

### Issue: File upload errors
**Solution**: Check file size limits and supported formats (PDF, DOCX, PNG, JPG, etc.).

### Issue: API key errors
**Solution**: Verify your Gemini API key is correct and has sufficient quota.

### Issue: Memory issues
**Solution**: Increase memory allocation or optimize file processing for large documents.

## 🔒 Security Considerations

1. **Environment Variables**: Never commit API keys to version control
2. **File Validation**: Implement proper file type and size validation
3. **Rate Limiting**: Add rate limiting for production use
4. **HTTPS**: Always use HTTPS in production
5. **CORS**: Configure CORS properly if needed

## 📊 Monitoring & Maintenance

1. **Logs**: Monitor application logs for errors
2. **Performance**: Track response times and memory usage
3. **Updates**: Keep dependencies updated
4. **Backups**: Regular backups of uploaded files (if storing permanently)

## 🆘 Support

If you encounter issues during deployment:
1. Check the logs in your hosting platform
2. Verify all environment variables are set correctly
3. Test the application locally first
4. Check the [GitHub Issues](https://github.com/lokeshwaraprasad/Terabytes-Legalai/issues) for common problems

---

**Happy Deploying! 🚀**
