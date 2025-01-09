import os
from backend.chromadb import get_chroma_db

def remove_pdf(file_name):
    target_file = f"pdf_files/{file_name}"
    if os.path.exists(target_file):
        os.remove(target_file)
        # Remove embeddings from Chroma DB
        db = get_chroma_db()
        db.delete_collection(file_name)
        print(f"✅ PDF {file_name} removed.")
    else:
        print(f"❌ PDF {file_name} not found.")
