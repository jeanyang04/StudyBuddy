import streamlit as st

from rag.rag import askRag

st.markdown("""
<style>
.stTextInput {
    position: fixed;
    bottom: 3rem;
    padding: 1rem;
    z-index: 100;
    left: 50%;
    transform: translateX(-50%);
}
</style>
""", unsafe_allow_html=True)

st.title("Study Buddy")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Define a callback function to handle the input
def handle_input():
    if st.session_state.prompt_input:
        prompt = st.session_state.prompt_input
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Clear the input by setting the value before the next rerun
        st.session_state.prompt_input = ""
        response = askRag(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Use the on_change parameter to trigger the callback
prompt = st.text_input(
    "Enter your prompt",
    key="prompt_input",
    autocomplete="off",
    on_change=handle_input
)

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.markdown("<div style='margin-bottom:7rem'></div>", unsafe_allow_html=True)

