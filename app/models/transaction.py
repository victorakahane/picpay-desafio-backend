from enum import Enum
from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Quem pagou
    payee_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Quem recebeu
    amount = Column(Numeric(scale=2), nullable=False)  # Valor da transação
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)
    created_at = Column(DateTime, default=func.now())  # Timestamp automático

    payer = relationship("User", foreign_keys=[payer_id])  # Relacionamento com quem pagou
    payee = relationship("User", foreign_keys=[payee_id])  # Relacionamento com quem recebeu
