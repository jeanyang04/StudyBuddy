import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
import os
import hashlib
import tempfile

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if not os.getenv("OPENAI_API_KEY") else os.getenv("OPENAI_API_KEY")
API_ADDRESS = "https://api.deepseek.com"

embed_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
llm = OpenAI(api_key=OPENAI_API_KEY, base_url=API_ADDRESS)

# --- Streamlit App ---
st.title("Simple RAG Demo")

# Password protection
password = st.text_input("Enter password:", type="password")
secret = st.secrets["PASSWORD"] if not os.getenv("PASSWORD") else os.getenv("PASSWORD")
if password != secret:
    st.error("Incorrect password. Please try again.")
    st.stop()

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}
if 'vector_store' not in st.session_state:  # Store embeddings locally
    st.session_state.vector_store = None

# --- File Upload & Processing ---
uploaded_files = st.file_uploader("Upload PDF document", type="pdf", accept_multiple_files=True)

# Convert uploaded_files to a dictionary for easy comparison
def get_file_hash(file):
    return hashlib.md5(file.getvalue()).hexdigest()

current_files = {}
if uploaded_files:
    current_files = {get_file_hash(file): file for file in uploaded_files}

# Detect deletions
deleted_files = [
    file_id for file_id in st.session_state.uploaded_files
    if file_id not in current_files.keys()
]

for file_id in deleted_files:
    # Remove from session state
    del st.session_state.uploaded_files[file_id]
    
    # Optional: Delete associated data from vector store
    if st.session_state.vector_store:
        doc_chunks = [
            chunk for chunk in st.session_state.vector_store.docstore._dict.values()
            if chunk.metadata.get("source") == file_id
        ]
        st.session_state.vector_store.delete([chunk.page_id for chunk in doc_chunks])
    
    st.success(f"Deleted file with ID {file_id} and its associated data.")

# Process new uploads
try:
    for file_id, file_obj in current_files.items():
        if file_id not in st.session_state.uploaded_files:
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(file_obj.getbuffer())
                tmp_path = tmp_file.name
            
            # Load and split PDF
            loader = PyPDFLoader(tmp_path)
            pages = loader.load_and_split()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(pages)
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            # Add metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata["source"] = file_id
                chunk.metadata["page"] = i + 1
            
            st.write("DEBUG: vector_store before processing:", st.session_state.get("vector_store"))

            if st.session_state.vector_store is None:
                st.session_state.vector_store = FAISS.from_documents(chunks, embed_model)
                st.write("DEBUG: newly created vector_store:", st.session_state.vector_store)
            else:
                st.session_state.vector_store.add_documents(chunks)
                st.write("DEBUG: updated existing vector_store:", st.session_state.vector_store)
            
            st.session_state.uploaded_files[file_id] = file_obj
            st.success(f"Processed file with ID {file_id}")
except Exception as e:
    st.error(f"Error processing file: {str(e)}")

# Update session state with current files
st.session_state.uploaded_files = current_files

# Display uploaded files
st.write("### Uploaded Files")
for file_id, file_obj in st.session_state.uploaded_files.items():
    st.write(f"- {file_obj.name} (ID: {file_id})")

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if not st.session_state.vector_store:
    st.chat_input(key="prompt_input", disabled=True, placeholder="Please upload PDF files first")
    st.info("⚠️ Please upload PDF files before asking questions.")
else:
    if prompt := st.chat_input(placeholder="Ask me anything about the files uploaded"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Retrieve relevant chunks from FAISS
        docs = st.session_state.vector_store.similarity_search(prompt, k=3)
        context = "Relevant document excerpts:\n\n" + "\n\n".join(
            [f"📄 Excerpt from page {doc.metadata['page']}:\n{doc.page_content}" 
             for doc in docs]
        )

        # Create augmented prompt with context
        augmented_prompt = f"""Use the following context to answer the question. 
        If you don't know the answer, say you don't know. Be detailed and technical.
        
        Context:
        {context}
        
        Question: {prompt}
        
        Answer:"""
        
        # Generate response with context
        with st.spinner("Generating response..."):
            stream = llm.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful technical assistant."},
                    {"role": "user", "content": augmented_prompt}
                ],
                stream=True,
            )

        # Stream the response and show sources
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
            
            # Show document sources in expander
            with st.expander("📚 Source Documents Used"):
                for doc in docs:
                    st.write(f"**Page {doc.metadata['page']}**")
                    st.caption(doc.page_content[:500] + "...")
        
        st.session_state.messages.append({"role": "assistant", "content": response})