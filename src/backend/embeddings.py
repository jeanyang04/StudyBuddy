from sentence_transformers import SentenceTransformer

def embed_text(text, model_name="all-MiniLM-L6-v2"):
    """
    Embed a single text chunk using sentence transformers.
    
    Args:
        text (str): The text to embed
        model_name (str): Name of the sentence transformer model to use
        
    Returns:
        list: The embedding as a list of floats
    """
    model = SentenceTransformer(model_name)
    embedding = model.encode(text, show_progress_bar=False)
    return embedding.tolist()

# If you need to embed multiple chunks, you can add this helper function
def embed_chunks(chunks, model_name="all-MiniLM-L6-v2"):
    """
    Embed multiple text chunks using the same model instance.
    
    Args:
        chunks (list): List of text chunks to embed
        model_name (str): Name of the sentence transformer model to use
        
    Returns:
        list: List of embeddings
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks, show_progress_bar=True)
    return [embedding.tolist() for embedding in embeddings]

