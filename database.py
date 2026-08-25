from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("sqlite:///school.db")
SessionLocal = sessionmaker(bind = engine)

def get_connection():
    return SessionLocal()

def init_db():
    Base.metadata.create_all(engine)
