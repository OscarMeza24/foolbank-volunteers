from dataclasses import dataclass
from typing import Optional, List


@dataclass
class UsuariosModel:
    usuarios_id: int
    nombre: Optional[str]
    apellido: Optional[str]
    correo: Optional[str]
    telefono: Optional[int]
    tipo: Optional[str]


@dataclass
class VoluntariosModel:
    voluntarios_id: int
    habilidades: Optional[str]
    disponibilidad: Optional[str]
    usuario_id: Optional[int]
    usuario: Optional[UsuariosModel] = None


@dataclass
class EventosModel:
    eventos_id: int
    nombre: Optional[str]
    fecha: Optional[str]
    hora: Optional[str]
    lugar: Optional[str]
    tipo: Optional[str]
    estado: Optional[str]


@dataclass
class AsignacionesModel:
    asignaciones_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    estado: Optional[str]


@dataclass
class FeedbackModel:
    feedback_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    calificacion: Optional[int]
    comentario: Optional[str]



