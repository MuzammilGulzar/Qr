import qrcode
import os

def create_qr_code(data, filename="file_qr_code.png"):
    """Creates and saves a QR code from the given data (URL)."""
    try:
        # Instantiate the QRCode object
        qr = qrcode.QRCode(
            version=None,  # Let the library determine the size
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        
        # Add the URL data
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create the image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image
        img.save(filename)
        
        print(f"✅ Successfully generated QR code for your file!")
        print(f"   Link: {data}")
        print(f"   File: {os.path.abspath(filename)}")

    except Exception as e:
        print(f"❌ Error generating QR code: {e}")

# --- Main execution ---
if __name__ == "__main__":
    
    # 1. PASTE YOUR SHARABLE LINK HERE
    #    (Example link is a placeholder)
    file_url = "https://drive.google.com/file/d/124UD7ENb50t5wMwjJF04GEysU2mUAmfZ/view?usp=drive_link" 
    
    # 2. Define the output filename
    output_filename = "my_file_qr.png"
    
    # 3. Create the QR code
    create_qr_code(file_url, output_filename)