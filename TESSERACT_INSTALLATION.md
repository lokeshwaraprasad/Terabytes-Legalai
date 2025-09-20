# Tesseract OCR Installation Guide

## For Windows (Your System)

### Method 1: Direct Download (Recommended)
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download the latest Windows installer (64-bit)
3. Run the installer as Administrator
4. During installation, make sure to check "Add to PATH"
5. Restart your command prompt/PowerShell
6. Test installation: `tesseract --version`

### Method 2: Using Chocolatey (if you have it)
```powershell
choco install tesseract
```

### Method 3: Using Scoop (if you have it)
```powershell
scoop install tesseract
```

## After Installation

1. **Restart your application:**
   ```bash
   python app.py
   ```

2. **Test image processing:**
   - Upload an image file (PNG, JPG, etc.)
   - The app should now extract text from images

## Alternative: Use PDF Instead

If you don't want to install Tesseract OCR:
1. Convert your image to PDF using online converters
2. Upload the PDF file instead
3. The app will extract text from PDF without needing OCR

## Troubleshooting

- If you get "tesseract not found" error, add Tesseract to your system PATH
- Default installation path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Add this path to your system environment variables
