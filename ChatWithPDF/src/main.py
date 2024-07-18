import os
from pdf_converter import convert_pdf_to_text
from rag_qa import RAGQuestionAnswerer

def main():
    print("Welcome to ChatWithPDF!")
    
    while True:
        # Get PDF file path from user
        pdf_path = input("Please enter the path to your PDF file (or 'quit' to exit): ").strip()
        
        if pdf_path.lower() == 'quit':
            break
        
        if not os.path.isfile(pdf_path) or not pdf_path.lower().endswith('.pdf'):
            print("Invalid file path or not a PDF file. Please try again.")
            continue
        
        # Convert PDF to text
        text_file_path = convert_pdf_to_text(pdf_path)
        
        if text_file_path:
            print(f"PDF converted successfully. Text file saved at: {text_file_path}")
            
            try:
                # Initialize RAG system
                rag_qa = RAGQuestionAnswerer(text_file_path)
                
                # Question answering loop
                while True:
                    question = input("\nEnter your question (or 'back' to choose another PDF, 'quit' to exit): ").strip()
                    if question.lower() == 'back':
                        break
                    if question.lower() == 'quit':
                        return
                    
                    answer = rag_qa.answer_question(question)
                    print(f"\nAnswer: {answer}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        else:
            print("Failed to convert the PDF. Please try another file.")
    
    print("Thank you for using ChatWithPDF!")

if __name__ == "__main__":
    main()
