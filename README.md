# Terabytes Legal AI - Smart Document Analysis

A powerful AI-powered legal document analysis platform that transforms complex legal documents into simple, understandable insights. Built with Flask and Google's Gemini AI, this application supports multiple languages including English and Tamil.

## 🚀 Features

- **Smart Document Upload**: Support for PDF, DOCX, and image files with automatic text extraction
- **AI-Powered Analysis**: Comprehensive document summaries with key points, risks, and obligations
- **Multi-Language Support**: Analysis available in both English and Tamil
- **Interactive Q&A**: Ask specific questions about your uploaded documents
- **Modern UI**: Beautiful, responsive interface with drag-and-drop file upload
- **OCR Support**: Extract text from images using optical character recognition

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI Model**: Google Gemini 1.5 Flash
- **Frontend**: HTML5, CSS3, JavaScript
- **Document Processing**: PyPDF2, python-docx, pytesseract
- **Styling**: Custom CSS with modern design principles

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Tesseract OCR (for image text extraction)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lokeshwaraprasad/Terabytes-Legalai.git
   cd Terabytes-Legalai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv legal_ai_env
   # On Windows
   legal_ai_env\Scripts\activate
   # On macOS/Linux
   source legal_ai_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```

5. **Install Tesseract OCR**
   - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### API Keys
- Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Update the API key in `app.py` or use environment variables

### File Upload Limits
- Maximum file size: 16MB
- Supported formats: PDF, DOCX, PNG, JPG, JPEG, GIF, BMP

## 📱 Usage

### Upload Documents
1. Select your preferred language (English/Tamil)
2. Choose "Upload File" tab
3. Drag and drop your document or click to browse
4. Click "Process Document" to analyze

### Paste Text
1. Select "Paste Text" tab
2. Enter your legal document text
3. Click "Process Document" to analyze

### Ask Questions
1. After uploading a document, use the Q&A section
2. Type your question about the document
3. Get instant AI-powered answers

## 🌐 Deployment

### Heroku Deployment
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Deploy to Heroku:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically

### Render Deployment
1. Connect your GitHub repository to Render
2. Set environment variables
3. Deploy as a web service

## 📁 Project Structure

```
Terabytes-Legalai/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main frontend template
├── uploads/              # Uploaded files storage
└── legal_ai_env/         # Virtual environment
```

## 🔒 Security Notes

- Change the default secret key in production
- Use environment variables for sensitive data
- Implement proper file validation
- Add rate limiting for production use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- Flask community for the excellent web framework
- All contributors and users of this project

## 📞 Support

For support, email support@terabytes-legal-ai.com or create an issue in this repository.

---

**Made with ❤️ for the legal community**