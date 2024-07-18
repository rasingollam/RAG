import os
import re
from PyPDF2 import PdfReader

def sanitize_filename(filename):
    # Remove invalid characters and replace spaces with underscores
    return re.sub(r'[<>:"/\\|?*]', '', filename).replace(' ', '_')

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

        # Generate sanitized output file name
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        sanitized_name = sanitize_filename(base_name)
        output_path = os.path.join(output_dir, f"{sanitized_name}.txt")

        # Write text to output file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)

        print(f"Converted {pdf_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")

def main():
    while True:
        pdf_directory = input("Enter the path to the directory containing PDF files: ").strip()
        if os.path.isdir(pdf_directory):
            break
        else:
            print(f"Error: '{pdf_directory}' is not a valid directory. Please try again.")

    output_directory = os.path.join(os.path.dirname(pdf_directory), "converted_text_files")

    pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
    total_files = len(pdf_files)

    if total_files == 0:
        print("No PDF files found in the specified directory.")
    else:
        print(f"Found {total_files} PDF file(s) to convert.")

        for index, filename in enumerate(pdf_files, start=1):
            pdf_path = os.path.join(pdf_directory, filename)
            print(f"Converting file {index} of {total_files}: {filename}")
            convert_pdf_to_text(pdf_path, output_directory)

        print("Conversion process completed.")
        print(f"Converted text files can be found in: {output_directory}")

if __name__ == "__main__":
    main()
