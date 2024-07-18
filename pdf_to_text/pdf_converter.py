import os
import sys
from PyPDF2 import PdfReader

def convert_pdf_to_text(pdf_path, output_dir):
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            
            # Extract text from each page
            text = ''
            for page in pdf.pages:
                text += page.extract_text()

        # Generate output file name
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.txt")

        # Write text to output file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)

        print(f"Converted {pdf_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python pdf_converter.py <pdf_directory>")
        sys.exit(1)

    pdf_directory = sys.argv[1]
    if not os.path.isdir(pdf_directory):
        print(f"Error: {pdf_directory} is not a valid directory")
        sys.exit(1)

    output_directory = os.path.join(os.path.dirname(pdf_directory), "converted_text_files")

    for filename in os.listdir(pdf_directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            convert_pdf_to_text(pdf_path, output_directory)

if __name__ == "__main__":
    main()
