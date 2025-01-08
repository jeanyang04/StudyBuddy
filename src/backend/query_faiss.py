import faiss
import numpy as np
import json
import sys

def query_index(query, index_file, model_name="all-MiniLM-L6-v2", top_k=5):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    
    # Load the FAISS index
    index = faiss.read_index(index_file)
    
    # # Load the filenames mapping
    # with open(filenames_file, "r", encoding="utf-8") as f:
    #     filenames = json.load(f)
    
    # # Load the embeddings for metadata retrieval
    # with open(embeddings_file, "r", encoding="utf-8") as f:
    #     embeddings = json.load(f)
    
    # Generate the query embedding
    query_embedding = model.encode(query).astype("float32")
    
    # Search the FAISS index
    distances, indices = index.search(np.array([query_embedding]), top_k)
    print(distances, indices)

    # Retrieve the text corresponding to the indices
    results = []
    for idx in indices:
        results.append({
            "text": None,  # To be populated below
        })
    
    # Populate the "text" field by reading the corresponding Markdown files
    for result in results:
        md_file = "./test_data/output/NIPS-2017-attention-is-all-you-need-Paper.md"
        with open(md_file, "r", encoding="utf-8") as f:
            result["text"] = f.read()
     
    return results

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python query_faiss.py <query> <index_file> <top_k>")
        sys.exit(1)
    
    query = sys.argv[1]
    index_file = sys.argv[2]
    top_k = int(sys.argv[3])
    
    results = query_index(query, index_file, top_k=top_k)
    print("Results:")
    for result in results:
        print(f"Filename: {result['filename']}")
        print(f"Distance: {result['distance']}")
        print(f"Text: {result['text']}")
        print()
