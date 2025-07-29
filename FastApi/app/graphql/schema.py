from typing import List
from app.database.database import SessionLocal


import strawberry
import asyncio
from app.graphql.definitions import Usuarios, Voluntarios, Eventos, Asignaciones, Feedback, UsuariosInput,\
    UsuariosDelete, VoluntariosInput, VoluntariosDelete, EventosInput, EventosDelete, AsignacionesInput,\
    AsignacionesDelete, FeedbackInput, FeedbackDelete

from strawberry.fastapi import GraphQLRouter
from app.routers.routers import get_usuarios, get_voluntarios, get_eventos, get_asignaciones, get_feedback,\
    insert_usuario, update_usuario, delete_usuario, insert_voluntario, update_voluntario, delete_voluntario,\
    insert_asignacion, update_asignacion, insert_evento, insert_feedback, update_asignacion, update_evento,\
    update_feedback, update_voluntario, delete_asignacion, delete_evento, delete_feedback

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
        from app.database.database import SessionLocal
        from app.models.models import Voluntarios as VoluntariosModel
        
        db = SessionLocal()
        try:
            voluntarios = db.query(VoluntariosModel).all()
            return [
                Voluntarios(
                    voluntarios_id=v.voluntarios_id,
                    habilidades=v.habilidades,
                    disponibilidad=v.disponibilidad,
                    usuario_id=v.usuario_id,
                    usuario=None  # This would need to be populated if needed
                )
                for v in voluntarios
            ]
        finally:
            db.close()

    @strawberry.field
    async def get_eventos(self) -> List[Eventos]:
        from app.database.database import SessionLocal
        from app.models.models import Eventos as EventosModel
        
        db = SessionLocal()
        try:
            eventos = db.query(EventosModel).all()
            return [Eventos(
                eventos_id=e.eventos_id,
                nombre=e.nombre,
                fecha=e.fecha,
                hora=e.hora,
                ubicacion=e.ubicacion,
                voluntarios_necesarios=e.voluntarios_necesarios,
                descripcion_eventos=e.descripcion_eventos
            ) for e in eventos]
        finally:
            db.close()

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
        from app.websocket.client import websocket_client
        from datetime import datetime
        import logging

        db = SessionLocal()
        logger = logging.getLogger(__name__)
        try:
            nuevo_usuario = await insert_usuario(usuario, db)
            
            # Prepara los datos del evento
            notification_data = {
                "event": "nuevo_usuario",
                "data": {
                    "usuarios_id": nuevo_usuario.usuarios_id,
                    "nombre": nuevo_usuario.nombre,
                    "correo": nuevo_usuario.correo,
                    "telefono": nuevo_usuario.telefono,
                    "tipo": nuevo_usuario.tipo,
                    "fecha_creacion": datetime.now().isoformat()
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Envía el evento por WebSocket
            await websocket_client.send_message(
                room="admin",  # O la sala que prefieras
                event="notificacion",
                data=notification_data
            )
            logger.info(f"Notificación de nuevo usuario enviada: {notification_data}")

            return nuevo_usuario
        finally:
            db.close()

    @strawberry.mutation
    async def update_usuario(self, usuario: UsuariosInput) -> Usuarios:
        from app.websocket.client import websocket_client
        from datetime import datetime
        import logging
        from app.routers.routers import update_usuario as router_update_usuario
        from app.models.schema import UsuariosModel

        db = SessionLocal()
        logger = logging.getLogger(__name__)
        try:
            # Convert the Strawberry input to a Pydantic model
            usuario_dict = {
                'usuarios_id': usuario.usuarios_id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'correo': usuario.correo,
                'telefono': usuario.telefono,
                'tipo': usuario.tipo
            }
            usuario_model = UsuariosModel(**usuario_dict)
            
            # Call the router function with the db session
            usuario_actualizado = await router_update_usuario(usuario_model, db=db)

            # Prepare notification data
            notification_data = {
                "event": "usuario_actualizado",
                "data": {
                    "usuarios_id": usuario_actualizado.usuarios_id,
                    "nombre": usuario_actualizado.nombre,
                    "correo": usuario_actualizado.correo,
                    "telefono": usuario_actualizado.telefono,
                    "tipo": usuario_actualizado.tipo,
                    "fecha_actualizacion": datetime.now().isoformat()
                },
                "timestamp": datetime.now().isoformat()
            }

            # Send WebSocket notification
            await websocket_client.send_message(
                room="admin",
                event="notificacion",
                data=notification_data
            )
            logger.info(f"Notificación de actualización enviada: {notification_data}")

            # Convert the SQLAlchemy model to Strawberry type
            return Usuarios(
                usuarios_id=usuario_actualizado.usuarios_id,
                nombre=usuario_actualizado.nombre,
                apellido=usuario_actualizado.apellido,
                correo=usuario_actualizado.correo,
                telefono=usuario_actualizado.telefono,
                tipo=usuario_actualizado.tipo
            )
        except Exception as e:
            logger.error(f"Error al actualizar usuario: {str(e)}")
            raise
        finally:
            db.close()

    @strawberry.mutation
    async def delete_usuario(self, usuario: UsuariosDelete) -> bool:
        from app.websocket.client import websocket_client
        from datetime import datetime
        import logging
        from app.models.models import Usuarios  # Import the Usuarios model

        db = SessionLocal()
        logger = logging.getLogger(__name__)
        try:
            # Get the user ID from the input object
            usuario_id = usuario.usuarios_id  # Access the field directly as it's defined in UsuariosDelete
            if usuario_id is None:
                raise ValueError("User ID is required")
                
            # Perform the deletion directly in the resolver
            existing_usuario = db.query(Usuarios).filter(Usuarios.usuarios_id == usuario_id).first()
            
            if existing_usuario:
                db.delete(existing_usuario)
                db.commit()
                
                # Send notification
                notification_data = {
                    "event": "usuario_eliminado",
                    "data": {
                        "usuarios_id": usuario_id,
                        "fecha_eliminacion": datetime.now().isoformat()
                    },
                    "timestamp": datetime.now().isoformat()
                }

                await websocket_client.send_message(
                    room="admin",
                    event="notificacion",
                    data=notification_data
                )
                logger.info(f"Notificación de usuario eliminado enviada: {notification_data}")
                return True
                
            return False
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar usuario: {str(e)}")
            raise
        finally:
            db.close()

    @strawberry.mutation
    async def create_voluntario(self, voluntario: VoluntariosInput) -> Voluntarios:
        from app.websocket.client import websocket_client
        from datetime import datetime
        import logging
        from app.database.database import SessionLocal
        from app.models.models import Voluntarios as VoluntariosModel
        from app.models.schema import VoluntariosModel as VoluntariosSchema

        db = SessionLocal()
        logger = logging.getLogger(__name__)
        
        try:
            # Convert Strawberry input to Pydantic model
            voluntario_dict = {
                'voluntarios_id': voluntario.voluntarios_id,
                'habilidades': voluntario.habilidades,
                'disponibilidad': voluntario.disponibilidad,
                'usuario_id': voluntario.usuario_id
            }
            voluntario_model = VoluntariosSchema(**voluntario_dict)

            # Create the new volunteer directly
            new_voluntario = VoluntariosModel(
                voluntarios_id=voluntario.voluntarios_id,
                habilidades=voluntario.habilidades,
                disponibilidad=voluntario.disponibilidad,
                usuario_id=voluntario.usuario_id
            )
            
            db.add(new_voluntario)
            db.commit()
            db.refresh(new_voluntario)
            
            # Prepare and send notification
            notification_data = {
                "event": "nuevo_voluntario",
                "data": {
                    "id": str(new_voluntario.voluntarios_id),
                    "habilidades": str(new_voluntario.habilidades or ""),
                    "disponibilidad": str(new_voluntario.disponibilidad or ""),
                    "usuario_id": new_voluntario.usuario_id,
                    "fecha_creacion": datetime.now().isoformat()
                },
                "timestamp": datetime.now().isoformat()
            }

            await websocket_client.send_message(
                room="admin",
                event="notificacion",
                data=notification_data
            )
            logger.info(f"Notificación de nuevo voluntario enviada: {notification_data}")

            # Convert to Strawberry type
            return Voluntarios(
                voluntarios_id=new_voluntario.voluntarios_id,
                habilidades=new_voluntario.habilidades,
                disponibilidad=new_voluntario.disponibilidad,
                usuario_id=new_voluntario.usuario_id,
                usuario=None  # This would need to be populated if needed
            )
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error al crear voluntario: {str(e)}")
            raise
        finally:
            db.close()

    @strawberry.mutation
    async def update_voluntario(self, voluntario: VoluntariosInput) -> Voluntarios:
        from app.websocket.client import websocket_client
        from datetime import datetime
        import logging
        from app.models.models import Voluntarios
        from sqlalchemy.orm import Session
        from app.database.database import SessionLocal

        db = SessionLocal()
        logger = logging.getLogger(__name__)
        try:
            # Get the existing voluntario
            existing_voluntario = db.query(Voluntarios).filter(
                Voluntarios.voluntarios_id == voluntario.voluntarios_id
            ).first()

            if not existing_voluntario:
                raise Exception("Voluntario no encontrado")

            # Update the fields
            for field, value in vars(voluntario).items():
                if value is not None and hasattr(existing_voluntario, field):
                    setattr(existing_voluntario, field, value)

            db.commit()
            db.refresh(existing_voluntario)

            # Prepare and send notification
            notification_data = {
                "event": "voluntario_actualizado",
                "data": {
                    "id": str(existing_voluntario.voluntarios_id),
                    "habilidades": str(existing_voluntario.habilidades or ""),
                    "disponibilidad": str(existing_voluntario.disponibilidad or ""),
                    "usuario_id": existing_voluntario.usuario_id,
                    "fecha_actualizacion": datetime.now().isoformat()
                },
                "timestamp": datetime.now().isoformat()
            }

            await websocket_client.send_message(
                room="admin",
                event="notificacion",
                data=notification_data
            )
            logger.info(f"Notificación de voluntario actualizado enviada: {notification_data}")

            # Convert to Strawberry type
            return Voluntarios(
                voluntarios_id=existing_voluntario.voluntarios_id,
                habilidades=existing_voluntario.habilidades,
                disponibilidad=existing_voluntario.disponibilidad,
                usuario_id=existing_voluntario.usuario_id,
                usuario=None  # This would need to be populated if needed
            )
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar voluntario: {str(e)}")
            raise
        finally:
            db.close()

    @strawberry.mutation
    async def delete_voluntario(self, voluntario: VoluntariosDelete) -> bool:
        from app.websocket.client import websocket_client
        from datetime import datetime
        import logging
        from app.models.models import Voluntarios
        from app.database.database import SessionLocal

        db = SessionLocal()
        logger = logging.getLogger(__name__)
        try:
            # Get the voluntario ID from the input
            voluntario_id = voluntario.voluntarios_id
            
            # Perform the deletion directly
            existing_voluntario = db.query(Voluntarios).filter(
                Voluntarios.voluntarios_id == voluntario_id
            ).first()

            if existing_voluntario:
                db.delete(existing_voluntario)
                db.commit()

                # Send notification
                notification_data = {
                    "event": "voluntario_eliminado",
                    "data": {
                        "voluntario_id": voluntario_id,
                        "fecha_eliminacion": datetime.now().isoformat()
                    },
                    "timestamp": datetime.now().isoformat()
                }

                await websocket_client.send_message(
                    room="admin",
                    event="notificacion",
                    data=notification_data
                )
                logger.info(f"Notificación de voluntario eliminado enviada: {notification_data}")
                return True
                
            return False
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar voluntario: {str(e)}")
            raise
        finally:
            db.close()

    @strawberry.mutation
    async def create_evento(self, evento: EventosInput) -> Eventos:
        from app.websocket.client import websocket_client
        from datetime import datetime
        import logging

        db = SessionLocal()
        logger = logging.getLogger(__name__)
        try:
            nuevo_evento = await insert_evento(evento, db=db)
            
            # Prepara los datos de la notificación
            notification_data = {
                "event": "nuevo_evento",
                "data": {
                    "eventos_id": nuevo_evento.eventos_id,
                    "nombre": nuevo_evento.nombre,
                    "fecha": str(nuevo_evento.fecha),
                    "hora": str(nuevo_evento.hora),
                    "ubicacion": nuevo_evento.ubicacion,
                    "fecha_creacion": datetime.now().isoformat()
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Envía la notificación por WebSocket
            await websocket_client.send_message(
                room="admin",  # O la sala que prefieras
                event="notificacion",
                data=notification_data
            )
            logger.info(f"Notificación de nuevo evento enviada: {notification_data}")

            return nuevo_evento
        except Exception as e:
            logger.error(f"Error al crear evento: {str(e)}")
            raise
        finally:
            db.close()

    @strawberry.mutation
    async def update_evento(self, evento: EventosInput) -> Eventos:
        from app.websocket.client import websocket_client
        from datetime import datetime
        import logging

        db = SessionLocal()
        logger = logging.getLogger(__name__)
        try:
            evento_actualizado = await update_evento(evento, db=db)

            notification_data = {
                "event": "evento_actualizado",
                "data": {
                    "eventos_id": evento_actualizado.eventos_id,
                    "nombre": evento_actualizado.nombre,
                    "fecha": str(evento_actualizado.fecha),
                    "hora": str(evento_actualizado.hora),
                    "ubicacion": evento_actualizado.ubicacion,
                    "fecha_actualizacion": datetime.now().isoformat()
                },
                "timestamp": datetime.now().isoformat()
            }

            await websocket_client.send_message(
                room="admin",
                event="notificacion",
                data=notification_data
            )
            logger.info(f"Notificación de evento actualizado enviada: {notification_data}")

            return evento_actualizado
        except Exception as e:
            logger.error(f"Error al actualizar evento: {str(e)}")
            raise
        finally:
            db.close()

    @strawberry.mutation
    async def delete_evento(self, evento: EventosDelete) -> bool:
        from app.websocket.client import websocket_client
        from datetime import datetime
        import logging

        db = SessionLocal()
        logger = logging.getLogger(__name__)
        try:
            exito = await delete_evento(evento_id=evento.eventos_id, db=db)

            if exito:
                notification_data = {
                    "event": "evento_eliminado",
                    "data": {
                        "eventos_id": evento.eventos_id,
                        "fecha_eliminacion": datetime.now().isoformat()
                    },
                    "timestamp": datetime.now().isoformat()
                }

                await websocket_client.send_message(
                    room="admin",
                    event="notificacion",
                    data=notification_data
                )
                logger.info(f"Notificación de evento eliminado enviada: {notification_data}")

            return exito
        except Exception as e:
            logger.error(f"Error al eliminar evento: {str(e)}")
            raise
        finally:
            db.close()

    @strawberry.mutation
    async def create_asignacion(self, asignacion: AsignacionesInput) -> Asignaciones:
        return await insert_asignacion(asignacion)

    @strawberry.mutation
    async def update_asignacion(self, asignacion: AsignacionesInput) -> Asignaciones:
        return await update_asignacion(asignacion)

    @strawberry.mutation
    async def delete_asignacion(self, asignacion: AsignacionesDelete) -> bool:
        return await delete_asignacion(asignacion_id=asignacion.asignaciones_id)

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
