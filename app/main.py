from fastapi import FastAPI
from app.database import create_tables
from app.routes.user_routes import router as user_router

app = FastAPI()

create_tables()

app.include_router(user_router, prefix='/users')

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao PicPay Simplificado!"}
