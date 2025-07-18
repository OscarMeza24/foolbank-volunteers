from typing import List

import strawberry
import asyncio
from app.graphql.definitions import Usuarios, Voluntarios, Eventos, Asignaciones, Feedback, UsuariosInput,\
    UsuariosDelete, VoluntariosInput, VoluntariosDelete, EventosInput, EventosDelete, AsignacionesInput,\
    AsignacionesDelete, FeedbackInput, FeedbackDelete

from strawberry.fastapi import GraphQLRouter
from app.routers.routers import get_usuarios, get_voluntarios, get_eventos, get_asignaciones, get_feedback,\
    insert_usuario, update_usuario, delete_usuario, insert_voluntario, update_voluntario, delete_voluntario


async def sleep_for_2_seconds(name: str, time: int) -> str:
    await asyncio.sleep(time)
    print(f"{name} has finished sleeping")
    return f"{name} has finished sleeping"

@strawberry.type
class Query:
    @strawberry.field
    async def get_usuarios(self) -> List[Usuarios]:
        return await get_usuarios()

    @strawberry.field
    async def get_voluntarios(self) -> List[Voluntarios]:
        return await get_voluntarios()

    @strawberry.field
    async def get_eventos(self) -> List[Eventos]:
        return await get_eventos()

    @strawberry.field
    async def get_asignaciones(self) -> List[Asignaciones]:
        return await get_asignaciones()

    @strawberry.field
    async def get_feedback(self) -> List[Feedback]:
        return await get_feedback()

    @strawberry.field
    async def test_sleep_1(self) -> str:
        print("Starting sleep 1")
        return await sleep_for_2_seconds("Function 1", 2)

    @strawberry.field
    async def test_sleep_2(self) -> str:
        print("Starting sleep 2")
        return await sleep_for_2_seconds("Function 2", 4)

    @strawberry.field
    async def test_sleep_3(self) -> str:
        print("Starting sleep 3")
        return await sleep_for_2_seconds("Function 3", 6)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_usuario(self, usuario: UsuariosInput) -> Usuarios:
        return await insert_usuario(usuario)

    @strawberry.mutation
    async def update_usuario(self, usuario: UsuariosInput) -> Usuarios:
        return await update_usuario(usuario)

    @strawberry.mutation
    async def delete_usuario(self, usuario: UsuariosDelete) -> bool:
        return await delete_usuario(usuario_id=usuario.usuario_id)

    @strawberry.mutation
    async def create_voluntario(self, voluntario: VoluntariosInput) -> Voluntarios:
        return await insert_voluntario(voluntario)

    @strawberry.mutation
    async def update_voluntario(self, voluntario: VoluntariosInput) -> Voluntarios:
        return await update_voluntario(voluntario)

    @strawberry.mutation
    async def delete_voluntario(self, voluntario: VoluntariosDelete) -> bool:
        return await delete_voluntario(voluntario_id=voluntario.voluntario_id)

    @strawberry.mutation
    async def create_evento(self, evento: EventosInput) -> Eventos:
        return await insert_evento(evento)

    @strawberry.mutation
    async def update_evento(self, evento: EventosInput) -> Eventos:
        return await update_evento(evento)

    @strawberry.mutation
    async def delete_evento(self, evento: EventosDelete) -> bool:
        return await delete_evento(evento_id=evento.evento_id)

    @strawberry.mutation
    async def create_asignacion(self, asignacion: AsignacionesInput) -> Asignaciones:
        return await insert_asignacion(asignacion)

    @strawberry.mutation
    async def update_asignacion(self, asignacion: AsignacionesInput) -> Asignaciones:
        return await update_asignacion(asignacion)

    @strawberry.mutation
    async def delete_asignacion(self, asignacion: AsignacionesDelete) -> bool:
        return await delete_asignacion(asignacion_id=asignacion.asignacion_id)

    @strawberry.mutation
    async def create_feedback(self, feedback: FeedbackInput) -> Feedback:
        return await insert_feedback(feedback)

    @strawberry.mutation
    async def update_feedback(self, feedback: FeedbackInput) -> Feedback:
        return await update_feedback(feedback)

    @strawberry.mutation
    async def delete_feedback(self, feedback: FeedbackDelete) -> bool:
        return await delete_feedback(feedback_id=feedback.feedback_id)

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)
