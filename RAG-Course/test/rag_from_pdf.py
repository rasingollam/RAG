import warnings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Suppress DeprecationWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
    text_file_path = "pdf_to_text\\data\\converted_text_files\\508_1716287433658.txt"
    question = "What is the company?"

    # Read document
    document = read_text_file(text_file_path)
    if document is None:
        return

    # Create a Document object and split
    doc = Document(page_content=document)
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=300, chunk_overlap=50)
    splits = text_splitter.split_documents([doc])

    # Create vector store and retriever
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

    # Create prompt template
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Create LLM and RAG chain
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Invoke RAG chain and print result
    result = rag_chain.invoke(question)
    print(result.strip())

if __name__ == "__main__":
    main()
