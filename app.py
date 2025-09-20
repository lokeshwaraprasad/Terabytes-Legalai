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
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not found!")
    print("Please set GEMINI_API_KEY in your environment variables.")
    exit(1)

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
    """,
    'land_document': """
    பாகப் பிரிவினைப் பத்திரம் (PARTITION DEED)

    இந்த ஆவணம் நாமக்கல் மாவட்டம், திருச்செங்கோடு வட்டம், கொக்கராயன் பேட்டை ரோடு, அனிமூர் போஸ்ட் பகுதியில் உள்ள நிலத்தைப் பிரித்துக்கொள்வதற்கான ஒப்பந்தம் ஆகும்.

    முக்கிய புள்ளிகள்:
    1. பங்காளிகள்: P. சுப்பிரமணியம், K. ஈஸ்வரமூர்த்தி, E. யசோதா
    2. நில இடம்: நாமக்கல் மாவட்டம், திருச்செங்கோடு வட்டம்
    3. முகவரி: கொக்கராயன் பேட்டை ரோடு, அனிமூர் போஸ்ட்
    4. ஆவண எண்: 49420
    5. பக்கம்: 5/20

    சட்ட நடவடிக்கைகள்:
    - இந்த ஆவணம் சட்டப்படி பதிவு செய்யப்பட்டுள்ளது
    - அனைத்து பங்காளிகளும் இந்த ஒப்பந்தத்தை ஒப்புக்கொண்டுள்ளனர்
    - நிலத்தின் பிரிவினை சட்டப்படி நடைபெறும்
    - எந்தவொரு சர்ச்சையும் நீதிமன்றத்தில் தீர்வு காணப்படும்

    குறிப்புகள்:
    - P. தெய்வாணை இ.பெ.ரே
    - N துளசியம்மாள் இ.பெ.ரே
    """
}

def extract_text_from_pdf(file_path):
    """Extract text from PDF file with better chunking"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            page_texts = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    page_texts.append(f"--- Page {page_num + 1} ---\n{page_text}\n")
                    text += page_text + "\n"
            
            # If we have multiple pages, add page separators for better processing
            if len(page_texts) > 1:
                return "\n".join(page_texts)
            else:
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
        # Check if tesseract is available
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            return "Error: Tesseract OCR is not installed. Please install Tesseract OCR to process images, or convert your image to PDF format."
        
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang='tam+eng')  # Support both Tamil and English
        return text if text.strip() else "No text could be extracted from the image. Please ensure the image is clear and contains readable text."
    except Exception as e:
        return f"Error extracting image text: {str(e)}"

def process_document_with_gemini(document_text, language, document_id=None):
    """Process document using Gemini AI with enhanced analysis"""
    try:
        # Check if document is too long and needs chunking
        if len(document_text) > 10000:  # If document is very long
            chunks = chunk_document(document_text)
            return process_large_document(chunks, language)
        
        if language == 'tamil':
            prompt = f"""
            இந்த சட்ட ஆவணத்தை முழுமையாக பகுப்பாய்வு செய்து விரிவான, புரிந்துகொள்ளக்கூடிய சுருக்கத்தை தமிழ் மற்றும் ஆங்கிலத்தில் தரவும்.
            
            ஆவணம்:
            {document_text}
            
            தயவுசெய்து பின்வரும் வடிவத்தில் விரிவான பதில் தரவும்:
            
            📋 ஆவண வகை (Document Type):
            - இது என்ன வகையான சட்ட ஆவணம்?
            
            👥 பங்காளிகள் (Parties Involved):
            - இந்த ஆவணத்தில் யார் யார் பங்கு வகிக்கிறார்கள்?
            - அவர்களின் பெயர்கள் மற்றும் பாத்திரங்கள் என்ன?
            
            🏠 சொத்து விவரங்கள் (Property Details):
            - சொத்து எங்கே உள்ளது?
            - சொத்தின் வகை மற்றும் விவரங்கள் என்ன?
            - சொத்து எண் அல்லது அடையாளங்கள் என்ன?
            
            📝 முக்கிய விதிமுறைகள் (Key Terms):
            - இந்த ஆவணத்தின் முக்கிய விதிமுறைகள் என்ன?
            - பணம், காலம், நிபந்தனைகள் பற்றி என்ன கூறப்பட்டுள்ளது?
            
            ⚖️ சட்ட நடவடிக்கைகள் (Legal Actions):
            - சட்டப்படி என்ன நடவடிக்கைகள் எடுக்கப்படும்?
            - சர்ச்சை நிலையில் என்ன செய்யப்படும்?
            
            ⚠️ அபாயங்கள் மற்றும் கவனிப்புகள் (Risks & Precautions):
            - இந்த ஆவணத்தில் என்ன அபாயங்கள் உள்ளன?
            - என்ன கவனிப்புகள் எடுக்க வேண்டும்?
            
            📋 எளிய சுருக்கம் (Simple Summary):
            - இந்த ஆவணத்தின் முக்கிய செய்தி என்ன?
            - இது ஏன் முக்கியமானது?
            """
        else:
            prompt = f"""
            Analyze this legal document comprehensively and provide a detailed, understandable summary in both English and Tamil.
            
            Document:
            {document_text}
            
            Please provide a detailed response in this format:
            
            📋 Document Type:
            - What type of legal document is this?
            
            👥 Parties Involved:
            - Who are the parties involved in this document?
            - What are their names and roles?
            
            🏠 Property Details:
            - Where is the property located?
            - What type of property and its details?
            - What are the property numbers or identifiers?
            
            📝 Key Terms:
            - What are the main terms and conditions?
            - What is mentioned about money, time, conditions?
            
            ⚖️ Legal Actions:
            - What legal actions will be taken?
            - What happens in case of disputes?
            
            ⚠️ Risks and Precautions:
            - What risks are involved in this document?
            - What precautions should be taken?
            
            📋 Simple Summary:
            - What is the main message of this document?
            - Why is this important?
            """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error processing document: {str(e)}"

