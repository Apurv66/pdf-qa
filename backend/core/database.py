from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

class Base(DeclarativeBase):
    pass

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)