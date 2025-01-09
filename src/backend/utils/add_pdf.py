import os
from backend.chromadb import get_chroma_db
from rag.rag import create_text_chunks

def add_pdf(file_path):
    target_dir = "pdf_files/"
    os.makedirs(target_dir, exist_ok=True)
    file_name = os.path.basename(file_path)
    target_file = os.path.join(target_dir, file_name)
    os.rename(file_path, target_file)

    # Process and store embeddings
    chunks = create_text_chunks(target_file) 
    db = get_chroma_db()
    db.add_documents(chunks)
    print(f"✅ PDF added to {target_file}")
