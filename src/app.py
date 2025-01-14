import os
import streamlit as st
from rag.rag import askRag

height = 500
icon = ":robot:"

# Define a callback function to handle the input
def handle_input(prompt):
    response = askRag(prompt, path="data/uploaded_files")

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})

    for message in st.session_state.messages:
        messages.chat_message(message["role"]).write(message["content"])

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

if "clicked" not in st.session_state:
    st.session_state.clicked = False

st.set_page_config(page_title="Study Buddy", page_icon=icon, layout="wide")  

def toggle_clicked():
    st.session_state.clicked = not st.session_state.clicked

if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploaded_files")):
    for file in os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploaded_files")):
        os.remove(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploaded_files", file))
else:
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploaded_files"))

col1, col2 = st.columns([4, 1], gap="large", vertical_alignment="bottom")
with col1:
    st.header("Study Buddy")
with col2:
    if st.session_state.clicked:
        st.button("Clear all files", on_click=toggle_clicked)
    else:
        st.button("Upload Files", on_click=toggle_clicked)

if st.session_state.clicked:
    st.session_state.uploaded_files = st.file_uploader("Upload multiple pdf files", accept_multiple_files=True, type="pdf")

    if st.session_state.uploaded_files:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploaded_files")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        else:
            for file in os.listdir(data_dir):
                os.remove(os.path.join(data_dir, file))

    for file in st.session_state.uploaded_files:
        with open(os.path.join(data_dir, file.name), "wb") as f:
            f.write(file.getbuffer())
    st.session_state.uploaded_files = None

messages = st.container(border=True, height=height)

# Add this function to check if files exist in the upload directory
def files_exist_in_upload_dir():
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploaded_files")
    return any(file.endswith('.pdf') for file in os.listdir(upload_dir)) if os.path.exists(upload_dir) else False

if files_exist_in_upload_dir():
    if prompt := st.text_input("Enter your prompt", key="prompt_input", autocomplete="off", placeholder="Ask me anything about the files uploaded"):
        handle_input(prompt)
else:
    st.session_state.messages = []
    st.text_input("Enter your prompt", key="prompt_input", disabled=True, placeholder="Please upload PDF files first")
    st.info("⚠️ Please upload PDF files before asking questions.")