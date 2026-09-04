from pydantic import BaseModel
from sqlalchemy import  Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Student(BaseModel):
    name: str
    age: int

class Grade(BaseModel):
    score: float
    subject: str

class Users(BaseModel):
    username: str
    password: str

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    age = Column(Integer)
    
    grades = relationship("GradeDB", back_populates = "student")
    
class GradeDB(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key = True)
    score = Column(Float)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)

    student = relationship("StudentDB", back_populates = "grades")

class UsersDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String, nullable = False, unique = True)
    hashed_password = Column(String, nullable = True)