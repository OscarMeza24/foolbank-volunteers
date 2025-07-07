from typing import Optional

import strawberry


@strawberry.type
class Usuarios:
    Usuarios_id: int
    nombre: Optional[str]
    apellido: Optional[str]
    correo: Optional[str]
    telefono: Optional[int]
    tipo: Optional[str]
    voluntarios: Optional["Voluntarios"]


@strawberry.input
class UsuariosInput:
    Usuarios_id: int
    nombre: Optional[str]
    apellido: Optional[str]
    correo: Optional[str]
    telefono: Optional[int]
    tipo: Optional[str]


@strawberry.input
class UsuariosDelete:
    Usuarios_id: int


@strawberry.type
class Voluntarios:
    voluntarios_id: int
    habilidades: Optional[str]
    disponibilidad: Optional[str]
    usuario_id: Optional[int]
    usuario: Optional["Usuarios"]


@strawberry.type
class Eventos:
    eventos_id: int
    nombre: Optional[str]
    fecha: Optional[str]
    hora: Optional[str]
    lugar: Optional[str]
    tipo: Optional[str]
    estado: Optional[str]


@strawberry.input
class EventosInput:
    eventos_id: int
    nombre: Optional[str]
    fecha: Optional[str]
    hora: Optional[str]
    lugar: Optional[str]
    tipo: Optional[str]
    estado: Optional[str]


@strawberry.input
class EventosDelete:
    eventos_id: int


@strawberry.type
class Asignaciones:
    asignaciones_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    estado: Optional[str]


@strawberry.type
class Asignaciones:
    asignaciones_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    estado: Optional[str]


@strawberry.type
class Eventos:
    eventos_id: int
    nombre: Optional[str]
    fecha: Optional[str]
    hora: Optional[str]
    lugar: Optional[str]
    tipo: Optional[str]
    estado: Optional[str]


@strawberry.type
class Feedback:
    feedback_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    calificacion: Optional[int]
    comentario: Optional[str]


@strawberry.type
class Feedback:
    feedback_id: int
    voluntario_id: Optional[int]
    evento_id: Optional[int]
    calificacion: Optional[int]
    comentario: Optional[str]

