import pytest
import re
from pydantic import ValidationError
from validate_docbr import CPF, CNPJ
from app.schemas.user import UserCreate, UserBase, UserResponse, UserType

def test_valid_cpf():
    cpf = CPF().generate(True)

    user = UserCreate(
        full_name = 'John Doe',
        document = cpf,
        email = 'john.doe@email.com',
        password = '123456',
        user_type = UserType.COMMON
    )
    
    assert user.document == re.sub(r"\D", "", cpf)
    assert CPF().validate(user.document) is True

def test_invalid_cpf():
    cpf = '111.111.111-11'

    with pytest.raises(ValueError, match='Invalid CPF') as exc:
        user = UserCreate(
            full_name = 'John Doe',
            document = cpf,
            email = 'john.doe@email.com',
            password = '123456',
            user_type = UserType.COMMON
        )

def test_valid_cnpj():
    cnpj = CNPJ().generate(True)

    user = UserCreate(
        full_name = 'John Doe',
        document = cnpj,
        email = 'john.doe@email.com',
        password = '123456',
        user_type = UserType.MERCHANT
    )
    
    assert user.document == re.sub(r"\D", "", cnpj)
    assert CNPJ().validate(user.document) is True

def test_invalid_cnpj():
    cnpj = '00.001.111/2221-43'

    with pytest.raises(ValueError, match='Invalid CNPJ') as exc:
        user = UserCreate(
            full_name = 'John Doe',
            document = cnpj,
            email = 'john.doe@email.com',
            password = '123456',
            user_type = UserType.MERCHANT
        )

def test_common_user_with_cnpj():
    cnpj = CNPJ().generate(True)

    with pytest.raises(ValueError, match='Invalid CPF') as exc:
        UserCreate(
            full_name='John Doe',
            document=cnpj,
            email='john.doe@email.com',
            password='123456',
            user_type=UserType.COMMON
        )

def test_merchant_user_with_cpf():
    cpf = CPF().generate(True)

    with pytest.raises(ValueError, match='Invalid CNPJ') as exc:
        UserCreate(
            full_name='John Doe',
            document=cpf,
            email='john.doe@email.com',
            password='123456',
            user_type=UserType.MERCHANT
        )

def test_user_response():
    cpf = CPF().generate()
    
    user_response = UserResponse(
        id=1,
        full_name='John Doe',
        document=cpf,
        email='john.doe@email.com',
        user_type=UserType.COMMON
    )

    assert user_response.id == 1
    assert user_response.full_name == 'John Doe'
    assert user_response.document == cpf
    assert user_response.email == 'john.doe@email.com'
    assert user_response.user_type == UserType.COMMON

def test_invalid_user_type():
    with pytest.raises(ValueError, match="Input should be 'common' or 'merchant'") as exc:
        UserCreate(
            full_name='John Doe',
            document='12345678909',
            email='john.doe@email.com',
            password='123456',
            user_type='INVALID_TYPE'
        )
