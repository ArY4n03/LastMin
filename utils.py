from langchain_core.prompts  import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader,PyPDFLoader,WebBaseLoader
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.vectorstores import Chroma
from tkinter import messagebox as msg


prompt = ChatPromptTemplate.from_template("""
Answer the question based on the given context
<context>
{context}
</context>
                                           
question:{input}
"""
)


llm = OllamaLLM(model='llama3.1')
embeddings = OllamaEmbeddings(model="nomic-embed-text")
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
    db = Chroma.from_documents(document,embeddings) #creating Chroma database
    retriver = db.as_retriever()

    document_chain = create_stuff_documents_chain(llm,prompt)
    retriveval_chain = create_retrieval_chain(retriver,document_chain)
    print("chain created")
    return retriveval_chain