from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.database import get_db
from app.dependencies import get_user_service

router = APIRouter()

@router.post('/', response_model=UserResponse)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
