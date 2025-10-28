from flask import Flask, send_file, render_template_string, url_for
import qrcode
import io
import requests

app = Flask(__name__)

# Google Drive URLs (keep your existing ones)
DIRECT_IMAGE_URL = "https://drive.usercontent.google.com/download?id=1DXvqYoBOED810kv0r_vK8VvRVRJSFV7y"
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
    # For deployment, use the deployed URL
    qr_data_url = url_for('display_content', _external=True)

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
    return '''
    <!doctype html>
    <html>
    <head>
        <title>QR Code Generator</title>
        <style>
            body { font-family: sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f4; }
            img.qr-display { max-width: 300px; height: auto; border: 1px solid #ddd; padding: 10px; background-color: white; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            p { color: #555; }
            h1 { color: #333; }
            .note { margin-top: 20px; font-style: italic; color: #777; font-size: 0.9em; max-width: 600px; margin: 20px auto; }
        </style>
    </head>
    <body>
        <h1>Scan this QR Code</h1>
        <img class="qr-display" src="/generate_qr" alt="QR Code">
        <p>This QR code links to a page with custom content fetched from Google Drive.</p>
        <div class="note">
            <p><strong>Important:</strong> Make sure your Google Drive files are shared with "Anyone with the link".</p>
        </div>
    </body>
    </html>
    '''


@app.route('/content')
def display_content():
    custom_text = fetch_text_content(DIRECT_TEXT_FILE_URL)
    formatted_text = custom_text.replace('\n', '<br>')

    return render_template_string(f'''
    <!doctype html>
    <html>
    <head>
        <title>QR Code Content</title>
        <style>
            body {{ font-family: sans-serif; text-align: center; margin-top: 50px; background-color: #e9e9e9; color: #333; }}
            h1 {{ color: #2a2a2a; }}
            p.content-text {{ font-size: 1.2em; line-height: 1.6; max-width: 600px; margin: 20px auto; border: 1px solid #ccc; padding: 20px; border-radius: 8px; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: left; word-wrap: break-word; }}
            img.content-image {{ max-width: 80%; height: auto; border: 2px solid #5cb85c; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15); margin-top: 30px; }}
            footer {{ margin-top: 50px; font-size: 0.9em; color: #777; }}
            .error {{ color: #d9534f; font-weight: bold; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>Your Custom Content</h1>
        <p class="content-text">{formatted_text}</p>
        <img class="content-image" src="{DIRECT_IMAGE_URL}" alt="Your custom image" onerror="this.style.display='none'; document.getElementById('error-msg').style.display='block';">
        <p id="error-msg" class="error" style="display:none;">Image failed to load. Check sharing settings.</p>
        <footer>
            <p>Content fetched from Google Drive.</p>
        </footer>
    </body>
    </html>
    ''')


# Remove the if __name__ == '__main__' block for Vercel
# Vercel expects the app object directly
