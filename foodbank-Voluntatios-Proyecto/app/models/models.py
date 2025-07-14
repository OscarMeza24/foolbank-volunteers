from typing import List

from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base


class Usuarios(Base):
    __tablename__ = "Usuarios"

    Usuarios_id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    correo = Column(String)
    telefono = Column(Integer)
    tipo = Column(String)
    voluntarios = relationship("Voluntarios", back_populates="usuario")

class Voluntarios(Base):
    __tablename__ = "Voluntarios"
    voluntarios_id = Column(Integer, primary_key=True)
    habilidades = Column(String)
    disponibilidad = Column(String)
    usuario_id = Column(Integer, ForeignKey("Usuarios.Usuarios_id"))
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
