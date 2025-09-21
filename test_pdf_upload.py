import requests
import os

# Test the upload endpoint with PDF
url = "http://127.0.0.1:5000/upload"

# Test the upload with PDF
try:
    with open("test_power_of_attorney.pdf", "rb") as f:
        files = {"file": ("test_power_of_attorney.pdf", f, "application/pdf")}
        data = {"language": "english"}
        
        print("Testing PDF upload endpoint...")
        response = requests.post(url, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
