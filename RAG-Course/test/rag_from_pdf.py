
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# Load the text file
def load_text(file_path):
    loader = TextLoader(file_path)
    documents = loader.load()
    return documents

# Split the text into chunks
def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
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
    # Path to the text file
    text_file_path = "pdf_to_text/data/converted_text_files/Additional_Attendee_payment_-_1147.txt"
    
    # Read the contents of the text file
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()
    
    # Print the content (you can remove this line if you don't want to print it)
    print("Text file content:")
    print(text_content)
    
    # documents = load_text(text_file_path)
    # texts = split_text(documents)
    # vectorstore = create_vector_store(texts)
    # qa_chain = setup_qa_chain(vectorstore)
    
    # while True:
    #     query = input("Enter your question (or 'quit' to exit): ")
    #     if query.lower() == 'quit':
    #         break
    #     result = qa_chain.run(query)
    #     print(f"Answer: {result}")

if __name__ == "__main__":
    main()
