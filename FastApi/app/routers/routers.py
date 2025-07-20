from typing import List
from fastapi import HTTPException
from app.models.models import Usuarios, Voluntarios, Eventos, Asignaciones, Feedback
from app.models.schema import UsuariosModel, VoluntariosModel, EventosModel, AsignacionesModel, FeedbackModel
from fastapi import APIRouter
from app.database.database import SessionLocal
from fastapi.encoders import jsonable_encoder

router = APIRouter()
db = SessionLocal()

@router.get("/", tags=["root"])
async def root():
    return {"message": "Bienvenido a la API de FoodBank"}

@router.get("/usuarios", response_model=None, tags=["usuarios"])
async def get_usuarios() -> List[UsuariosModel]:
    usuarios = db.query(Usuarios).all()
    return usuarios


@router.post("/add-usuarios/", tags=["usuarios"])
async def insert_usuario(usuario: UsuariosModel):
    new_usuario = Usuarios(
        Usuarios_id=usuario.Usuarios_id,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        telefono=usuario.telefono,
        tipo=usuario.tipo

    )

    db.add(new_usuario)
    db.commit()
    db.refresh(new_usuario)
    return new_usuario


@router.put("/update-usuarios/", tags=["usuarios"])
async def update_usuario(updated_usuario: UsuariosModel):
    print(updated_usuario)
    existing_usuario = db.query(Usuarios).filter(Usuarios.Usuarios_id == updated_usuario.Usuarios_id).first()

    if existing_usuario:
        # Update the attributes of the existing usuario
        for field, value in jsonable_encoder(updated_usuario).items():
            print(field, value)
            if value:
                setattr(existing_usuario, field, value)

        db.commit()
        db.refresh(existing_usuario)
        return existing_usuario

    return {"message": "Usuario not found"}


@router.delete("/delete-usuarios/{Usuarios_id}", tags=["usuarios"])
async def delete_usuario(Usuarios_id: int):
    existing_usuario = db.query(Usuarios).filter(Usuarios.Usuarios_id == Usuarios_id).first()

    if existing_usuario:
        db.delete(existing_usuario)
        db.commit()
        return True

    return False


@router.get("/voluntarios", response_model=None, tags=["voluntarios"])
async def get_voluntarios()->List[VoluntariosModel]:
    voluntarios = db.query(Voluntarios).all()
    return voluntarios


@router.get("/eventos", response_model=None, tags=["eventos"])
async def get_eventos() ->List[EventosModel]:
    eventos = db.query(Eventos).all()
    return eventos


@router.get("/asignaciones", response_model=None, tags=["asignaciones"])
async def get_asignaciones() ->List[AsignacionesModel]:
    asignaciones = db.query(Asignaciones).all()
    return asignaciones


@router.get("/feedback", response_model=None, tags=["feedback"])
async def get_feedback() ->List[FeedbackModel]:
    feedback = db.query(Feedback).all()
    return feedback


@router.post("/add-voluntarios/", tags=["voluntarios"])
async def insert_voluntario(voluntario: VoluntariosModel):
    new_voluntario = Voluntarios(
        voluntarios_id=voluntario.voluntarios_id,
        habilidades=voluntario.habilidades,
        disponibilidad=voluntario.disponibilidad,
        usuario_id=voluntario.usuario_id
    )
    
    db.add(new_voluntario)
    db.commit()
    db.refresh(new_voluntario)
    return new_voluntario


@router.put("/update-voluntario/", tags=["voluntarios"])
async def update_voluntario(updated_voluntario: VoluntariosModel):
    existing_voluntario = db.query(Voluntarios).filter(Voluntarios.voluntarios_id == updated_voluntario.voluntarios_id).first()

    if existing_voluntario:
        # Update the attributes of the existing buyer excluding 'buyer_id'
        update_item_encoded = jsonable_encoder(updated_voluntario)
        for field, value in update_item_encoded.items():
            if field != "voluntarios_id":
                setattr(existing_voluntario, field, value)

        db.commit()
        db.refresh(existing_voluntario)
        return existing_voluntario

    return {"message": "Voluntario not found"}


@router.delete("/delete-voluntario/{voluntario_id}", tags=["voluntarios"])
async def delete_voluntario(voluntario_id: int):
    existing_voluntario = db.query(Voluntarios).filter(Voluntarios.voluntarios_id == voluntario_id).first()

    if existing_voluntario:
        db.delete(existing_voluntario)
        db.commit()
        return True

    return False


@router.get("/eventos", response_model=None, tags=["eventos"])
async def get_eventos()->List[EventosModel]:
    eventos = db.query(Eventos).all()
    return eventos


@router.get("/asignaciones", response_model=None, tags=["asignaciones"])
async def get_asignaciones() -> List[AsignacionesModel]:
    asignaciones = db.query(Asignaciones).all()
    return asignaciones


@router.get("/feedback", response_model=None, tags=["feedback"])
async def get_feedback() -> List[FeedbackModel]:
    feedback = db.query(Feedback).all()
    return feedback


