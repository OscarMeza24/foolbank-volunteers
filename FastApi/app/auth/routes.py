from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.models import Usuarios
from .schemas import Token, UserCreate, UserInDB, UserLogin
from .jwt_handler import (
    create_access_token,
    get_password_hash,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserInDB)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el correo ya está registrado
    db_user = db.query(Usuarios).filter(Usuarios.correo == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user.password)
    db_user = Usuarios(
        nombre=user.nombre,
        apellido=user.apellido,
        correo=user.email,
        telefono=user.telefono,
        tipo=user.tipo,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=False  # Podrías implementar verificación por correo electrónico
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(Usuarios).filter(Usuarios.correo == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.correo, "user_id": user.usuarios_id, "user_type": user.tipo},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: Usuarios = Depends(get_current_user)):
    return current_user
