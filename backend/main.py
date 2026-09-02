from fastapi import FastAPI

from backend.api.routes.document import doc_router
from backend.api.routes.llm import llm_router

app = FastAPI()

app.include_router(doc_router)
app.include_router(llm_router)