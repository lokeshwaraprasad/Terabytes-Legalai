import requests
import os

# Test the upload endpoint
url = "http://127.0.0.1:5000/upload"

# Create a simple test file
test_content = """POWER OF ATTORNEY

This Power of Attorney is made on the 20th day of September 2025.

I, Mr. Raghavan, son of Mr. Krishnan, residing at 21, Lakshmi Nagar, Chennai, Tamil Nadu, do hereby appoint Mr. Suresh Kumar, son of Mr. Raman, residing at 45, Anna Salai, Chennai, to be my true and lawful attorney to act on my behalf.

The attorney is granted powers in respect of the following matters:

1. To manage, sell, lease, mortgage, or otherwise deal with my land property situated at Survey No. 112/3, Thiruvanmiyur, Chennai.

2. To represent me before the Registrar Office, Revenue Department, Municipal Corporation, and any other government offices in connection with the said property.

3. To sign, execute, and deliver all necessary documents, deeds, and agreements related to the above property.

4. To deposit and withdraw money in respect of transactions related to the above-mentioned property.

This Power of Attorney shall remain valid until revoked by me in writing.

Signed at Chennai on this 20th day of September 2025.

Mr. Raghavan (Principal)
Mr. Suresh Kumar (Attorney)

Witnesses:
1. ________________
2. ________________
"""

# Create a test file
with open("test_upload.txt", "w", encoding="utf-8") as f:
    f.write(test_content)

# Test the upload
try:
    with open("test_upload.txt", "rb") as f:
        files = {"file": ("test_document.txt", f, "text/plain")}
        data = {"language": "english"}
        
        print("Testing upload endpoint...")
        response = requests.post(url, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
