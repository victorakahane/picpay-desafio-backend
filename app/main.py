from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.database import get_db, Base, engine, create_tables
from app.services.user_service import UserService
from contextlib import asynccontextmanager

app = FastAPI()

create_tables()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao PicPay Simplificado!"}

@app.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    try:
        return user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
