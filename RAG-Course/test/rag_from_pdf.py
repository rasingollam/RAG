
def main():
    # Path to the text file
    text_file_path = "pdf_to_text/data/converted_text_files/Additional_Attendee_payment_-_1147.txt"
    
    # Read the contents of the text file
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()
    
    # Print the content
    print("Text file content:")
    print(text_content)

if __name__ == "__main__":
    main()
