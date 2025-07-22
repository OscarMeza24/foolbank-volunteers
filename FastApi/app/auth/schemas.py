from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    user_type: Optional[str] = None

class UserBase(BaseModel):
    correo: EmailStr = Field(..., alias="email")
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    tipo: str

class UserCreate(UserBase):
    password: str
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "password": "contraseñaSegura123",
                "nombre": "Nombre",
                "apellido": "Apellido",
                "tipo": "voluntario",
                "telefono": "1234567890"
            }
        }

class UserInDB(UserBase):
    usuarios_id: int
    is_active: bool
    is_verified: bool

    class Config:
        orm_mode = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "usuarios_id": 1,
                "email": "usuario@ejemplo.com",
                "nombre": "Nombre",
                "apellido": "Apellido",
                "tipo": "voluntario",
                "telefono": "1234567890",
                "is_active": True,
                "is_verified": False
            }
        }

class UserLogin(BaseModel):
    email: EmailStr = Field(..., alias="username")
    password: str
    
    class Config:
        populate_by_name = True
