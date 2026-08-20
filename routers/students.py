from fastapi import HTTPException, APIRouter
from models import Student
from database import get_connection

router = APIRouter()
conn = get_connection()
cursor = conn.cursor()
@router.post("/students/{student_id}")
def add_student(student_id: int, student: Student):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students where id = ?", (student_id,))
        existing = cursor.fetchone()
        if existing:
            conn.close()
            raise HTTPException(status_code = 409, detail = "Студент с таким id уже существует")
        cursor.execute("INSERT INTO students (id, name, age, grade) VALUES (?, ?, ?, ?)",(student_id, student.name, student.age, student.grade))
        conn.commit()
        conn.close()
        return {"status": "added", "student": student}

@router.get("/students/{student_name}")
def get_student(student_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name = ?", (student_name,))
    found = cursor.fetchone()
    if not found:
       conn.close()
       raise HTTPException(status_code = 404, detail = "Студент не найден")
    conn.close()
    return {"status": "Студент найден", "student": found}

@router.put("/students")
def update_student(student_name: str, student_grade: float):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET grade = ? WHERE name = ?", (student_grade, student_name))
        if cursor.rowcount == 0:
               conn.close()
               raise HTTPException(status_code = 404, detail = "Студент не найден")
        conn.commit()
        conn.close()
        return {"status": "updated", "student": student_name, "grade": student_grade}

@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    if cursor.rowcount == 0:
                   conn.close()
                   raise HTTPException(status_code = 404, detail = "Студент для удаления не найден")
    conn.commit()
    conn.close()
    return {"status": "deleted"}
