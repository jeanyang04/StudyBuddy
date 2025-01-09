from backend.chromadb import get_chroma_db
from frontend.gui import chat


def main():
    # Initialize ChromaDB
    get_chroma_db()

    # Print a welcome message
    print("📚 Retrieval-Augmented Generation (RAG) System Booting Up...")
    print("💡 Add PDFs to 'pdf_files/' directory and interact via the chat interface.")
    
    # Run GUI
    chat()

if __name__ == "__main__":
    main()
