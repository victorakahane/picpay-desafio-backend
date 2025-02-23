from sqlalchemy import Column, Integer, String, Float, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from .transaction import Transaction
from enum import Enum

class UserType(str, Enum):
    COMMON = 'common'
    MERCHANT = 'merchant'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    document = Column(String(14), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    balance = Column(Numeric(scale=2), default=0.0)
    user_type = Column(SQLEnum(UserType), nullable=False)
    transactions_as_payer = relationship("Transaction", foreign_keys=[Transaction.payer_id], back_populates="payer")
    transactions_as_payee = relationship("Transaction", foreign_keys=[Transaction.payee_id], back_populates="payee")
