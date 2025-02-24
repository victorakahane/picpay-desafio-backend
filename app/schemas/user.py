from app.models.user import UserType
from pydantic import BaseModel, EmailStr, model_validator, field_validator
from typing import Optional
from validate_docbr import CPF, CNPJ
import re

class UserBase(BaseModel):
    full_name: str
    document: str
    email: EmailStr
    password: str
    user_type: UserType

    @model_validator(mode='after')
    def validate_document(cls, values):
        user_type = values.user_type
        document = values.document
        
        # Removendo caracteres não numéricos do documento
        values.document = re.sub(r"\D", "", document)
        document = values.document
        
        # Verifica se o tipo de usuário é 'common' e valida o CPF
        if user_type == UserType.COMMON:
            if CPF().validate(document):
                return values 
            raise ValueError('Invalid CPF. Provide a valid one.')

        # Verifica se o tipo de usuário é 'merchant' e valida o CNPJ
        elif user_type == UserType.MERCHANT:
            if CNPJ().validate(document):
                return values
            raise ValueError('Invalid CNPJ. Provide a valid one.')

        # Se a validação falhar, lança um erro
        raise ValueError('Invalid document. Provide a valid CPF or CNPJ.')
    
    class Config:
        use_enum_values = True

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    full_name: Optional[str] = None
    document: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    user_type: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    document: str
    email: EmailStr
    user_type: UserType
    
    class Config:
        from_attributes = True
