import qrcode

# Replace this with the URL where your image and file are hosted
# For example: a link to a Google Drive folder, a Dropbox link, or your own website
data = "https://docs.google.com/document/d/1sxzCpjz0hdmZr6yW9dsV7hmJSXGVDexfE4SVVnjSgVo/edit?usp=drive_link"

# Create qr code instance
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add data
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("my_qr_code.png")

print("QR code generated and saved as my_qr_code.png")