from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime
import enum

class AnalysisStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class VolunteerAnalysis(Base):
    """
    Modelo para almacenar los análisis de voluntarios realizados por el agente autónomo.
    """
    __tablename__ = "volunteer_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    voluntario_id = Column(Integer, ForeignKey("Voluntarios.voluntarios_id"), nullable=False)
    estado = Column(SQLAlchemyEnum(AnalysisStatus), nullable=False, default=AnalysisStatus.PENDING)
    parametros = Column(JSON, nullable=False, default={})
    resultado = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=func.now(), nullable=True)
    
    # Relación con el modelo Voluntarios
    voluntario = relationship("Voluntarios", back_populates="analisis")

# Añadir la relación al modelo Voluntarios existente
def add_relationship_to_volunteers():
    """
    Función para añadir la relación al modelo Voluntarios existente.
    Esto debería llamarse después de que se hayan definido ambos modelos.
    """
    from app.models.models import Voluntarios
    
    if not hasattr(Voluntarios, 'analisis'):
        Voluntarios.analisis = relationship(
            "VolunteerAnalysis", 
            back_populates="voluntario",
            cascade="all, delete-orphan"
        )
