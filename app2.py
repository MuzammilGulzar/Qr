from flask import Flask, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/generate_qr')
def generate_qr():
    # The data encoded in your QR code.
    # Replace this with any URL or text you want the QR code to point to.
    data = "https://drive.google.com/drive/folders/1pDhc9a-HfIR3maGhcQz2WejtBbLdUNqP?usp=sharing"

    # Configure QR code properties
    qr = qrcode.QRCode(
        version=1, # Controls the size of the QR Code. 1 (21x21) to 40 (177x177)
        error_correction=qrcode.constants.ERROR_CORRECT_L, # Error correction level
        box_size=10, # Size of each 'box' (pixel) in the QR code
        border=4, # Thickness of the border around the QR code (minimum 4)
    )
    qr.add_data(data)
    qr.make(fit=True) # Ensure all data fits in the chosen version

    # Create the QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to an in-memory byte stream instead of a file
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0) # Rewind the stream to the beginning for reading

    # Send the image bytes as a PNG file
    return send_file(img_bytes, mimetype='image/png')

@app.route('/')
def index():
    # This is the main HTML page that will display the QR code
    # The <img src="/generate_qr"> tag tells the browser to fetch the image from your Flask route
    return '''
    <!doctype html>
    <html>
    <head>
        <title>QR Code Display</title>
        <style>
            body { font-family: sans-serif; text-align: center; margin-top: 50px; }
            img { max-width: 300px; height: auto; border: 1px solid #ddd; padding: 10px; background-color: white; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            p { color: #555; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Scan this QR Code</h1>
        <img src="/generate_qr" alt="QR Code">
        <p>This QR code links to an example website.</p>
        <p>You can change the URL in the <code>app.py</code> file.</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # This block is for local development only. Vercel will not use it.
    app.run(debug=True)