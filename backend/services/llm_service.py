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


def chat_service(db: Session, id: UUID, question: str):
    stmt = select(DocumentModel.file_path).where(DocumentModel.id==id)
    try:
        result = db.execute(stmt)
        file_path = result.scalar_one_or_none()

    except SQLAlchemyError:
        raise

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