@router.get("/asignaciones", response_model=None, tags=["asignaciones"])
async def get_asignaciones() -> List[AsignacionesModel]:
    asignaciones = db.query(Asignaciones).all()
    return asignaciones


@router.post("/add-asignacion/", tags=["asignaciones"])
async def insert_asignacion(asignacion: AsignacionesModel):
    new_asignacion = Asignaciones(
        asignaciones_id=asignacion.asignaciones_id,
        voluntario_id=asignacion.voluntario_id,
        evento_id=asignacion.evento_id,
        estado=asignacion.estado
    )
    
    db.add(new_asignacion)
    db.commit()
    db.refresh(new_asignacion)
    return new_asignacion


@router.post("/add-evento/", tags=["eventos"])
async def insert_evento(evento: EventosModel):
    new_evento = Eventos(
        eventos_id=evento.eventos_id,
        nombre=evento.nombre,
        fecha=evento.fecha,
        hora=evento.hora,
        ubicacion=evento.ubicacion,
        voluntarios_necesarios=evento.voluntarios_necesarios,
        descripcion_eventos=evento.descripcion_eventos
    )
    
    db.add(new_evento)
    db.commit()
    db.refresh(new_evento)
    return new_evento

@router.post("/add-feedback/", tags=["feedback"])
async def insert_feedback(feedback: FeedbackModel):
    new_feedback = Feedback(
        feedback_id=feedback.feedback_id,
        voluntario_id=feedback.voluntario_id,
        evento_id=feedback.evento_id,
        calificacion=feedback.calificacion,
        comentario=feedback.comentario
    )
    
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


@router.put("/update-asignacion/", tags=["asignaciones"])
async def update_asignacion(updated_asignacion: AsignacionesModel):
    existing_asignacion = db.query(Asignaciones).filter(Asignaciones.asignaciones_id == updated_asignacion.asignaciones_id).first()

    if existing_asignacion:
        # Update the attributes of the existing asignacion
        for field, value in jsonable_encoder(updated_asignacion).items():
            if value is not None:  # Only update fields that are provided (not None)
                setattr(existing_asignacion, field, value)
        
        db.commit()
        db.refresh(existing_asignacion)
        return existing_asignacion
    else:
        raise HTTPException(status_code=404, detail="Asignacion no encontrada")

@router.put("/update-evento/", tags=["eventos"])
async def update_evento(updated_evento: EventosModel):
    existing_evento = db.query(Eventos).filter(Eventos.eventos_id == updated_evento.eventos_id).first()

    if existing_evento:
        # Update the attributes of the existing evento
        for field, value in jsonable_encoder(updated_evento).items():
            if value is not None:  # Only update fields that are provided (not None)
                setattr(existing_evento, field, value)
        
        db.commit()
        db.refresh(existing_evento)
        return existing_evento
    else:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

@router.put("/update-feedback/", tags=["feedback"])
async def update_feedback(updated_feedback: FeedbackModel):
    existing_feedback = db.query(Feedback).filter(Feedback.feedback_id == updated_feedback.feedback_id).first()

    if existing_feedback:
        # Update the attributes of the existing feedback
        for field, value in jsonable_encoder(updated_feedback).items():
            if value is not None:  # Only update fields that are provided (not None)
                setattr(existing_feedback, field, value)
        
        db.commit()
        db.refresh(existing_feedback)
        return existing_feedback
    else:
        raise HTTPException(status_code=404, detail="Feedback no encontrado")

@router.put("/update-voluntario/", tags=["voluntarios"])
async def update_voluntario(updated_voluntario: VoluntariosModel):
    existing_voluntario = db.query(Voluntarios).filter(Voluntarios.voluntarios_id == updated_voluntario.voluntarios_id).first()

    if existing_voluntario:
        # Update the attributes of the existing voluntario
        for field, value in jsonable_encoder(updated_voluntario).items():
            if value is not None:  # Only update fields that are provided (not None)
                setattr(existing_voluntario, field, value)
        
        db.commit()
        db.refresh(existing_voluntario)
        return existing_voluntario
    else:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")

@router.delete("/delete-asignacion/{asignacion_id}", tags=["asignaciones"])
async def delete_asignacion(asignacion_id: int):
    existing_asignacion = db.query(Asignaciones).filter(Asignaciones.asignaciones_id == asignacion_id).first()

    if existing_asignacion:
        db.delete(existing_asignacion)
        db.commit()
        return True

    return False

@router.delete("/delete-evento/{evento_id}", tags=["eventos"])
async def delete_evento(evento_id: int):
    existing_evento = db.query(Eventos).filter(Eventos.eventos_id == evento_id).first()

    if existing_evento:
        db.delete(existing_evento)
        db.commit()
        return True

    return False

@router.delete("/delete-feedback/{feedback_id}", tags=["feedback"])
async def delete_feedback(feedback_id: int):
    existing_feedback = db.query(Feedback).filter(Feedback.feedback_id == feedback_id).first()

    if existing_feedback:
        db.delete(existing_feedback)
        db.commit()
        return True

    return False

