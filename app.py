from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Replace this with your actual Google Apps Script webhook URL
GOOGLE_SHEET_WEBHOOK_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec'

# Destination URL to redirect after logging the scan
REDIRECT_URL = 'https://example.com'  # change this

@app.route('/')
def track_and_redirect():
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent')
        referrer = request.referrer or "Direct"

        payload = {
            'ip': ip,
            'user_agent': user_agent,
            'referrer': referrer,
            'location': ''  # Optional — can be extended with geo API
        }

        # Post to Google Apps Script
        response = requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            print("Google Sheets webhook error:", response.text)

    except Exception as e:
        print("Error during logging:", e)

    return redirect(REDIRECT_URL)

if __name__ == '__main__':
    app.run(debug=True)
