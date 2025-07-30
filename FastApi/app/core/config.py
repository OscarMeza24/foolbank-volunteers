from pydantic_settings import BaseSettings
from typing import List, Optional, Union
import os
from pathlib import Path

class Settings(BaseSettings):
    # Configuración de la base de datos
    DATABASE_URL: str = "sqlite:///./sqlite.db"
    
    # Configuración de autenticación
    SECRET_KEY: str = "una_clave_secreta_muy_segura"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Configuración de OpenRoute Service
    OPENROUTE_API_KEY: str = "tu_api_key_aqui"
    OPENROUTE_BASE_URL: str = "https://api.openrouteservice.org/v2"
    
    # Configuración del agente
    AGENT_MAX_RETRIES: int = 3
    AGENT_TIMEOUT: int = 60
    AGENT_MAX_DISTANCE_KM: float = 20.0
    AGENT_MIN_SKILL_MATCH: float = 0.5
    
    # Configuración de n8n
    N8N_WEBHOOK_URL: str = "http://localhost:5678/webhook/"
    N8N_TIMEOUT: int = 30
    N8N_RETRIES: int = 3
    
    # Configuración de depuración
    DEBUG: bool = True
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # Permite variables adicionales no definidas

# Crear instancia de configuración
settings = Settings()

# Crear el directorio de la base de datos si no existe
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SQLITE_DB_PATH = BASE_DIR / "sqlite.db"
SQLITE_DIR = SQLITE_DB_PATH.parent
SQLITE_DIR.mkdir(parents=True, exist_ok=True)
