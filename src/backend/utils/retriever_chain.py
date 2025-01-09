from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


def create_rag_chain(vector_store: Chroma, model_name: str = "llama3.1"):
    """Create the RAG chain with retriever and LLM."""
    llm = Ollama(model=model_name)
    
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question based only on the following context: {context}
        Think step by step before providing a detailed answer.
        I will tip you 1000$ if you answer correctly and user finds it helpful.
        Question: {input}
        """
    )   
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector_store.as_retriever()
    return create_retrieval_chain(retriever, document_chain)

def retrieve_response(prompt: str, db: Chroma):
    # Create RAG chain
    chain = create_rag_chain(db)
    
    response = chain.invoke({
        "input": prompt
    })
    
    return response