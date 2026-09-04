from fastapi import FastAPI
from routers import students, users
from database import init_db

app = FastAPI()

init_db()  

app.include_router(students.router)
app.include_router(users.router)