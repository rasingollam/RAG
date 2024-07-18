def read_text_file(file_path):
    """
    Read and return the contents of a text file.

    Args:
    file_path (str): The path to the text file.

    Returns:
    str: The contents of the text file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def main():
    # Path to the text file
    text_file_path = "pdf_to_text/data/converted_text_files/Additional_Attendee_payment_-_1147.txt"
    
    # Read the contents of the text file
    text_content = read_text_file(text_file_path)
    
    if text_content:
        print("Text file content:")
        print(text_content)
    else:
        print("Failed to read the text file.")

if __name__ == "__main__":
    main()
