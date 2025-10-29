from flask import Flask, send_file, render_template_string, url_for
import qrcode
import io
import requests

app = Flask(__name__)

# Use thumbnail format for Google Drive images
DIRECT_IMAGE_URL = "https://drive.google.com/thumbnail?id=1BtB5fu6TaRsr_9nhqJwdWH1vev1qL7fh&sz=w1000"

# Use export format for Google Docs
DIRECT_TEXT_FILE_URL = "https://docs.google.com/document/d/1y7NdAFc6OySVu5CIbKF7WyCOaAh44D89/export?format=txt"

DEFAULT_TEXT_CONTENT = "Default text: No custom text file found or loaded."


def fetch_text_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching text from {url}: {e}")
        return DEFAULT_TEXT_CONTENT


@app.route('/generate_qr')
def generate_qr():
    # QR code points to /content (where image and text are shown)
    qr_data_url = url_for('content_page', _external=True)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png')


@app.route('/')
def index():
    # This page SHOWS THE QR CODE for people to scan
    return '''
    <!doctype html>
    <html>
    <head>
        <title>QR Code Generator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: sans-serif; 
                text-align: center; 
                margin-top: 50px; 
                background-color: #f4f4f4; 
            }
            img.qr-display { 
                max-width: 300px; 
                height: auto; 
                border: 1px solid #ddd; 
                padding: 10px; 
                background-color: white; 
                box-shadow: 0 0 10px rgba(0,0,0,0.1); 
            }
            p { 
                color: #555; 
                margin: 20px auto;
                max-width: 600px;
            }
            h1 { 
                color: #333; 
            }
            .note { 
                margin-top: 20px; 
                font-style: italic; 
                color: #777; 
                font-size: 0.9em; 
                max-width: 600px; 
                margin: 20px auto; 
                padding: 15px;
                background-color: #d9edf7;
                border: 1px solid #bce8f1;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Scan this QR Code</h1>
        <img class="qr-display" src="/generate_qr" alt="QR Code">
        <p>Scan the QR code to view lab report with image and text from Google Drive.</p>
        <div class="note">
            <p><strong>Important:</strong> Make sure your Google Drive files are shared with "Anyone with the link" (Viewer access).</p>
        </div>
    </body>
    </html>
    '''


@app.route('/content')
def content_page():
    # This is what users see AFTER scanning the QR code
    # IMAGE ABOVE, TEXT BELOW
    custom_text = fetch_text_content(DIRECT_TEXT_FILE_URL)
    formatted_text = custom_text.replace('\n', '<br>')

    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Lab Report</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: sans-serif; 
                text-align: center; 
                margin: 20px; 
                padding: 20px;
                background-color: #e9e9e9; 
                color: #333; 
            }
            h1 { 
                color: #2a2a2a; 
                margin-bottom: 30px; 
            }
            img.content-image {
                max-width: 90%; 
                height: auto; 
                border: 2px solid #5cb85c;
                border-radius: 8px; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                margin-bottom: 30px;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            p.content-text {
                font-size: 1.1em; 
                line-height: 1.6; 
                max-width: 600px;
                margin: 0 auto 20px auto; 
                padding: 20px;
                border: 1px solid #ccc; 
                border-radius: 8px;
                background-color: white; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: left; 
                word-wrap: break-word;
            }
            footer { 
                margin-top: 40px; 
                font-size: 0.9em; 
                color: #777; 
            }
            .error { 
                color: #d9534f; 
                font-weight: bold; 
                margin: 20px auto;
                max-width: 600px;
                padding: 15px;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Lab Report</h1>
        
        <!-- IMAGE ABOVE -->
        <img class="content-image" src="{{ image_url }}" alt="Lab report image"
         onerror="this.style.display='none'; document.getElementById('error-msg').style.display='block';">
        
        <p id="error-msg" class="error" style="display:none;">
            ⚠️ Image failed to load. Please check sharing settings on Google Drive.
        </p>
        
        <!-- TEXT BELOW -->
        <p class="content-text">{{ formatted_text|safe }}</p>
        
        <footer>
            <p>Content fetched from Google Drive</p>
        </footer>
    </body>
    </html>
    ''', formatted_text=formatted_text, image_url=DIRECT_IMAGE_URL)
