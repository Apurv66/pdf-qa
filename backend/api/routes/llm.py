from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.schemas.llm_schema import UserRequest
from backend.services.llm_service import chat_service
from backend.core.config import get_db

llm_router = APIRouter(
    prefix='/llm'
)

@llm_router.post('/chat')
def chat(user_request: UserRequest, db: Session = Depends(get_db)):
    response = chat_service(db=db, id=user_request.id, question=user_request.question)

    return {'ai_response': response}
    