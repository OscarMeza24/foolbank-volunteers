import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base, get_db
from main import app

# Configuración de la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos de prueba
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Sobrescribe la dependencia get_db para usar la base de datos de prueba"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Sobrescribir la dependencia get_db en la aplicación
app.dependency_overrides[get_db] = override_get_db

# Fixture para el cliente de prueba
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Fixture para la sesión de base de datos
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# Fixture para datos de prueba
@pytest.fixture
def usuario_data():
    return {
        "usuarios_id": 1,
        "nombre": "Juan",
        "apellido": "Pérez",
        "correo": "juan@example.com",
        "telefono": "1234567890",
        "tipo": "voluntario",
        "hashed_password": "hashedpassword123",
        "is_active": True,
        "is_verified": True
    }

@pytest.fixture
def voluntario_data():
    return {
        "voluntarios_id": 1,
        "habilidades": "Cocina, Logística",
        "disponibilidad": "Fines de semana",
        "usuario_id": 1
    }

@pytest.fixture
def evento_data():
    return {
        "eventos_id": 1,
        "nombre": "Banco de Alimentos 2023",
        "fecha": "2023-12-15",
        "hora": "10:00",
        "ubicacion": "Plaza Central",
        "voluntarios_necesarios": 10
    }

@pytest.fixture
def asignacion_data():
    return {
        "asignaciones_id": 1,
        "evento_id": 1,
        "voluntario_id": 1,
        "rol": "Ayudante",
        "estado": "Pendiente",
        "fecha_asignacion": "2023-11-20"
    }

@pytest.fixture
def feedback_data():
    return {
        "feedback_id": 1,
        "evento_id": 1,
        "voluntario_id": 1,
        "calificacion": 5,
        "comentario": "Excelente experiencia"
    }
