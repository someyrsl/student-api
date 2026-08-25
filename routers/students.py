from fastapi import HTTPException, APIRouter
from models import Student, StudentDB
from database import get_connection

router = APIRouter()

@router.post("/students/{student_id}")
def add_student(student_id: int, student: Student):
    session = get_connection()
    existing = session.query(StudentDB).filter(StudentDB.id == student_id).first()
    if existing:
           session.close()
           raise HTTPException(status_code = 409, detail = "Студент с таким id уже существует")
    else:
           new_student = StudentDB(id = student_id, name = student.name, age = student.age, grade = student.grade)
           session.add(new_student)
           session.commit()
           result = {"status": "added", "id": new_student.id, "name": new_student.name, "age": new_student.age, "grade": new_student.grade}
           session.close()
           return result

@router.get("/students/{student_name}")
def get_student(student_name: str):
    session = get_connection()
    found = session.query(StudentDB).filter(StudentDB.name == student_name).first()
    session.close()
    if not found:
           raise HTTPException(status_code = 404, detail = "Студент не найден")
    return {"status": "Студент найден", "student": found.name, "age": found.age, "grade": found.grade}

@router.put("/students")
def update_student(student_name: str, student_grade: float):
    session = get_connection()
    found = session.query(StudentDB).filter(StudentDB.name == student_name).first()
    if not found:
          session.close()
          raise HTTPException(status_code = 404, detail = "Студент не найден")
    else:
          found.grade = student_grade
          session.commit()
          session.close()
          return {"status": "updated", "student": student_name, "grade": student_grade}

@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    session = get_connection()
    found = session.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not found:
          session.close()
          raise HTTPException(status_code = 404, detail = "Студент для удаления не найден")
    else:
          session.delete(found)
          session.commit()
          session.close()
          return {"status": "Студент удален"}
