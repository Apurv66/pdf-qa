from sqlalchemy.orm import Session
import uuid
from pathlib import Path
import shutil

from backend.repositories.document_repository import save_document, get_all_documents

def create_document(file, db: Session):
    pdf_id = uuid.uuid4()
    
    file_path = Path("uploads") / f"{pdf_id}.pdf"
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    save_document(filename=file.filename, pdf_id=pdf_id, file_path=file_path, db=db)

    return pdf_id

def list_documents(db: Session):
    documents = get_all_documents(db=db)
    
    return [
        {
            "id": document.id,
            "filename": document.filename
        }
        for document in documents
    ]