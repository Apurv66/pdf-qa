from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv

from backend.utils.pdf_loader import load_pdf
from backend.models.document import DocumentModel

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model='gemini-embedding-001')

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

def chat_service(db: Session, id: UUID, question: str):
    stmt = select(DocumentModel.file_path).where(DocumentModel.id==id)
    try:
        result = db.execute(stmt)
        file_path = result.scalar_one_or_none()

    except SQLAlchemyError:
        raise

    documents = load_pdf(file_path=file_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    retriever = vector_store.as_retriever(search_kwargs={'k': 4})


    prompt_template = """
You are a helpful document question-answering assistant.

Answer the user's question using only the provided context.

Rules:

1. Use only information from the context.
2. If the answer is not present in the context, say: "I couldn't find the answer in the provided document."
3. Do not make up or assume information.
4. Give a clear and concise answer.
5. If the context contains conflicting information, mention the conflict.

Context:
{context}

Question:
{question}

Answer:
"""
    prompt = ChatPromptTemplate.from_template(prompt_template)
    ouput_parser = StrOutputParser()

    def format_docs(chunks):
        return "\n\n".join(chunk.page_content for chunk in chunks)

    chain = (
        RunnableParallel({
            'context': retriever | format_docs,
            'question': RunnablePassthrough()
        })
        | prompt
        | model
        | ouput_parser
    )

    response = chain.invoke(question)

    return response