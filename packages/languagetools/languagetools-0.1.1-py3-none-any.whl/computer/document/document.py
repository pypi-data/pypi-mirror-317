"""

- Use CSS page-break-after: always; for page breaks.
- Set explicit height (e.g., height: 297mm; for A4) for full-page content.
- Example HTML structure for multi-page:

    <div style="page-break-after: always;">
        <!-- Content for page 1 -->
    </div>
    <div style="page-break-after: always;">
        <!-- Content for page 2 -->
    </div>
    
"""

import pdfkit

class Document:
    def __init__(self, computer):
        self.computer = computer

    def html_to_pdf(self, html_file, pdf_file):
        # Configure wkhtmltopdf options
        options = {
            'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None,  # Allow loading local files
            'print-media-type': None,  # Use print media CSS
            'background': None,  # Enable background graphics
        }

        try:
            # Convert HTML to PDF
            print("Converting HTML to PDF...")
            pdfkit.from_file(html_file, pdf_file, options=options)
            print(f"PDF saved as {pdf_file}")

        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise