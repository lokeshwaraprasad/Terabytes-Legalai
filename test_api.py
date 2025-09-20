#!/usr/bin/env python3
"""
Test script to verify Gemini API key is working
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test if Gemini API key is working"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in environment variables")
        print("Please set GEMINI_API_KEY in your .env file or environment")
        return False
    
    print(f"✅ Found API Key: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with a simple prompt
        response = model.generate_content("Hello, this is a test. Please respond with 'API working!'")
        
        if response.text:
            print("✅ Gemini API is working!")
            print(f"Response: {response.text}")
            return True
        else:
            print("❌ No response from Gemini API")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini API: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Gemini API Key...")
    test_gemini_api()
