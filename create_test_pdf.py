from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_test_pdf():
    filename = "test_power_of_attorney.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "POWER OF ATTORNEY")
    
    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 150
    
    content = [
        "This Power of Attorney is made on the 20th day of September 2025.",
        "",
        "I, Mr. Raghavan, son of Mr. Krishnan, residing at 21, Lakshmi Nagar,",
        "Chennai, Tamil Nadu, do hereby appoint Mr. Suresh Kumar, son of Mr. Raman,",
        "residing at 45, Anna Salai, Chennai, to be my true and lawful attorney",
        "to act on my behalf.",
        "",
        "The attorney is granted powers in respect of the following matters:",
        "",
        "1. To manage, sell, lease, mortgage, or otherwise deal with my land",
        "   property situated at Survey No. 112/3, Thiruvanmiyur, Chennai.",
        "",
        "2. To represent me before the Registrar Office, Revenue Department,",
        "   Municipal Corporation, and any other government offices in connection",
        "   with the said property.",
        "",
        "3. To sign, execute, and deliver all necessary documents, deeds, and",
        "   agreements related to the above property.",
        "",
        "4. To deposit and withdraw money in respect of transactions related",
        "   to the above-mentioned property.",
        "",
        "This Power of Attorney shall remain valid until revoked by me in writing.",
        "",
        "Signed at Chennai on this 20th day of September 2025.",
        "",
        "Mr. Raghavan (Principal)",
        "Mr. Suresh Kumar (Attorney)",
        "",
        "Witnesses:",
        "1. ________________",
        "2. ________________"
    ]
    
    for line in content:
        c.drawString(100, y_position, line)
        y_position -= 20
        if y_position < 100:
            c.showPage()
            y_position = height - 100
    
    c.save()
    print(f"Created test PDF: {filename}")
    return filename

if __name__ == "__main__":
    create_test_pdf()
