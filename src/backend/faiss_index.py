import faiss
import numpy as np

def create_faiss_index(vector, dimension=384):
    """
    Create a FAISS index and add a single vector to it.
    
    Args:
        vector (list or np.array): The embedding vector to add
        dimension (int): Dimension of the embedding vector (default 384 for MiniLM-L6-v2)
        
    Returns:
        faiss.Index: The created FAISS index
    """
    # Convert vector to numpy array if it's a list
    vector_np = np.array([vector]).astype('float32')
    
    # Create the index
    index = faiss.IndexFlatL2(dimension)
    index.add(vector_np)
    return index

def add_to_faiss_index(index, vector):
    """
    Add a single vector to an existing FAISS index.
    
    Args:
        index (faiss.Index): The existing FAISS index
        vector (list or np.array): The embedding vector to add
    """
    vector_np = np.array([vector]).astype('float32')
    index.add(vector_np)

def save_faiss_index(index, index_path):
    """
    Save a FAISS index to disk.
    
    Args:
        index (faiss.Index): The FAISS index to save
        index_path (str): Path where to save the index
    """
    faiss.write_index(index, index_path)

def load_faiss_index(index_path):
    """
    Load a FAISS index from disk.
    
    Args:
        index_path (str): Path to the saved index
        
    Returns:
        faiss.Index: The loaded FAISS index
    """
    return faiss.read_index(index_path)


