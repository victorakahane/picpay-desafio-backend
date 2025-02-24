from app.core.security import generate_password_hash
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session
from app.models.user import User

class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_by_id(user_id)

    def get_user_by_document(self, document: str) -> User:
        return self.user_repository.get_by_document(document)
    
    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_by_email(email)

    def create_user(self, user_data: UserCreate) -> User:
        # Lógica de negócios (validação, verificação, etc.)
        if self.get_user_by_document(user_data.document):
            raise ValueError("User already exists with this document.")
        if self.get_user_by_email(user_data.email):
            raise ValueError('User already exists with this e-mail.')

        user_data.password = generate_password_hash(user_data.password)
        
        return self.user_repository.create_user(user_data)

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found.")

        return self.user_repository.update_user(user, user_data)
