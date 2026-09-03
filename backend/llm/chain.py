from langchain_core.output_parsers import StrOutputParser

from backend.llm.prompts import prompt
from backend.llm.model import model

llm_chain = prompt | model | StrOutputParser()

