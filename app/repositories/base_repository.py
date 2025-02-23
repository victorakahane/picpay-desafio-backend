from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, instance):
        self.db.add(instance)

    def commit(self):
        self.db.commit()

    def refresh(self, instance):
        self.db.refresh(instance)