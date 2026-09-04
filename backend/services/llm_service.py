from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from backend.utils.pdf_loader import load_pdf
from backend.models.document import DocumentModel
from backend.llm.model import model
from backend.llm.prompts import prompt
from backend.llm.chain import llm_chain
from backend.rag.embeddings import embeddings
from backend.rag.splitter import split_documents
from backend.rag.vector_store import create_vector_store
from backend.rag.retriever import get_retriever
from backend.utils.format_docs import format_docs
from backend.repositories.document_repository import get_file_path


def chat_service(db: Session, document_id: UUID, question: str):
    file_path = get_file_path(document_id=document_id, db=db)

    documents = load_pdf(file_path=file_path)

    chunks = split_documents(documents=documents)

    vector_store = create_vector_store(chunks=chunks)

    retriever = get_retriever(vector_store)
    
    chain = (
        RunnableParallel({
            'context': retriever | format_docs,
            'question': RunnablePassthrough()
        })
        | llm_chain
    )

    response = chain.invoke(question)

    return response