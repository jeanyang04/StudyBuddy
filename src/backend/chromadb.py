from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CHROMA_DB_PATH = "../../test_data/chroma_db"
CHROMA_DB_INSTANCE = None

def get_chroma_db():
    global CHROMA_DB_INSTANCE
    if not CHROMA_DB_INSTANCE:
        CHROMA_DB_INSTANCE = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding=HuggingFaceEmbeddings(model="all-MiniLM-L6-v2")
        )
    print(f"✅ Init ChromaDB {CHROMA_DB_INSTANCE} from {CHROMA_DB_PATH}")
    return CHROMA_DB_INSTANCE
