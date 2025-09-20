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

# Load environment variables (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass  # Continue without .env file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this-in-production')

# Document storage
DOCUMENTS_STORAGE = {}

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyAxWFW3wCpdpbiis5djEONz_p5vaIY4LzQ')
print(f"Using API Key: {GEMINI_API_KEY[:10]}...")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sample legal documents
SAMPLE_DOCUMENTS = {
    'tamil': """
    வணக்கம்! இது ஒரு சட்ட ஆவணம் ஆகும். இந்த ஆவணத்தில் பின்வரும் முக்கிய புள்ளிகள் உள்ளன:

    1. சொத்து விவரங்கள்: இந்த ஆவணம் ஒரு நிலத்தைப் பற்றியது
    2. விற்பனையாளர்: ராமன்
    3. வாங்குபவர்: குமார்
    4. விலை: ₹5,00,000
    5. நிலம் அளவு: 2400 சதுர அடி
    6. முகவரி: சென்னை, தமிழ்நாடு

    இந்த ஆவணம் சட்டரீதியாக சரியானது மற்றும் பதிவு செய்யப்பட்டது.
    """,
    'english': """
    This is a legal document regarding property transfer. The key details are:

    1. Property Details: Residential land
    2. Seller: John Smith
    3. Buyer: Jane Doe
    4. Price: $50,000
    5. Land Area: 2400 sq ft
    6. Address: New York, USA

    This document is legally valid and registered.
    """
}

def extract_text_from_pdf(file_path):
    """Extract text from PDF file with chunking for large documents"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
                
                # Add page break for better processing
                if page_num < len(pdf_reader.pages) - 1:
                    text += f"\n--- PAGE {page_num + 2} ---\n"
            
            return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error extracting text from DOCX: {str(e)}"

def extract_text_from_image(file_path):
    """Extract text from image using OCR"""
    try:
        # Check if Tesseract is available
        try:
            pytesseract.get_tesseract_version()
        except:
            return "Tesseract OCR is not installed. Please convert your image to PDF or use manual text input."
        
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang='eng+tam')
        return text
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"

def chunk_document(document_text, chunk_size=8000):
    """Split large documents into smaller chunks"""
    words = document_text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

def process_large_document(chunks, language):
    """Process document chunks and synthesize a comprehensive summary"""
    try:
        chunk_summaries = []
        
        for i, chunk in enumerate(chunks):
            prompt = f"""
            Analyze this legal document chunk {i+1} of {len(chunks)} and provide a detailed summary in {language}:
            
            {chunk}
            
            Please provide:
            1. Document type and nature
            2. Key parties involved
            3. Important dates and amounts
            4. Legal terms and conditions
            5. Any risks or important notes
            """
            
            response = model.generate_content(prompt)
            chunk_summaries.append(response.text)
        
        # Synthesize all chunk summaries
        synthesis_prompt = f"""
        Combine these {len(chunk_summaries)} summaries of a legal document into one comprehensive analysis in {language}:
        
        {chr(10).join([f"Summary {i+1}: {summary}" for i, summary in enumerate(chunk_summaries)])}
        
        Provide a final comprehensive summary with:
        1. Document Type and Purpose
        2. All Parties Involved
        3. Property/Asset Details
        4. Key Terms and Conditions
        5. Important Dates and Financial Details
        6. Legal Risks and Precautions
        7. Simple Summary for non-legal understanding
        """
        
        final_response = model.generate_content(synthesis_prompt)
        return final_response.text
        
    except Exception as e:
        return f"Error processing large document: {str(e)}"

def process_document_with_gemini(document_text, language, document_id=None):
    """Process document with Gemini AI for comprehensive analysis"""
    try:
        # Check if document is too large and needs chunking
        if len(document_text) > 10000:  # If document is very large
            chunks = chunk_document(document_text)
            return process_large_document(chunks, language)
        
        prompt = f"""
        Analyze this legal document and provide a comprehensive summary in {language}. 
        Please structure your response with clear sections:

        Document Text:
        {document_text}

        Please provide:
        1. **Document Type**: What type of legal document is this?
        2. **Parties Involved**: Who are the main parties in this document?
        3. **Property/Asset Details**: What property or assets are being discussed?
        4. **Key Terms**: What are the important terms and conditions?
        5. **Legal Actions**: What legal actions or agreements are mentioned?
        6. **Risks & Precautions**: What risks or important precautions should be noted?
        7. **Simple Summary**: A simple, easy-to-understand summary for non-legal professionals

        Make sure to highlight any important dates, amounts, or legal obligations.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error processing document with AI: {str(e)}"

