# zulip-email-forwarder
A lightweight Python/Flask bridge that acts as an outgoing webhook for Zulip, instantly forwarding chat messages to any email address via SMTP. 🚀✉️
# Zulip to Email Forwarder 📨

A simple Python Flask application that acts as an Outgoing Webhook for [Zulip](https://zulip.com). It listens for new messages in your Zulip chat and instantly forwards them to a designated email address via SMTP.

> **⚠️ DISCLAIMER:** This project is vibe-coded and not tested. It was written conceptually as a starting point. You may need to debug or adjust the payload parsing depending on your specific Zulip server version and SMTP provider. Use at your own risk!

## How it Works
1. A team member sends a message in a Zulip stream.
2. Zulip's "Outgoing Webhook" bot sees the message and sends a JSON payload to this app.
3. This app parses the sender, stream, topic, and content.
4. The app authenticates with your email provider (Gmail, SendGrid, Mailgun, etc.) and sends an email to your target inbox.

## Prerequisites
* Python 3.8+
* An SMTP email account (e.g., a Gmail App Password, SendGrid API key, etc.)
* Admin access to a Zulip workspace to create Bots.

## Local Setup & Testing

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/zulip-to-email-forwarder.git
   cd zulip-to-email-forwarder

##1. Install dependencies:
code
Bash
pip install -r requirements.txt

##2. Set your Environment Variables:
You need to provide your SMTP credentials so the app can send emails. On Linux/macOS:
code
Bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASS="your-app-password"
export DESTINATION_EMAIL="team-inbox@yourdomain.com"

##Run the application:
code
Bash
python app.py

The app will start running on http://localhost:5000.

(Note: To test this locally with Zulip, you will need to expose your local port to the internet using a tool like ngrok: ngrok http 5000)

##Deployment

For production, host this app on a platform like Heroku, Render, AWS, or DigitalOcean.
Make sure to:

Set the environment variables (SMTP_USER, SMTP_PASS, etc.) in your hosting provider's dashboard.
Run the app using gunicorn instead of the built-in Flask server:
code
Bash
gunicorn app:app --bind 0.0.0.0:$PORT

##Connecting to Zulip
Once your app is hosted and has a public URL (e.g., https://my-zulip-email-app.herokuapp.com/zulip-to-email), configure Zulip to send messages to it:

1. In Zulip, click the Gear Icon (⚙️) in the top right and go to Personal settings > Bots.
2. Click Add a new bot.
3. Set the Bot Type to Outgoing webhook.
4. Give your bot a name (e.g., Email Forwarder Bot).
5. In the Endpoint URL field, paste your app's live URL:
   https://YOUR_APP_URL/zulip-to-email
6. Click Create bot.
7. Subscribe the bot to the Streams you want it to listen to, or mention it directly in a chat. Any message the bot can "see" will trigger the webhook and send an email!

##Customization
You can easily change the format of the generated email by editing the msg.set_content() function inside app.py.

##License

MIT License
code
Code

*(Pro-tip: If you are using Gmail to send the emails, you cannot use your normal account password. You have to go into your Google Account Security settings, enable 2-Factor Authentication, and generate an "App Password" to put into the `SMTP_PASS` variable.)*
