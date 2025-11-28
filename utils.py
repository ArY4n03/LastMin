from langchain_core.prompts  import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader,PyPDFLoader,WebBaseLoader
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.vectorstores import Chroma
from tkinter import messagebox as msg
from dotenv import load_dotenv
import os
load_dotenv()

prompt = ChatPromptTemplate.from_template("""
Answer the question based on the given context
<context>
{context}
</context>
                                           
question:{input}
"""
)

llm_name= os.getenv("local_llm")
embedding_name = os.getenv("embedding_llm")
llm = OllamaLLM(model=llm_name)
embeddings = OllamaEmbeddings(model=embedding_name)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

def load_document(file=None,FileType=None):
    try:
        if FileType == "text" and file:
            doc = TextLoader(file).load() #loading text file
            document = text_splitter.split_documents(doc) #spilliting documents into chunks
            return document
        if FileType == "pdf":
            doc = PyPDFLoader(file).load()
            document = text_splitter.split_documents(doc)
            return document
    except Exception as e:
        msg.showwarning(message="Error Occured while loading document",title="Catastropic error")
        print(e)
        return None
    

def create_retrieval_chain_(document):
    if document:
        db = Chroma.from_documents(document,embeddings) #creating Chroma database for embedded chunks
        retriver = db.as_retriever()

        document_chain = create_stuff_documents_chain(llm,prompt) #LLM chains combining propmt and document
        retriveval_chain = create_retrieval_chain(retriver,document_chain) # retrieval chain
        return retriveval_chain