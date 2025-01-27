from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
import time

PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
API_ADDRESS = "https://api.deepseek.com"

embed_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
pc = Pinecone(api_key=PINECONE_API_KEY)
llm = OpenAI(OPENAI_API_KEY, API_ADDRESS)

index_name = "studybuddy-embeddings"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    ) 

# Wait for the index to be ready
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

# --- Streamlit App ---
st.title("Simple RAG Demo")

# Password protection
password = st.text_input("Enter password:", type="password")
if password != st.secrets["PASSWORD"]:
    st.stop()

# Initialize session state for document tracking
if 'uploaded_docs' not in st.session_state:
    st.session_state.uploaded_docs = {}  # Format: {doc_id: {"name": "file.pdf", "namespace": "ns123"}}

# --- File Upload & Processing ---
uploaded_file = st.file_uploader("Upload PDF document", type="pdf")

if st.session_state.uploaded_docs:
    # Create dropdown of document names
    doc_names = [f"{details['name']} ({doc_id})" 
                for doc_id, details in st.session_state.uploaded_docs.items()]
    selected_doc = st.selectbox("Select document to delete", doc_names)
    
    # Extract doc_id from selection
    selected_doc_id = selected_doc.split("(")[-1].rstrip(")")
    
    if st.button("Delete Selected Document"):
        # # Delete from Pinecone
        # namespace = st.session_state.uploaded_docs[selected_doc_id]["namespace"]
        # index.delete(delete_all=True, namespace=namespace)
        
        # Remove from session state
        del st.session_state.uploaded_docs[selected_doc_id]
        
        st.success("Document deleted successfully!")
else:
    st.info("No documents uploaded yet")

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
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # # Generate a response using the OpenAI API.
    # stream = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": m["role"], "content": m["content"]}
    #         for m in st.session_state.messages
    #     ],
    #     stream=True,
    # )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
