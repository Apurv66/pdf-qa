from pydantic import BaseModel
from uuid import UUID

class UserRequest(BaseModel):
    id: UUID
    question: str