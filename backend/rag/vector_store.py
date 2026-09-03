from langchain_chroma import Chroma

from backend.rag.embeddings import embeddings

def create_vector_store(chunks):
    return Chroma.from_documents(documents=chunks, embedding=embeddings)