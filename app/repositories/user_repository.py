from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from .base_repository import BaseRepository
from typing import Optional

class UserRepository(BaseRepository):
    def create_user(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.add(user)
        self.commit()
        self.refresh(user)
        return user
    
    def update_user(self, user: User, user_data: UserUpdate) -> User:
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) ->Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_document(self, document: str) -> Optional[User]:
        return self.db.query(User).filter(User.document == document).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
