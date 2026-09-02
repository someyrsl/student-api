from fastapi import HTTPException, APIRouter
from models import Student, StudentDB, GradeDB, Grade
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
           new_student = StudentDB(id = student_id, name = student.name, age = student.age)
           session.add(new_student)
           session.commit()
           result = {"status": "added", "id": new_student.id, "name": new_student.name, "age": new_student.age}
           session.close()
           return result
            

@router.get("/students/{student_id}/grades")
def get_grades(student_id: int):
    session = get_connection()
    student = session.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not student:
        session.close()
        raise HTTPException(status_code=404, detail="Студент не найден")
    grades = [{"subject": g.subject, "score": g.score} for g in student.grades]
    session.close()
    return {"student": student.name, "grades": grades}

@router.put("/students/{student_id}/grades/{grade_id}")
def update_grade(student_id: int, grade_id: int, new_score: float):
    session = get_connection()
    found = session.query(GradeDB).filter(GradeDB.id == grade_id, GradeDB.student_id == student_id).first()
    if not found:
          session.close()
          raise HTTPException(status_code = 404, detail = "Студент не найден")
    else:
          found.score = new_score
          session.commit()
          session.close()
          return {"status": "updated", "student_id": student_id, "grade": new_score}

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

@router.post("/students/{student_id}/grades")
def add_grade(student_id: int, grade: Grade):
      session = get_connection()
      found = session.query(StudentDB).filter(StudentDB.id == student_id).first()
      if not found:
            session.close()
            raise HTTPException(status_code = 404, detail = "Студент не найден")
      else:
            new_grade = GradeDB(student_id = student_id, subject = grade.subject, score = grade.score)
            session.add(new_grade)
            session.commit()
            result = {"status": "added", "id": new_grade.id, "subject": new_grade.subject, "score": new_grade.score}
            session.close()
            return result

@router.get("/students/{student_id}")
def get_student(student_id: int):
     session = get_connection()
     student = session.query(StudentDB).filter(StudentDB.id == student_id).first()
     if not student:
          session.close()
          raise HTTPException(status_code = 404, detail = "Студент не найден")
     else:
          result = {"id": student.id, "name": student.name, "age": student.age, "grades": [{"subject": g.subject, "score": g.score} for g in student.grades]}
          session.close()
          return result