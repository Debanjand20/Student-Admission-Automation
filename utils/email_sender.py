import smtplib
from email.message import EmailMessage
import os

# You should set these in your .streamlit/secrets.toml or environment variables
EMAIL_ADDRESS = os.environ.get("ADMISSION_BOT_EMAIL")
EMAIL_PASSWORD = os.environ.get("ADMISSION_BOT_PASS")

def send_admission_email(to_email, student_name, letter_text, pdf_path=None):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return False  # Email not configured

    msg = EmailMessage()
    msg['Subject'] = '🎓 Your University Admission Confirmation'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    msg.set_content(f"""
Dear {student_name},

{letter_text}

Please find your admission letter attached.

Best regards,  
University Admissions Team
    """)

    # Attach PDF if exists
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        msg.add_attachment(
            pdf_data,
            maintype='application',
            subtype='pdf',
            filename=os.path.basename(pdf_path)
        )

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
