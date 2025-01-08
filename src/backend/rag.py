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

def main():
    # Load documents
    docs = load_pdf_documents("../../test_data/input")
    
    # Create chunks
    chunks = create_text_chunks(docs)
    
    # Setup vector store
    db = setup_vector_store(chunks)
    
    # Create RAG chain
    chain = create_rag_chain(db)
    
    # Example query
    response = chain.invoke({
        "input": "What is the machine specs that is used to train the model?"
    })
    
    print(response['answer'])

if __name__ == "__main__":
    main() 