from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a engine de conexão
engine = create_engine(DATABASE_URL)

# Configura a sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Criar todas as tabelas
def create_tables():
    try:
        print("Tentando criar as tabelas...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")


# Dependência para obter a sessão
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
