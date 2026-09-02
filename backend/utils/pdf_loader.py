from pypdf import PdfReader
from langchain_core.documents import Document

def load_pdf(file_path: str) -> list[Document]:
    reader = PdfReader(file_path)
    documents = []
    
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
    
        doc = Document(
            page_content=text,
            metadata={"source": file_path, "page": page_num}
        )
        documents.append(doc)
        
    return documents