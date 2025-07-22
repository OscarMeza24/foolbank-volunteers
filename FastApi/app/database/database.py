from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Configuración de la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

# Creación de la engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Creación de la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creación de la base de datos
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Función de dependencia que proporciona una sesión de base de datos.
    Se asegura de que la sesión se cierre correctamente después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