def answer_question_with_gemini(question, document_text, language):
    """Answer questions about the document using Gemini AI"""
    try:
        prompt = f"""
        Based on the following legal document, answer this question in {language}:
        
        Question: {question}
        
        Document Text:
        {document_text}
        
        Please provide:
        1. **Direct Answer**: A clear, direct answer to the question
        2. **Evidence**: Specific quotes or references from the document that support your answer
        3. **Explanation**: Why this answer is correct based on the document
        4. **Important Notes**: Any additional important information related to the question
        
        If the question cannot be answered from the document, please say so clearly.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error answering question: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_document():
    try:
        data = request.get_json()
        document_text = data.get('document_text', '')
        language = data.get('language', 'English')
        
        if not document_text.strip():
            return jsonify({'error': 'Please provide document text'}), 400
        
        # Process with Gemini AI
        result = process_document_with_gemini(document_text, language)
        
        return jsonify({
            'success': True,
            'result': result,
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing document: {str(e)}'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get language preference
        language = request.form.get('language', 'English')
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        file_path = f"temp_{uuid.uuid4()}_{filename}"
        file.save(file_path)
        
        # Extract text based on file type
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            document_text = extract_text_from_pdf(file_path)
        elif file_extension in ['doc', 'docx']:
            document_text = extract_text_from_docx(file_path)
        elif file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            document_text = extract_text_from_image(file_path)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Clean up temporary file
        try:
            os.remove(file_path)
        except:
            pass
        
        if not document_text.strip():
            return jsonify({'error': 'Could not extract text from file'}), 400
        
        # Store document for Q&A
        document_id = str(uuid.uuid4())
        DOCUMENTS_STORAGE[document_id] = {
            'text': document_text,
            'filename': filename,
            'uploaded_at': datetime.now().isoformat()
        }
        
        # Process with Gemini AI
        result = process_document_with_gemini(document_text, language, document_id)
        
        return jsonify({
            'success': True,
            'result': result,
            'document_id': document_id,
            'filename': filename,
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        document_id = data.get('document_id', '')
        language = data.get('language', 'English')
        
        if not question.strip():
            return jsonify({'error': 'Please provide a question'}), 400
        
        if not document_id or document_id not in DOCUMENTS_STORAGE:
            return jsonify({'error': 'Document not found. Please upload a document first.'}), 400
        
        document_text = DOCUMENTS_STORAGE[document_id]['text']
        
        # Answer question with Gemini AI
        answer = answer_question_with_gemini(question, document_text, language)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': f'Error answering question: {str(e)}'}), 500

@app.route('/ask_text', methods=['POST'])
def ask_question_text():
    try:
        data = request.get_json()
        question = data.get('question', '')
        document_text = data.get('document_text', '')
        language = data.get('language', 'English')
        
        if not question.strip() or not document_text.strip():
            return jsonify({'error': 'Please provide both question and document text'}), 400
        
        # Answer question with Gemini AI
        answer = answer_question_with_gemini(question, document_text, language)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': f'Error answering question: {str(e)}'}), 500

@app.route('/documents', methods=['GET'])
def get_documents():
    """Get list of uploaded documents"""
    try:
        documents = []
        for doc_id, doc_data in DOCUMENTS_STORAGE.items():
            documents.append({
                'id': doc_id,
                'filename': doc_data['filename'],
                'uploaded_at': doc_data['uploaded_at']
            })
        
        return jsonify({
            'success': True,
            'documents': documents
        })
        
    except Exception as e:
        return jsonify({'error': f'Error getting documents: {str(e)}'}), 500

@app.route('/sample/<language>')
def get_sample_document(language):
    """Get sample document in specified language"""
    try:
        if language.lower() in SAMPLE_DOCUMENTS:
            return jsonify({
                'success': True,
                'text': SAMPLE_DOCUMENTS[language.lower()],
                'language': language
            })
        else:
            return jsonify({'error': 'Language not supported'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Error getting sample document: {str(e)}'}), 500

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)
