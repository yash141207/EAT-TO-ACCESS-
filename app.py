# app.py
import os
import requests
from flask import Flask, request, jsonify
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

# Target API URL – can be overridden by environment variable
TARGET_API_URL = os.environ.get("TARGET_API_URL", "https://api-otrss.garena.com/support/callback/")

@app.route('/rizer', methods=['GET'])
def rizer():
    # Get the eat_token from query parameters
    eat_token = request.args.get('eat_token')
    if not eat_token:
        return "Missing eat_token parameter", 400

    # Forward relevant headers (filter out problematic ones)
    headers_to_forward = {}
    for header, value in request.headers.items():
        # Skip headers that might cause issues
        if header.lower() in ['host', 'content-length', 'connection', 'transfer-encoding']:
            continue
        headers_to_forward[header] = value

    # Make the request to the target API
    try:
        # We want to follow redirects and capture the final URL
        session = requests.Session()
        # Disable automatic redirect handling so we can inspect each step
        response = session.get(TARGET_API_URL, params={'access_token': eat_token},
                               headers=headers_to_forward, allow_redirects=False)
        
        # Follow redirects manually
        while response.status_code in (301, 302, 303, 307, 308):
            location = response.headers.get('Location')
            if not location:
                break
            # Handle relative vs absolute URLs
            if not location.startswith(('http://', 'https://')):
                # Build absolute URL from base
                base = urlparse(TARGET_API_URL)
                location = base._replace(path=location).geturl()
            response = session.get(location, headers=headers_to_forward, allow_redirects=False)

        final_url = response.url

        # Extract access_token from final URL query parameters
        parsed = urlparse(final_url)
        query_params = parse_qs(parsed.query)
        access_token = query_params.get('access_token', [None])[0]

        if not access_token:
            # Fallback: try to find in response body? (not described, but just in case)
            # Here we could parse response.text but we'll just return an error.
            return "Access token not found in final URL", 500

        # Build the response text
        response_text = f"""YASH_1429
TELEGRAM:@Yash_1429
TELEGRAM CHANNEL:@YashxUdit
THANKS FOR USING!
access token= {access_token}"""
        return response_text, 200, {'Content-Type': 'text/plain'}

    except Exception as e:
        # Log the error (you may want to use proper logging)
        print(f"Error: {e}")
        return f"Internal server error: {str(e)}", 500

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    #MADE BY RIZER..
    # CREDIT CHORO KI MAA KI CHUT