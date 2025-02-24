import pytest
from validate_docbr import CPF, CNPJ
from unittest.mock import MagicMock
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserType
from app.models.user import User
from unittest.mock import MagicMock, patch
from app.schemas.user import UserCreate, UserType

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_user_service(mock_db):
    mock_user_service = UserService(mock_db)
    mock_user_service.user_repository = MagicMock()
    return mock_user_service

def test_create_user_success(mock_user_service):
    user_data = UserCreate(
        full_name="New User",
        document=CPF().generate(),
        email="new@email.com",
        password="12345",
        user_type=UserType.COMMON
    )

    mock_user_service.user_repository.get_by_document.return_value = None
    mock_user_service.user_repository.get_by_email.return_value = None
    mock_user_service.user_repository.create_user.side_effect = lambda user_data: User(**user_data.model_dump())

    with patch('app.services.user_service.generate_password_hash', return_value="hashed_password"):
        user = mock_user_service.create_user(user_data)

    assert user.email == user_data.email
    assert user.full_name == user_data.full_name
    assert user.password == "hashed_password"

def test_create_user_existing_document(mock_user_service):
    user_data = UserCreate(
        full_name="New User",
        document=CPF().generate(),
        email="new@email.com",
        password="12345",
        user_type=UserType.COMMON
    )

    mock_user_service.user_repository.get_by_document.return_value = User(**user_data.model_dump())

    with pytest.raises(ValueError, match="User already exists with this document."):
        mock_user_service.create_user(user_data)

def test_create_user_existing_email(mock_user_service):
    user_data = UserCreate(
        full_name="New User",
        document=CPF().generate(),
        email="new@email.com",
        password="12345",
        user_type=UserType.COMMON
    )

    mock_user_service.user_repository.get_by_document.return_value = None
    mock_user_service.user_repository.get_by_email.return_value = User(**user_data.model_dump())

    with pytest.raises(ValueError, match="User already exists with this e-mail."):
        mock_user_service.create_user(user_data)
