import pdftotext
import base64
from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image

def read_pdf(pdf_path):
    """
    Read a PDF file and extract both text and images using poppler-based tools.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        dict: Dictionary containing:
            - 'text': Extracted text from all pages
            - 'images': List of base64 encoded images from all pages
    """
    text = ""
    images = []
    
    # Extract text using pdftotext (poppler)
    try:
        with open(pdf_path, "rb") as f:
            pdf = pdftotext.PDF(f)
            # Join all pages with newlines
            text = "\n".join(pdf)
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        text = ""

    # Convert pages to images using pdf2image (poppler)
    try:
        # Convert each page to an image
        pages = convert_from_path(pdf_path)
        
        # Process each page
        for page in pages:
            try:
                # Convert PIL Image to base64
                img_buffer = BytesIO()
                page.save(img_buffer, format='PNG')
                img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                images.append("<lt_base64>" + img_str + "</lt_base64>")
            except Exception as e:
                print(f"Error processing page to image: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
    
    return {
        "text": text.strip(),
        "images": images
    }
