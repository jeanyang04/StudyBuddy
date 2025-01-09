from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoModel, AutoTokenizer

CHROMA_DB_PATH = "../../test_data/chroma_db"
CHROMA_DB_INSTANCE = None

def get_chroma_db():
    global CHROMA_DB_INSTANCE
    if not CHROMA_DB_INSTANCE:
        # Define tokenizer and model explicitly
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

        # Pass tokenizer and model to HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(model=model, tokenizer=tokenizer)

        CHROMA_DB_INSTANCE = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings  # Correct argument
        )
    print(f"✅ Init ChromaDB {CHROMA_DB_INSTANCE} from {CHROMA_DB_PATH}")
    return CHROMA_DB_INSTANCE
