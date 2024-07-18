import os
from pdf_converter import convert_pdf_to_text
from rag_qa import RAGQuestionAnswerer

def main():
    print("Welcome to ChatWithPDF!")
    
    # Get PDF file path from user
    pdf_path = input("Please enter the path to your PDF file: ").strip()
    
    # Convert PDF to text
    text_file_path = convert_pdf_to_text(pdf_path)
    
    if text_file_path:
        print(f"PDF converted successfully. Text file saved at: {text_file_path}")
        
        # Initialize RAG system
        rag_qa = RAGQuestionAnswerer(text_file_path)
        
        # Question answering loop
        while True:
            question = input("\nEnter your question (or 'quit' to exit): ").strip()
            if question.lower() == 'quit':
                break
            
            answer = rag_qa.answer_question(question)
            print(f"\nAnswer: {answer}")
    
    print("Thank you for using ChatWithPDF!")

if __name__ == "__main__":
    main()
