from uuid import UUID
from backend.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class DocumentModel(Base):
    __tablename__='documents'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)