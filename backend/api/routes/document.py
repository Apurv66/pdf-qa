from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid
from pathlib import Path
import shutil

from backend.models.document import DocumentModel
from backend.core.config import get_db

doc_router = APIRouter(
    prefix='/document'
)

@doc_router.post("/upload")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):

    pdf_id = str(uuid.uuid4())

    file_path = Path("uploads") / f"{pdf_id}.pdf"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = DocumentModel(
        id=pdf_id,
        filename=file.filename,
        file_path=str(file_path)
    )

    db.add(document)
    db.commit()

    return {
        "pdf_id": pdf_id,
        "filename": file.filename
    }

@doc_router.get("/")
def get_documents(db: Session = Depends(get_db)):
    stmt = select(DocumentModel.id, DocumentModel.filename)

    result = db.execute(stmt)
    documents = result.all()

    return [
        {
            "id": document.id,
            "filename": document.filename
        }
        for document in documents
    ]