def chunk_document(document_text, chunk_size=8000):
    """Split large document into smaller chunks for processing"""
    words = document_text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

def process_large_document(chunks, language):
    """Process large document by analyzing chunks and providing comprehensive summary"""
    try:
        summaries = []
        
        for i, chunk in enumerate(chunks):
            if language == 'tamil':
                prompt = f"""
                இந்த சட்ட ஆவணத்தின் பகுதி {i+1} ஐ பகுப்பாய்வு செய்து முக்கிய புள்ளிகளை தமிழ் மற்றும் ஆங்கிலத்தில் தரவும்.
                
                ஆவண பகுதி:
                {chunk}
                
                முக்கிய புள்ளிகள்:
                1. பங்காளிகள்
                2. சொத்து விவரங்கள்  
                3. முக்கிய விதிமுறைகள்
                4. சட்ட நடவடிக்கைகள்
                """
            else:
                prompt = f"""
                Analyze this part {i+1} of the legal document and provide key points in both English and Tamil.
                
                Document Part:
                {chunk}
                
                Key Points:
                1. Parties involved
                2. Property details
                3. Key terms
                4. Legal actions
                """
            
            response = model.generate_content(prompt)
            summaries.append(f"--- Part {i+1} Analysis ---\n{response.text}\n")
        
        # Create final comprehensive summary
        final_prompt = f"""
        Based on these individual analyses of a legal document, provide a comprehensive summary in both English and Tamil:
        
        {chr(10).join(summaries)}
        
        Please provide:
        1. Complete document overview
        2. All parties involved
        3. Complete property details
        4. All key terms and conditions
        5. Legal implications and risks
        6. Simple explanation for common people
        """
        
        final_response = model.generate_content(final_prompt)
        return final_response.text
        
    except Exception as e:
        return f"Error processing large document: {str(e)}"

def answer_question_with_gemini(question, document_text, language):
    """Answer questions about the document using Gemini AI with enhanced context"""
    try:
        if language == 'tamil':
            prompt = f"""
            இந்த கேள்விக்கு ஆவணத்தின் அடிப்படையில் விரிவான, துல்லியமான பதில் தரவும்:
            
            கேள்வி: {question}
            
            ஆவணம்:
            {document_text}
            
            தயவுசெய்து பின்வரும் வடிவத்தில் பதில் தரவும்:
            
            📝 நேரடி பதில் (Direct Answer):
            - கேள்விக்கு நேரடியான பதில்
            
            📋 ஆவணத்தில் இருந்து ஆதாரம் (Evidence from Document):
            - ஆவணத்தில் இருந்து தொடர்புடைய பகுதிகள்
            - குறிப்புகள் மற்றும் எண்கள்
            
            🔍 விளக்கம் (Explanation):
            - பதிலின் விளக்கம்
            - சட்ட அர்த்தம்
            
            ⚠️ கவனிப்புகள் (Important Notes):
            - முக்கியமான கவனிப்புகள்
            - சட்ட அறிவுரைகள்
            
            தமிழ் மற்றும் ஆங்கிலத்தில் பதில் தரவும்.
            """
        else:
            prompt = f"""
            Answer this question based on the document with detailed, accurate information:
            
            Question: {question}
            
            Document:
            {document_text}
            
            Please provide your answer in this format:
            
            📝 Direct Answer:
            - Direct response to the question
            
            📋 Evidence from Document:
            - Relevant parts from the document
            - Specific references and numbers
            
            🔍 Explanation:
            - Explanation of the answer
            - Legal implications
            
            ⚠️ Important Notes:
            - Important considerations
            - Legal advice
            
            Provide the answer in both English and Tamil.
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
                if document_text.startswith("Error: Tesseract OCR is not installed"):
                    return jsonify({
                        'error': 'Image processing requires Tesseract OCR. Please convert your image to PDF format or install Tesseract OCR. For now, you can use the "Paste Text" tab to manually enter the text from your image.',
                        'suggestion': 'Convert image to PDF or use manual text input'
                    }), 400
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
        
        document_text = None
        
        # Check if document_id is provided and exists in storage
        if document_id and document_id in DOCUMENTS_STORAGE:
            document_text = DOCUMENTS_STORAGE[document_id]['text']
        else:
            # If no document_id, try to get from session or return error
            return jsonify({'error': 'No document available. Please upload a document first.'}), 400
        
        if not document_text:
            return jsonify({'error': 'Document text not found'}), 400
        
        # Answer question with Gemini AI
        answer = answer_question_with_gemini(question, document_text, language)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'language': language
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask_text', methods=['POST'])
def ask_question_text():
    """Ask questions about text documents (not uploaded files)"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        document_text = data.get('document_text', '')
        language = data.get('language', 'english')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if not document_text:
            return jsonify({'error': 'No document text provided'}), 400
        
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

@app.route('/sample/land')
def get_land_document_sample():
    return jsonify({
        'success': True,
        'document': SAMPLE_DOCUMENTS['land_document'],
        'language': 'tamil'
    })

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
