from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from backend.core.config import get_db
from backend.services.document_service import create_document, list_documents

doc_router = APIRouter(
    prefix='/document'
)

@doc_router.post("/upload")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):

    pdf_id = create_document(file=file, db=db)

    return {
        "pdf_id": pdf_id,
        "filename": file.filename
    }

@doc_router.get("/")
def get_documents(db: Session = Depends(get_db)):
    return list_documents(db=db)