from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class AgentSettings(BaseSettings):
    """Configuración para el módulo de agente autónomo."""
    
    # Configuración de OpenRoute Service
    OPENROUTE_API_KEY: str = os.getenv("OPENROUTE_API_KEY", "your_api_key_here")
    OPENROUTE_BASE_URL: str = os.getenv("OPENROUTE_BASE_URL", "https://api.openrouteservice.org/v2")
    
    # Configuración del agente
    AGENT_MAX_RETRIES: int = int(os.getenv("AGENT_MAX_RETRIES", "3"))
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", "60"))
    AGENT_MAX_DISTANCE_KM: float = float(os.getenv("AGENT_MAX_DISTANCE_KM", "20.0"))
    AGENT_MIN_SKILL_MATCH: float = float(os.getenv("AGENT_MIN_SKILL_MATCH", "0.5"))
    
    # Configuración de la API interna
    INTERNAL_API_BASE_URL: str = os.getenv("INTERNAL_API_BASE_URL", "http://localhost:8000/api/v1")
    
    # Configuración de n8n (para integración futura)
    N8N_WEBHOOK_URL: Optional[str] = os.getenv("N8N_WEBHOOK_URL")
    
    # Tiempo de espera máximo para las solicitudes HTTP (en segundos)
    HTTP_TIMEOUT: int = int(os.getenv("HTTP_TIMEOUT", "30"))
    
    # Nivel de registro (debug, info, warning, error, critical)
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info").lower()
    
    # Ignorar campos adicionales para evitar errores de validación
    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instancia de configuración
settings = AgentSettings()

# Configuración de logging
import logging

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
