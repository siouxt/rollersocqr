from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)

# 🔁 Replace with your actual Google Apps Script webhook URL
GOOGLE_SHEET_WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbw99sNRC-tYiOkRgydziz3sgq0sCeSd_vIsrsAVtINzzrBSTjjhE-8YLVWYQu__op4c/exec'

# 🔁 Replace with your actual destination URL
REDIRECT_URL = 'https://su.sheffield.ac.uk/activities/view/roller-skate-society'

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
            'location': ''
        }

        # Send the data to your Google Sheet via Apps Script
        requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=payload, timeout=2)

    except Exception as e:
        print(f"Error logging to Google Sheet: {e}")

    # Redirect the user to the final URL
    return redirect(REDIRECT_URL, code=302)

# 👇 This makes the app work properly on Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
