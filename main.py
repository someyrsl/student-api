from fastapi import FastAPI
from routers import students   
from database import init_db

app = FastAPI()

init_db()  

app.include_router(students.router)