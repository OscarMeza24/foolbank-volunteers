from __future__ import annotations

from typing import Optional

from strawberry import type as strawberry_type, input as strawberry_input

@strawberry_type
class Usuarios:
    usuarios_id: int
    nombre: Optional[str]
    apellido: Optional[str]
    correo: Optional[str]
    telefono: Optional[int]
    tipo: Optional[str]
    voluntarios: Optional["Voluntarios"] = None


@strawberry_input
class UsuariosInput:
    usuarios_id: int
    nombre: Optional[str]
    apellido: Optional[str]
    correo: Optional[str]
    telefono: Optional[int]
    tipo: Optional[str]


@strawberry_input
class UsuariosDelete:
    usuarios_id: int


@strawberry_type
class Voluntarios:
    voluntarios_id: int
    habilidades: Optional[str]
    disponibilidad: Optional[str]
    usuario_id: Optional[int]
    usuario: Optional["Usuarios"]


@strawberry_input
class VoluntariosInput:
    voluntarios_id: int
    habilidades: Optional[str]
    disponibilidad: Optional[str]
    usuario_id: Optional[int]

@strawberry_input
class VoluntariosDelete:
    voluntarios_id: int


@strawberry_type
class Eventos:
    eventos_id: int
    nombre: Optional[str]
    fecha: Optional[str]
    hora: Optional[str]
    ubicacion: Optional[str]
    voluntarios_necesarios: Optional[int]
    descripcion_eventos: Optional[str]


@strawberry_input
class EventosInput:
    eventos_id: int
    nombre: Optional[str] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    ubicacion: Optional[str] = None
    voluntarios_necesarios: Optional[int] = None
    descripcion_eventos: Optional[str] = None


@strawberry_input
class EventosDelete:
    eventos_id: int


@strawberry_type
class Asignaciones:
    asignaciones_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    estado: Optional[str]

@strawberry_input
class AsignacionesInput:
    asignaciones_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    estado: Optional[str]
    voluntario_id: Optional[int]

@strawberry_input
class AsignacionesDelete:
    asignaciones_id: int


@strawberry_type
class Feedback:
    feedback_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    calificacion: Optional[int]
    comentario: Optional[str]
    usuario: Optional["Usuarios"] = None
    voluntario: Optional["Voluntarios"] = None
    evento: Optional["Eventos"] = None

@strawberry_input
class FeedbackInput:
    feedback_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    calificacion: Optional[int]
    comentario: Optional[str]

@strawberry_input
class FeedbackDelete:
    feedback_id: int
