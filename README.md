# StudyBuddy

StudyBuddy is an interactive web-based application that empowers students and professionals with an AI-powered study assistant. Using Retrieval-Augmented Generation (RAG), it enables users to upload PDFs and engage in meaningful conversations about their content through an intuitive chat interface.

## Features

- **Upload Multiple PDFs**: Dynamically add and remove PDF documents
- **Intelligent Question-Answering**: Get AI-generated responses based on your uploaded documents
- **Real-Time Interaction**: Seamless chat interface for natural conversations
- **Persistent Database**: Efficient document management using ChromaDB

## Tech Stack

- **Frontend**: Streamlit
- **Backend**:
  - ChromaDB for vector database management
  - HuggingFace Embeddings for semantic text embeddings
  - DeepSeek API for LLM responses

## Key Dependencies

- langchain
- streamlit
- chromadb
- openai

## How It Works

### PDF Processing
The application uses PYPDFLoader to extract text from uploaded PDFs. The extracted content is then split into manageable chunks using RecursiveCharacterTextSplitter for optimal embedding generation.

### Embedding Generation
- Utilizes the all-MiniLM-L6-v2 embedding model
- Chosen for optimal balance between performance and efficiency
- Embeddings are stored in ChromaDB for quick retrieval

### Language Model
- Powered by DeepSeek's API
- Selected for cost-effectiveness and reliability
- Outperforms local LLM alternatives in testing

### Query Processing Workflow
1. User query is converted to an embedding
2. ChromaDB searches for relevant document chunks
3. Top-ranked chunks are provided as context
4. LLM generates coherent responses based on context and query

## Usage Example

1. **Upload Documents**
   - Drag and drop PDFs into the upload area

2. **Ask Questions**
   - Type questions about your documents in the chat
   - Example: "What are the causes of climate change?"

3. **Manage Documents**
   - Add or remove PDFs as needed
   - Reference material updates dynamically

4. **Review Responses**
   - Watch as AI generates real-time answers based on your documents

## Current Limitations

1. **Embedding Quality**
   - Document retrieval effectiveness depends on embedding accuracy

2. **Local Deployment**
   - Currently limited to offline use (1-week project constraint)

3. **PDF Parsing**
   - Complex diagrams and images may affect retrieval accuracy

4. **UI Customization**
   - Streamlit limitations affect frontend flexibility

## Future Development Roadmap

1. **Enhanced Query Processing**
   - LLM-based prompt preprocessing
   - Implementation of reranking models

2. **Expanded Functionality**
   - Web deployment with user authentication
   - Support for additional file formats (CSV, TXT)
   - Multi-chat session management

## Contact

jeanyang.chen@gmail.com
