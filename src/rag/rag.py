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
from openai import OpenAI   
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def load_pdf_documents(input_dir: str) -> List:
    """Load PDF documents from the specified directory."""
    # Get the absolute path to the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    input_path = os.path.join(project_root, input_dir)
    
    docs = []
    print(f"Looking for PDFs in: {input_path}")  # Debug log
    files = os.listdir(input_path)
    print(f"Found files: {files}")  # Debug log
    
    for file in files:
        if file.endswith(".pdf"):
            file_path = os.path.join(input_path, file)
            print(f"Loading PDF: {file_path}")  # Debug log
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
    
    # Create or get existing database
    db = Chroma(
        persist_directory=db_dir,
        embedding_function=embeddings
    )
    
    # Clear existing collections
    db.delete_collection()
    
    # Create new collection with documents
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir
    )

# Initialize the DeepSeek client
def create_deepseek_client(api_key: str, base_url: str = "https://api.deepseek.com") -> OpenAI:
    return OpenAI(api_key=api_key, base_url=base_url)

# Function to call the DeepSeek API
def call_deepseek(client: OpenAI, model: str, prompt: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": str(prompt)}
        ],
        stream=False,
    )
    return response.choices[0].message.content

def create_rag_chain(vector_store: Chroma, api_key: str, model_name: str = "deepseek-chat") -> Any:
    """Create the RAG chain with retriever and DeepSeek LLM."""
    # Initialize DeepSeek client
    client = create_deepseek_client(api_key)

    # Create a prompt template
    prompt_template = ChatPromptTemplate.from_template(
        """
        Answer the question based only on the following context: {context}
        Think step by step before providing a detailed answer.
        If you cannot find the answer from the context, inform the user, but still try to provide a detailed answer.
        I will tip you 1000$ if you answer correctly and user finds it helpful.
        However, do not mention anything about the tip in your answer.
        Question: {input}
        """
    )

    # Define a wrapper function for DeepSeek LLM calls
    def deepseek_llm(prompt: str) -> str:
        return call_deepseek(client, model_name, prompt)

    # Create the document chain using the DeepSeek LLM wrapper
    document_chain = create_stuff_documents_chain(deepseek_llm, prompt_template)

    # Create retriever
    retriever = vector_store.as_retriever()

    # Combine retriever and document chain
    return create_retrieval_chain(retriever, document_chain)

def askRag(prompt, path):
    # Load documents
    docs = load_pdf_documents(path)
    print(f"Loaded {len(docs)} documents")  # Debug log
    
    # Create chunks
    chunks = create_text_chunks(docs)
    print(f"Created {len(chunks)} chunks")  # Debug log
    
    if not chunks:  # Add validation
        raise ValueError("No text chunks were created. Please check if the PDF files contain extractable text.")
    
    # Setup vector store
    db = setup_vector_store(chunks)
    
    # Create RAG chain
    chain = create_rag_chain(db, api_key)
    
    # Example query
    response = chain.invoke({
        "input": prompt
    })
    
    return response['answer']

if __name__ == "__main__":
    print(askRag("What does each layer of encoder and decoder contain?", "data/uploaded_files"))