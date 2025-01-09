from typing import List, Any

# Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os

def load_pdf_documents(input_dir: str) -> List:
    """Load PDF documents from the specified directory."""
    # Get the absolute path to the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    input_path = os.path.join(project_root, "test_data", "input")
    
    docs = []
    for file in os.listdir(input_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(input_path, file))
            docs.extend(loader.load())
    return docs

def create_text_chunks(documents: List, chunk_size: int = 1000, chunk_overlap: int = 200) -> List:
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

def setup_vector_store(chunks: List) -> Chroma:
    """Initialize the vector store with document chunks."""
    # Get path for persistent storage
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    db_dir = os.path.join(project_root, "chroma_db")
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    
    # Create vector store with persistence
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir
    )

def create_rag_chain(vector_store: Chroma, model_name: str = "llama3.1") -> Any:
    """Create the RAG chain with retriever and LLM."""
    llm = Ollama(model=model_name)
    
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question based only on the following context: {context}
        Think step by step before providing a detailed answer.
        I will tip you 1000$ if you answer correctly and user finds it helpful.
        Question: {input}
        """
    )
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector_store.as_retriever()
    return create_retrieval_chain(retriever, document_chain)

def askRag(prompt: str):
    # Load documents
    docs = load_pdf_documents("input")
    
    # Create chunks
    chunks = create_text_chunks(docs)
    
    # Setup vector store
    db = setup_vector_store(chunks)
    
    # Create RAG chain
    chain = create_rag_chain(db)
    
    # Example query
    response = chain.invoke({
        "input": prompt
    })
    
    return response['answer']

if __name__ == "__main__":
    print(askRag("What is the machine specs that is used to train the model?"))