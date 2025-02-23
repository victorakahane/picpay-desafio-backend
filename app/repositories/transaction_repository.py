from .base_repository import BaseRepository
from app.models.transaction import Transaction

class TransactionRepository(BaseRepository):
    def add(self, transaction: Transaction):
        self.db.add(transaction)
    
    def commit(self, transaction: Transaction):
        self.db.commit()
        self.db.refresh(transaction)