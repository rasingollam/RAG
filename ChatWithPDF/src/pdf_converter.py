import os
import re
from PyPDF2 import PdfReader

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename).replace(' ', '_')

def convert_pdf_to_text(pdf_path):
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(pdf_path), "converted_text_files")
        os.makedirs(output_dir, exist_ok=True)

        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            
            # Extract text from each page
            text = ''
            total_pages = len(pdf.pages)
            for i, page in enumerate(pdf.pages, 1):
                text += page.extract_text()
                print(f"\rConverting: {(i / total_pages) * 100:.1f}%", end="", flush=True)

        # Generate sanitized output file name
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        sanitized_name = sanitize_filename(base_name)
        output_path = os.path.join(output_dir, f"{sanitized_name}.txt")

        # Write text to output file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)

        print(f"\nConverted {pdf_path} to {output_path}")
        return output_path
    except Exception as e:
        print(f"\nError converting {pdf_path}: {str(e)}")
        return None
