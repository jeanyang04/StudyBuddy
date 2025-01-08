import pymupdf4llm
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embeddings import embed_chunks
from faiss_index import create_faiss_index, add_to_faiss_index, save_faiss_index

def process_single_pdf(pdf_path, output_folder, chunk_size=1000, chunk_overlap=200):
    """
    Process a single PDF file: convert to markdown, split into chunks, create embeddings,
    and store in FAISS index.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_folder (str): Folder to save the outputs
        chunk_size (int): Size of text chunks
        chunk_overlap (int): Overlap between chunks
    
    Returns:
        tuple: (faiss_index, list of chunks, list of chunk_ids)
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Convert PDF to markdown
    md_text = pymupdf4llm.to_markdown(pdf_path)
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
        add_start_index=True
    )
    
    # Split into chunks
    chunks = text_splitter.split_text(md_text)
    
    # Create chunk IDs
    filename = os.path.basename(pdf_path)
    chunk_ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    
    # Get embeddings for all chunks
    embeddings = embed_chunks(chunks)
    
    # Initialize FAISS index with first vector
    index = create_faiss_index(embeddings[0])
    
    # Add remaining vectors to index
    for embedding in embeddings[1:]:
        add_to_faiss_index(index, embedding)
    
    # Save the index
    index_path = os.path.join(output_folder, "faiss.index")
    save_faiss_index(index, index_path)
    
    # Save chunks and their IDs for reference
    chunks_path = os.path.join(output_folder, "chunks.txt")
    with open(chunks_path, "w", encoding="utf-8") as f:
        for chunk_id, chunk in zip(chunk_ids, chunks):
            f.write(f"=== {chunk_id} ===\n{chunk}\n\n")
    
    return index, chunks, chunk_ids

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python pdf_processor.py <pdf_path> <output_folder>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_folder = sys.argv[2]
    
    index, chunks, chunk_ids = process_single_pdf(pdf_path, output_folder)
    print(f"Processed {len(chunks)} chunks from {pdf_path}")
    print(f"FAISS index saved with {index.ntotal} vectors")

