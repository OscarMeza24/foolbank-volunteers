from typing import List
from fastapi import HTTPException
from app.models.models import Headers, Lines, Buyers, Items, Markets, Resource, SalesRep
from app.models.schema import HeadersModel, LinesModel, BuyersModel, ItemsModel, MarketsModel, ResourceModel, SalesRepModel
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
        name=buyer.name,
    )
    db.add(new_buyer)
    db.commit()
    db.refresh(new_buyer)
    return buyer


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


@router.get("/asignaciones", response_model=None, tags=["asignaciones"])
async def get_asignaciones() -> List[AsignacionesModel]:
    asignaciones = db.query(Asignaciones).all()
    return asignaciones


