from backend.utils import add_pdf, remove_pdf
from backend.utils.retriever_chain import retrieve_response


def handle_query(query):
    response = retrieve_response(query)
    return response.to_json()

def handle_add_pdf(file_path):
    add_pdf(file_path)

def handle_remove_pdf(file_name):
    remove_pdf(file_name)
