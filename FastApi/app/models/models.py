from typing import List
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.util import u
from app.database.database import Base
from passlib.context import CryptContext

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Usuarios(Base):
    __tablename__ = "Usuarios"

    usuarios_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(20))
    tipo = Column(String(50), nullable=False)  # Ejemplo: 'admin', 'voluntario', 'organizador'
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Relaciones
    voluntarios = relationship("Voluntarios", back_populates="usuario")

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

class Voluntarios(Base):
    __tablename__ = "Voluntarios"
    voluntarios_id = Column(Integer, primary_key=True)
    habilidades = Column(String)
    disponibilidad = Column(String)
    usuario_id = Column(Integer, ForeignKey("Usuarios.usuarios_id"))
    usuario = relationship("Usuarios", back_populates="voluntarios")
    asignaciones = relationship("Asignaciones", back_populates="voluntario")
    feedback = relationship("Feedback", back_populates="voluntario")

class Eventos(Base):
    __tablename__ = "Eventos"
    eventos_id = Column(Integer, primary_key=True)
    nombre = Column(String)
    fecha = Column(String)
    hora = Column(String)
    ubicacion = Column(String)
    voluntarios_necesarios = Column(Integer)
    descripcion_eventos = Column(Text)
    asignaciones = relationship("Asignaciones", back_populates="evento")
    feedback = relationship("Feedback", back_populates="evento")

class Asignaciones(Base):
    __tablename__ = "Asignaciones"
    asignaciones_id = Column(Integer, primary_key=True)
    evento_id = Column(Integer, ForeignKey("Eventos.eventos_id"))
    voluntario_id = Column(Integer, ForeignKey("Voluntarios.voluntarios_id"))
    rol = Column(String)
    estado = Column(String)
    fecha_asignacion = Column(String)
    evento = relationship("Eventos", back_populates="asignaciones")
    voluntario = relationship("Voluntarios", back_populates="asignaciones")
    
class Feedback(Base):
    __tablename__ = "feedback"
    feedback_id = Column(Integer, primary_key=True)
    evento_id = Column(Integer, ForeignKey("Eventos.eventos_id"))
    voluntario_id = Column(Integer, ForeignKey("Voluntarios.voluntarios_id"))
    calificacion = Column(Integer)
    comentario = Column(Text)
    evento = relationship("Eventos", back_populates="feedback")
    voluntario = relationship("Voluntarios", back_populates="feedback")
