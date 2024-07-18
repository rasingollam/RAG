import tiktoken
from langchain_openai import OpenAIEmbeddings
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def read_text_file(file_path):
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
    
    ###### DOCUMENT ######
    
    document = read_text_file(text_file_path)
    # doc_tokens = num_tokens_from_string(document, "cl100k_base")
    # print(doc_tokens)
    question = "What is the content of the text?"
    # question_tokens = num_tokens_from_string(question, "cl100k_base")
    # print(question_tokens)
    
    ###### TEXT EMBEDDING MODEL ######
    
    embd = OpenAIEmbeddings()
    query_result = embd.embed_query(question)
    document_result = embd.embed_query(document)
    # print(len(document_result))
    
    ###### COSINE SIMILARITY ######
    
    similarity = cosine_similarity(query_result, document_result)
    print("Cosine Similarity:", similarity)
    
    ###### SPLITTER ######
    
    # Split
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=300, chunk_overlap=50)
    # Make splits
    splits = text_splitter.split_documents(document)
    print(splits)

if __name__ == "__main__":
    main()
