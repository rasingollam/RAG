import tiktoken
from langchain_openai import OpenAIEmbeddings
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

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
    
###### PART 01 : INDEXING ######
## ----------------------------------------------------------------------------------------------------------------
    
    # Path to the text file
    text_file_path = "pdf_to_text\\data\\converted_text_files\\508_1716287433658.txt"
    
    ###### DOCUMENT ######
    
    document = read_text_file(text_file_path)
    # doc_tokens = num_tokens_from_string(document, "cl100k_base")
    # print(doc_tokens)
    question = "What is the company?"
    # question_tokens = num_tokens_from_string(question, "cl100k_base")
    # print(question_tokens)
    
    ###### TEXT EMBEDDING MODEL ######
    
    embd = OpenAIEmbeddings()
    query_result = embd.embed_query(question)
    document_result = embd.embed_query(document)
    # print(len(document_result))
    
    ###### COSINE SIMILARITY ######
    
    similarity = cosine_similarity(query_result, document_result)
    # print("Cosine Similarity:", similarity)
    
    ###### SPLITTER ######
    
    # Create a Document object
    doc = Document(page_content=document)

    # Split
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=300, chunk_overlap=50)
    # Make splits
    splits = text_splitter.split_documents([doc])
    
    # ###### VECTOR STORES ######
    # vectorstore = Chroma.from_documents(documents=splits, 
    #                                 embedding=OpenAIEmbeddings())

    # retriever = vectorstore.as_retriever()
    # print(retriever)
    
###### PART 02 : RETRIEVAL ######
## ----------------------------------------------------------------------------------------------------------------
    vectorstore = Chroma.from_documents(documents=splits, 
                                    embedding=OpenAIEmbeddings())


    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    # print(retriever)
    
    docs = retriever.get_relevant_documents(question)
    # print(len(docs))    

###### PART 03 : GENARATION ######
## ----------------------------------------------------------------------------------------------------------------

    # Prompt
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    # print(prompt)
    
    # LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Chain
    chain = prompt | llm
    
    # Run
    chain.invoke({"context":docs,"question":question})

    prompt_hub_rag = hub.pull("rlm/rag-prompt")
    # print(prompt_hub_rag)

    ###### VECTOR STORES ######
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke(question)
    # Remove any warnings or additional text before the actual result
    clean_result = result.split('---')[-1].strip()
    print(clean_result)




if __name__ == "__main__":
    main()
