from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import json
import uuid
from datetime import datetime

# Load environment variables (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this-in-production')

# Document storage
DOCUMENTS_STORAGE = {}

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyAxWFW3wCpdpbiis5djEONz_p5vaIY4LzQ')
print(f"Using API Key: {GEMINI_API_KEY[:10]}...")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Gemini AI model initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Gemini AI: {e}")
    model = None

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

def process_document_with_gemini(document_text, language):
    """Process document with Gemini AI for comprehensive analysis"""
    try:
        if model is None:
            return "❌ AI model is not available. Please check the API key configuration."
        
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
        
        print(f"🤖 Processing document with AI (Language: {language})")
        response = model.generate_content(prompt)
        print("✅ AI response received successfully")
        return response.text
        
    except Exception as e:
        print(f"❌ AI Error: {str(e)}")
        return f"❌ Error processing document with AI: {str(e)}"

def answer_question_with_gemini(question, document_text, language):
    """Answer questions about the document using Gemini AI"""
    try:
        if model is None:
            return "❌ AI model is not available. Please check the API key configuration."
        
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
        
        print(f"🤖 Answering question with AI (Language: {language})")
        response = model.generate_content(prompt)
        print("✅ AI Q&A response received successfully")
        return response.text
        
    except Exception as e:
        print(f"❌ AI Q&A Error: {str(e)}")
        return f"❌ Error answering question: {str(e)}"

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

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'message': 'Terabytes Legal AI is running!',
        'timestamp': datetime.now().isoformat(),
        'ai_model_status': 'available' if model is not None else 'unavailable',
        'sample_documents': list(SAMPLE_DOCUMENTS.keys())
    })

@app.route('/debug')
def debug_info():
    """Debug endpoint to check AI and sample documents"""
    try:
        # Test AI with a simple prompt
        ai_test_result = "❌ AI not working"
        if model is not None:
            try:
                test_response = model.generate_content("Say 'AI is working' in one word")
                ai_test_result = f"✅ AI working: {test_response.text}"
            except Exception as e:
                ai_test_result = f"❌ AI error: {str(e)}"
        
        return jsonify({
            'ai_status': ai_test_result,
            'sample_documents': SAMPLE_DOCUMENTS,
            'api_key_configured': bool(GEMINI_API_KEY),
            'model_initialized': model is not None
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
