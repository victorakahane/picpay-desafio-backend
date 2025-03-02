from app.core.security import generate_password_hash
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.exceptions import UserAlreadyExistsException, UserCreationException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_by_id(user_id)

    def get_user_by_document(self, document: str) -> User:
        return self.user_repository.get_by_document(document)
    
    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_by_email(email)

    def create_user(self, user_data: UserCreate) -> User:
        # Lógica de negócios (validação, verificação, etc.)
        if self.get_user_by_document(user_data.document):
            raise UserAlreadyExistsException("User already exists with this document.")
        if self.get_user_by_email(user_data.email):
            raise UserAlreadyExistsException('User already exists with this e-mail.')

        try:
            user_data.password = generate_password_hash(user_data.password)
            return self.user_repository.create_user(user_data)
        except IntegrityError:
            raise UserAlreadyExistsException("A database integrity error occurred.") from e
        except SQLAlchemyError as e:
            raise UserCreationException("An error occurred while creating the user.") from e


    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found.")

        return self.user_repository.update_user(user, user_data)
