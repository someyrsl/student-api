from pydantic import BaseModel
from sqlalchemy import  Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(BaseModel):
    name: str
    age: int
    grade: float

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    grade = Column(Float)