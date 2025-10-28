from flask import Flask, send_file, render_template_string, url_for
import qrcode
import io
import requests # Needed to fetch content from URLs

app = Flask(__name__)

# --- CONFIGURATION FOR GOOGLE DRIVE LINKS ---
# IMPORTANT: These must be PUBLICLY ACCESSIBLE links that allow direct embedding/download.
# Obtain these by sharing the files publicly on Google Drive and getting the modified links.

# 1. Direct Embeddable Image URL
# For Google Drive images, this is tricky. The best is often a direct link to the image's raw content.
# If you make a file public, you can often get a URL like:
# https://drive.google.com/uc?id=FILE_ID&export=download
# However, this often triggers a download. For direct embedding in <img>, it's safer to use:
# - an image hosted on a CDN
# - an image hosted on GitHub with `?raw=true`
# - a publicly viewable image that Google Drive has processed (e.g., via Google Photos or a specific embed trick).
# For this example, let's use a placeholder assuming you've found a suitable URL.
# Replace with YOUR actual direct image URL
DIRECT_IMAGE_URL = "https://drive.google.com/file/d/1DXvqYoBOED810kv0r_vK8VvRVRJSFV7y/view?usp=drive_link"
# Example of a publicly hosted image that works well:
# DIRECT_IMAGE_URL = "https://images.unsplash.com/photo-1507525428034-b723cf961fac?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"


# 2. Direct Text File URL
# For Google Drive text files, use the format: https://drive.google.com/uc?id=FILE_ID&export=download
# Replace with YOUR actual direct text file URL
DIRECT_TEXT_FILE_URL = "https://docs.google.com/document/d/1y7NdAFc6OySVu5CIbKF7WyCOaAh44D89/edit?usp=drive_link&ouid=115301108895638210931&rtpof=true&sd=true" # <-- REPLACE 'YOUR_TEXT_FILE_ID'

# Placeholder if you haven't set up the text file yet
DEFAULT_TEXT_CONTENT = "Default text: No custom text file found or loaded."

# --- Helper function to fetch text content ---
def fetch_text_content(url):
    try:
        response = requests.get(url, timeout=5) # Add a timeout for network requests
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching text from {url}: {e}")
        return DEFAULT_TEXT_CONTENT

@app.route('/generate_qr')
def generate_qr():
    # The QR code will now point to our new dynamic content page.
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
            .note { margin-top: 20px; font-style: italic; color: #777; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <h1>Scan this QR Code</h1>
        <img class="qr-display" src="/generate_qr" alt="QR Code">
        <p>This QR code links to a page with custom content fetched from Google Drive.</p>
        <div class="note">
            <p><strong>To modify:</strong></p>
            <p>Update <code>DIRECT_IMAGE_URL</code> and <code>DIRECT_TEXT_FILE_URL</code> in <code>app.py</code> with your public Google Drive links.</p>
            <p>Ensure your Google Drive files are set to "Anyone with the link" (Viewer).</p>
        </div>
    </body>
    </html>
    '''

@app.route('/content')
def display_content():
    # Fetch content from the public Google Drive text file URL
    custom_text = fetch_text_content(DIRECT_TEXT_FILE_URL)

    # Basic markdown-like rendering for newlines
    formatted_text = custom_text.replace('\n', '<br>')

    return render_template_string(f'''
    <!doctype html>
    <html>
    <head>
        <title>QR Code Content</title>
        <style>
            body {{ font-family: sans-serif; text-align: center; margin-top: 50px; background-color: #e9e9e9; color: #333; }}
            h1 {{ color: #2a2a2a; }}
            p.content-text {{ font-size: 1.2em; line-height: 1.6; max-width: 600px; margin: 20px auto; border: 1px solid #ccc; padding: 20px; border-radius: 8px; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: left; }}
            img.content-image {{ max-width: 80%; height: auto; border: 2px solid #5cb85c; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15); margin-top: 30px; }}
            footer {{ margin-top: 50px; font-size: 0.9em; color: #777; }}
        </style>
    </head>
    <body>
        <h1>Your Custom Content</h1>
        <p class="content-text">{formatted_text}</p>
        <img class="content-image" src="{DIRECT_IMAGE_URL}" alt="Your custom image">
        <footer>
            <p>Content fetched from Google Drive.</p>
        </footer>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)