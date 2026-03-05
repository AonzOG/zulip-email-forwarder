import os
import smtplib
from email.message import EmailMessage
from flask import Flask, request

app = Flask(__name__)

# Fetch configuration from environment variables for security
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
DESTINATION_EMAIL = os.environ.get("DESTINATION_EMAIL")

@app.route('/zulip-to-email', methods=['POST'])
def zulip_webhook():
    # Parse the incoming JSON payload from Zulip
    data = request.json
    
    if not data or 'message' not in data:
        return "Invalid payload", 400

    message_data = data['message']
    
    # Extract message details
    sender = message_data.get('sender_full_name', 'Unknown Sender')
    stream = message_data.get('display_recipient', 'Direct Message')
    topic = message_data.get('subject', 'No Topic')
    content = data.get('data', '') # The raw markdown message body
    
    # Construct the email
    msg = EmailMessage()
    msg.set_content(f"{sender} posted in #{stream} > {topic}:\n\n{content}\n\n---\nSent via Zulip to Email Forwarder")
    msg['Subject'] = f"New Zulip Message: {stream} - {topic}"
    msg['From'] = SMTP_USER
    msg['To'] = DESTINATION_EMAIL

    # Send the email via SMTP
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return "Email sent successfully", 200
    except Exception as e:
        print(f"Failed to send email: {e}")
        return "Internal Server Error", 500

if __name__ == '__main__':
    # Run the app locally on port 5000
    app.run(host='0.0.0.0', port=5000)
