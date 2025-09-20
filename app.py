from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename
import json
import PyPDF2
from docx import Document
import pytesseract
from PIL import Image
import io
import base64
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this-in-production')

# Document storage
DOCUMENTS_STORAGE = {}

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyAxWFW3wCpdpbiis5djEONz_p5vaIY4LzQ')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sample legal documents
SAMPLE_DOCUMENTS = {
    'tamil': """
    வணக்கம்! இது ஒரு சட்ட ஆவணம் ஆகும். இந்த ஆவணத்தில் பின்வரும் முக்கிய புள்ளிகள் உள்ளன:

    1. கடனாளி மற்றும் கடன்தாரர் இடையேயான ஒப்பந்தம்
    2. கடன் தொகை: ₹5,00,000 (ஐந்து லட்சம் ரூபாய்)
    3. வட்டி விகிதம்: 12% ஆண்டுக்கு
    4. திருப்பிச் செலுத்தும் காலம்: 24 மாதங்கள்
    5. தாமத கட்டணம்: ₹500 மாதத்திற்கு
    6. கடனாளி தினசரி ₹2000 செலுத்த வேண்டும்
    7. ஒப்பந்தம் முறிவு நிலையில், முழு கடன் தொகையும் உடனடியாக திருப்பிச் செலுத்தப்பட வேண்டும்
    8. சட்ட நடவடிக்கை எடுக்கப்படலாம்
    """,
    'english': """
    LEGAL AGREEMENT FOR LOAN REPAYMENT

    This document outlines the terms and conditions between the Borrower and Lender:

    1. Loan Amount: ₹5,00,000 (Five Lakh Rupees)
    2. Interest Rate: 12% per annum
    3. Repayment Period: 24 months
    4. Late Payment Fee: ₹500 per month
    5. Daily Payment: ₹2000
    6. Default Clause: In case of breach, full amount becomes immediately due
    7. Legal Action: Lender reserves right to take legal action
    8. Jurisdiction: Chennai High Court
    """
}

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error extracting DOCX text: {str(e)}"

def extract_text_from_image(file_path):
    """Extract text from image using OCR"""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error extracting image text: {str(e)}"

def process_document_with_gemini(document_text, language, document_id=None):
    """Process document using Gemini AI"""
    try:
        if language == 'tamil':
            prompt = f"""
            இந்த சட்ட ஆவணத்தை பகுப்பாய்வு செய்து எளிய, புரிந்துகொள்ளக்கூடிய சுருக்கத்தை தமிழ் மற்றும் ஆங்கிலத்தில் தரவும்.
            
            ஆவணம்:
            {document_text}
            
            தயவுசெய்து பின்வரும் வடிவத்தில் பதில் தரவும்:
            1. முக்கிய புள்ளிகள் (Key Points)
            2. அபாயங்கள் (Risks)
            3. கடமைகள் (Obligations)
            4. எளிய விளக்கம் (Simple Explanation)
            """
        else:
            prompt = f"""
            Analyze this legal document and provide a simple, understandable summary in both English and Tamil.
            
            Document:
            {document_text}
            
            Please provide in this format:
            1. Key Points
            2. Risks
            3. Obligations
            4. Simple Explanation
            """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error processing document: {str(e)}"

def answer_question_with_gemini(question, document_text, language):
    """Answer questions about the document using Gemini AI"""
    try:
        if language == 'tamil':
            prompt = f"""
            இந்த கேள்விக்கு ஆவணத்தின் அடிப்படையில் பதில் தரவும்:
            
            கேள்வி: {question}
            
            ஆவணம்:
            {document_text}
            
            தயவுசெய்து தெளிவான, புரிந்துகொள்ளக்கூடிய பதிலை தமிழ் மற்றும் ஆங்கிலத்தில் தரவும்.
            """
        else:
            prompt = f"""
            Answer this question based on the document:
            
            Question: {question}
            
            Document:
            {document_text}
            
            Please provide a clear, understandable answer in both English and Tamil.
            """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error answering question: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        language = request.form.get('language', 'english')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            file_id = str(uuid.uuid4())
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
            file.save(file_path)
            
            # Extract text based on file type
            file_extension = filename.lower().split('.')[-1]
            document_text = ""
            
            if file_extension == 'pdf':
                document_text = extract_text_from_pdf(file_path)
            elif file_extension in ['docx', 'doc']:
                document_text = extract_text_from_docx(file_path)
            elif file_extension in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
                document_text = extract_text_from_image(file_path)
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
            
            if document_text.startswith("Error"):
                return jsonify({'error': document_text}), 400
            
            # Store document
            DOCUMENTS_STORAGE[file_id] = {
                'filename': filename,
                'text': document_text,
                'language': language,
                'upload_time': datetime.now().isoformat(),
                'file_path': file_path
            }
            
            # Process with Gemini AI
            result = process_document_with_gemini(document_text, language, file_id)
            
            return jsonify({
                'success': True,
                'summary': result,
                'language': language,
                'document_id': file_id,
                'filename': filename
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_document():
    try:
        data = request.get_json()
        document_text = data.get('document_text', '')
        language = data.get('language', 'english')
        
        if not document_text:
            return jsonify({'error': 'No document text provided'}), 400
        
        # Process with Gemini AI
        result = process_document_with_gemini(document_text, language)
        
        return jsonify({
            'success': True,
            'summary': result,
            'language': language
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        document_id = data.get('document_id', '')
        language = data.get('language', 'english')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if not document_id or document_id not in DOCUMENTS_STORAGE:
            return jsonify({'error': 'Document not found'}), 400
        
        document_text = DOCUMENTS_STORAGE[document_id]['text']
        
        # Answer question with Gemini AI
        answer = answer_question_with_gemini(question, document_text, language)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'language': language
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/documents', methods=['GET'])
def get_documents():
    """Get list of uploaded documents"""
    try:
        documents = []
        for doc_id, doc_data in DOCUMENTS_STORAGE.items():
            documents.append({
                'id': doc_id,
                'filename': doc_data['filename'],
                'language': doc_data['language'],
                'upload_time': doc_data['upload_time']
            })
        
        return jsonify({
            'success': True,
            'documents': documents
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sample/<language>')
def get_sample_document(language):
    if language in SAMPLE_DOCUMENTS:
        return jsonify({
            'success': True,
            'document': SAMPLE_DOCUMENTS[language],
            'language': language
        })
    else:
        return jsonify({'error': 'Language not supported'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
