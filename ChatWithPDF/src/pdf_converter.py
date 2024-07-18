import os
import re
from PyPDF2 import PdfReader

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename).replace(' ', '_')

def convert_pdf_to_text(pdf_path):
    # Implementation details will be added later
    pass
