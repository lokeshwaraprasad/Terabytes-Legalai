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
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDKKQNaefREXR7y8vkTJnlP8FrjrAQg-f0')
print(f"Using API Key: {GEMINI_API_KEY[:10]}...")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    print("✅ Gemini AI model initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Gemini AI: {e}")
    model = None

# Sample legal documents
SAMPLE_DOCUMENTS = {
    'tamil': """
    சொத்து விற்பனை ஒப்பந்தம் / PROPERTY SALE AGREEMENT

    விற்பனையாளர்: ராமன் (Ram Kumar)
    வாங்குபவர்: குமார் (Kumar Rajan)
    சொத்து விலை: ₹5,00,000 (ஐந்து லட்சம் ரூபாய்)
    நிலம் அளவு: 2400 சதுர அடி
    முகவரி: சென்னை, தமிழ்நாடு, இந்தியா
    தேதி: 15-09-2024

    முக்கிய விதிகள்:
    1. வாங்குபவர் 30 நாட்களுக்குள் முழு தொகையையும் செலுத்த வேண்டும்
    2. சொத்து பதிவு 60 நாட்களுக்குள் முடிக்கப்பட வேண்டும்
    3. விற்பனையாளர் சொத்து சுத்தமான தலைப்பை வழங்க வேண்டும்
    4. எந்தவொரு கட்டணமும் வாங்குபவர் பொறுப்பில்

    எச்சரிக்கைகள்:
    - சொத்து மீது எந்தவொரு கடனும் இல்லை என்பதை உறுதிப்படுத்தவும்
    - சட்டரீதியான ஆவணங்களை சரிபார்க்கவும்
    - பதிவு கட்டணங்களை கணக்கில் எடுத்துக்கொள்ளவும்
    """,
    'english': """
    PROPERTY SALE AGREEMENT

    Seller: John Smith
    Buyer: Jane Doe
    Property Price: $50,000 (Fifty Thousand Dollars)
    Land Area: 2400 sq ft
    Address: 123 Main Street, New York, USA
    Date: September 15, 2024

    Key Terms and Conditions:
    1. Buyer must pay full amount within 30 days
    2. Property registration must be completed within 60 days
    3. Seller must provide clear title to the property
    4. All registration fees are buyer's responsibility

    Legal Clauses:
    - Property must be free from any encumbrances
    - Seller warrants clear ownership
    - Buyer responsible for due diligence
    - Dispute resolution through arbitration

    Red Alerts - Critical Risks:
    - Verify no outstanding loans on property
    - Check all legal documents thoroughly
    - Consider registration costs and taxes
    - Ensure property boundaries are clear
    - Verify seller's legal capacity to sell

    Important Deadlines:
    - Payment due: October 15, 2024
    - Registration deadline: November 15, 2024
    - Possession date: December 1, 2024
    """
}

def process_document_with_gemini(document_text, language):
    """Process document with Gemini AI for comprehensive bilingual analysis"""
    try:
        if model is None:
            return "❌ AI model is not available. Please check the API key configuration."
        
        prompt = f"""
        Analyze this legal document and provide a comprehensive analysis in BOTH English and Tamil. 
        Please structure your response with clear sections:

        Document Text:
        {document_text}

        Please provide the following sections:

        ## 📋 **DOCUMENT OVERVIEW / ஆவண கண்ணோட்டம்**
        **English**: What type of legal document is this? Brief overview.
        **Tamil**: இது என்ன வகையான சட்ட ஆவணம்? சுருக்கமான கண்ணோட்டம்.

        ## 👥 **PARTIES INVOLVED / பங்கேற்பாளர்கள்**
        **English**: Who are the main parties in this document?
        **Tamil**: இந்த ஆவணத்தில் முக்கிய பங்கேற்பாளர்கள் யார்?

        ## 🏠 **PROPERTY/ASSET DETAILS / சொத்து விவரங்கள்**
        **English**: What property or assets are being discussed?
        **Tamil**: எந்த சொத்து அல்லது சொத்துக்கள் பற்றி விவாதிக்கப்படுகிறது?

        ## 📜 **KEY LEGAL CLAUSES / முக்கிய சட்ட விதிகள்**
        **English**: Important legal clauses and their implications.
        **Tamil**: முக்கியமான சட்ட விதிகள் மற்றும் அவற்றின் விளைவுகள்.

        ## ⚠️ **RED ALERTS - CRITICAL RISKS / சிவப்பு எச்சரிக்கைகள் - முக்கியமான அபாயங்கள்**
        **English**: Critical risks, warnings, and things to be careful about.
        **Tamil**: முக்கியமான அபாயங்கள், எச்சரிக்கைகள் மற்றும் கவனமாக இருக்க வேண்டிய விஷயங்கள்.

        ## 📅 **IMPORTANT DATES & AMOUNTS / முக்கியமான தேதிகள் மற்றும் தொகைகள்**
        **English**: Key dates, deadlines, and financial amounts.
        **Tamil**: முக்கியமான தேதிகள், காலக்கெடுக்கள் மற்றும் நிதி தொகைகள்.

        ## 📝 **SIMPLE SUMMARY / எளிய சுருக்கம்**
        **English**: Easy-to-understand summary for non-legal professionals.
        **Tamil**: சட்ட நிபுணர்கள் அல்லாதவர்களுக்கு புரிந்துகொள்ள எளிதான சுருக்கம்.

        ## 💡 **RECOMMENDATIONS / பரிந்துரைகள்**
        **English**: What should the parties do next?
        **Tamil**: பங்கேற்பாளர்கள் அடுத்து என்ன செய்ய வேண்டும்?

        Make sure to highlight any critical legal obligations, deadlines, or financial risks in both languages.
        """
        
        print(f"🤖 Processing document with comprehensive bilingual analysis")
        response = model.generate_content(prompt)
        print("✅ AI response received successfully")
        return response.text
        
    except Exception as e:
        print(f"❌ AI Error: {str(e)}")
        return f"❌ Error processing document with AI: {str(e)}"

def answer_question_with_gemini(question, document_text, language):
    """Answer questions about the document using Gemini AI with bilingual support"""
    try:
        if model is None:
            return "❌ AI model is not available. Please check the API key configuration."
        
        prompt = f"""
        Based on the following legal document, answer this question in BOTH English and Tamil:
        
        Question: {question}
        
        Document Text:
        {document_text}
        
        Please provide your answer in this format:

        ## 🎯 **DIRECT ANSWER / நேரடி பதில்**
        **English**: [Clear, direct answer to the question]
        **Tamil**: [தமிழில் தெளிவான, நேரடி பதில்]

        ## 📄 **EVIDENCE FROM DOCUMENT / ஆவணத்திலிருந்து சான்று**
        **English**: [Specific quotes or references from the document]
        **Tamil**: [ஆவணத்திலிருந்து குறிப்பிட்ட மேற்கோள்கள் அல்லது குறிப்புகள்]

        ## 💡 **EXPLANATION / விளக்கம்**
        **English**: [Why this answer is correct based on the document]
        **Tamil**: [ஆவணத்தின் அடிப்படையில் இந்த பதில் ஏன் சரியானது]

        ## ⚠️ **IMPORTANT NOTES / முக்கியமான குறிப்புகள்**
        **English**: [Any additional important information related to the question]
        **Tamil**: [கேள்வியுடன் தொடர்புடைய கூடுதல் முக்கியமான தகவல்கள்]

        If the question cannot be answered from the document, please say so clearly in both languages.
        """
        
        print(f"🤖 Answering question with bilingual AI response")
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
        # Ensure we get JSON data
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        document_text = data.get('document_text', '')
        language = data.get('language', 'English')
        
        if not document_text.strip():
            return jsonify({'error': 'Please provide document text'}), 400
        
        print(f"📝 Processing document (Language: {language})")
        # Process with Gemini AI
        result = process_document_with_gemini(document_text, language)
        
        return jsonify({
            'success': True,
            'result': result,
            'language': language
        })
        
    except Exception as e:
        print(f"❌ Process error: {str(e)}")
        return jsonify({'error': f'Error processing document: {str(e)}'}), 500

@app.route('/ask_text', methods=['POST'])
def ask_question_text():
    try:
        # Ensure we get JSON data
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        question = data.get('question', '')
        document_text = data.get('document_text', '')
        language = data.get('language', 'English')
        
        if not question.strip() or not document_text.strip():
            return jsonify({'error': 'Please provide both question and document text'}), 400
        
        print(f"❓ Answering question (Language: {language})")
        # Answer question with Gemini AI
        answer = answer_question_with_gemini(question, document_text, language)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'language': language
        })
        
    except Exception as e:
        print(f"❌ Q&A error: {str(e)}")
        return jsonify({'error': f'Error answering question: {str(e)}'}), 500

@app.route('/sample/<language>')
def get_sample_document(language):
    """Get sample document in specified language"""
    try:
        if language.lower() in SAMPLE_DOCUMENTS:
            return jsonify({
                'success': True,
                'document': SAMPLE_DOCUMENTS[language.lower()],  # Changed 'text' to 'document'
                'language': language
            })
        elif language.lower() == 'land':
            # Special case for land document - return English sample
            return jsonify({
                'success': True,
                'document': SAMPLE_DOCUMENTS['english'],
                'language': 'english'
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

# Global error handler to ensure JSON responses
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"❌ Unhandled error: {str(e)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
