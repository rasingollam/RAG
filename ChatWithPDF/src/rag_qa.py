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

class RAGQuestionAnswerer:
    def __init__(self, text_file_path):
        self.text_file_path = text_file_path
        self.setup_rag_system()

    def read_text_file(self):
        try:
            with open(self.text_file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File not found at {self.text_file_path}")
            return None
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return None

    def setup_rag_system(self):
        document = self.read_text_file()
        if document is None:
            raise ValueError("Failed to read the text file")

        doc = Document(page_content=document)
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=300, chunk_overlap=50)
        splits = text_splitter.split_documents([doc])

        self.vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 1})

        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        self.prompt = ChatPromptTemplate.from_template(template)

        self.llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
        self.rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def answer_question(self, question):
        result = self.rag_chain.invoke(question)
        return result.strip()
