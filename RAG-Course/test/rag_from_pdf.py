import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# Load the PDF
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages

# Split the text into chunks
def split_text(pages):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(pages)
    return texts

# Create vector store
def create_vector_store(texts):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(texts, embeddings)
    return vectorstore

# Set up retrieval QA chain
def setup_qa_chain(vectorstore):
    llm = OpenAI(temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
    return qa_chain

def main():
    # Replace with your PDF file path
    pdf_path = "path/to/your/pdf/file.pdf"
    
    pages = load_pdf(pdf_path)
    texts = split_text(pages)
    vectorstore = create_vector_store(texts)
    qa_chain = setup_qa_chain(vectorstore)
    
    while True:
        query = input("Enter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        result = qa_chain.run(query)
        print(f"Answer: {result}")

if __name__ == "__main__":
    main()
