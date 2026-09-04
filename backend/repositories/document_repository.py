from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.models.document import DocumentModel

def save_document(filename, pdf_id, file_path, db: Session):
    document = DocumentModel(
        id=pdf_id,
        filename=filename,
        file_path=str(file_path)
    )

    db.add(document)
    db.commit()
    return document

def get_all_documents(db: Session):
    stmt = select(DocumentModel.id, DocumentModel.filename)
    
    result = db.execute(stmt)
    documents = result.all()
    return documents