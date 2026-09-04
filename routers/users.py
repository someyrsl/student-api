from fastapi import APIRouter, HTTPException
from models import Users, UsersDB
from database import get_connection
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
def register(user: Users):
    session = get_connection()
    found = session.query(UsersDB).filter(UsersDB.username == user.username).first()
    if found:
        session.close()
        raise HTTPException(status_code = 409, detail = "Такой логин уже занят")
    hashed = hash_password(user.password)
    new_user = UsersDB(username = user.username, hashed_password = hashed)
    session.add(new_user)
    session.commit()
    session.close()
    return {"status": "added"}

@router.post("/login")
def login(user: Users):
    session = get_connection()
    found = session.query(UsersDB).filter(UsersDB.username == user.username).first()
    if not found:
        session.close()
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    is_password = verify_password(user.password, found.hashed_password)
    if not is_password:
        session.close()
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    session.close()
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}