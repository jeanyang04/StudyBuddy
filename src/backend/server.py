from backend.utils import add_pdf, remove_pdf
from backend.utils.retriever_chain import retrieve_response
from backend.chromadb import get_chroma_db

def handle_query(query):
    db = get_chroma_db()
    response = retrieve_response(query, db)
    return response.to_json()

def handle_add_pdf(file_path):
    add_pdf(file_path)

def handle_remove_pdf(file_name):
    remove_pdf(file_name)
