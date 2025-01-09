from typing import List, Any

# Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def load_pdf_documents(input_dir: str) -> List:
    """Load PDF documents from the specified directory."""
    docs = []
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(input_dir, file))
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
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    return Chroma.from_documents(chunks, embeddings)
