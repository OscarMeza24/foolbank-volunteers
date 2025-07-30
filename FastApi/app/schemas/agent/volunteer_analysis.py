from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class VolunteerAnalysisBase(BaseModel):
    voluntario_id: int = Field(..., description="ID del voluntario a analizar")
    parametros: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Parámetros adicionales para el análisis"
    )

class VolunteerAnalysisCreate(VolunteerAnalysisBase):
    pass

class VolunteerAnalysisUpdate(BaseModel):
    estado: AnalysisStatus
    resultado: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class VolunteerAnalysisInDB(VolunteerAnalysisBase):
    id: int
    estado: AnalysisStatus
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    resultado: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True

class AnalysisResult(BaseModel):
    voluntario_id: int
    resumen: str
    fortalezas: List[str]
    areas_mejora: List[str]
    recomendaciones: List[str]
    eventos_participados: int
    calificacion_promedio: Optional[float] = None
    ultima_participacion: Optional[str] = None
    habilidades_destacadas: List[str] = []
    compatibilidad_eventos_futuros: Dict[str, float] = {}

class AnalysisRequest(BaseModel):
    voluntario_id: int
    incluir_historico: bool = True
    incluir_recomendaciones: bool = True
    idioma: str = "es"
