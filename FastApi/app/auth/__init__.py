# Este archivo hace que el directorio sea un paquete de Python

from .routes import router as auth_router

__all__ = ["auth_router"]
