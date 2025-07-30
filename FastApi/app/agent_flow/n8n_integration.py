import httpx
import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)

class N8NIntegration:
    """
    Clase para manejar la integración con n8n
    """
    
    def __init__(self):
        self.base_url = settings.N8N_WEBHOOK_URL.rstrip('/')
        self.timeout = settings.N8N_TIMEOUT
        self.max_retries = settings.N8N_RETRIES
        self.client = None
    
    async def _get_client(self):
        """Obtiene un cliente HTTP asíncrono"""
        if self.client is None or self.client.is_closed:
            self.client = httpx.AsyncClient(timeout=self.timeout)
        return self.client
    
    async def close(self):
        """Cierra el cliente HTTP"""
        if self.client and not self.client.is_closed:
            await self.client.aclose()
            self.client = None
    
    async def trigger_volunteer_analysis(self, voluntario_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Activa el flujo de análisis de voluntario en n8n
        
        Args:
            voluntario_id: ID del voluntario a analizar
            params: Parámetros adicionales para el análisis
            
        Returns:
            Dict con la respuesta del webhook
        """
        webhook_url = f"{self.base_url}/webhook/volunteer-analysis"
        payload = {
            "voluntario_id": voluntario_id,
            "parametros": params
        }
        
        try:
            client = await self._get_client()
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            error_msg = f"Error al activar el flujo de análisis: {str(e)}"
            logger.error(f"{error_msg}. Response: {e.response.text}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )
            
        except Exception as e:
            error_msg = f"Error inesperado al activar el flujo de análisis: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )

# Instancia global para usar en toda la aplicación
n8n = N8NIntegration()

# Manejo de eventos de inicio y cierre de la aplicación
async def startup_n8n_client():
    """Inicializa el cliente n8n al arrancar la aplicación"""
    logger.info("Inicializando cliente n8n...")
    # No es necesario hacer nada aquí, el cliente se crea bajo demanda

async def shutdown_n8n_client():
    """Cierra el cliente n8n al detener la aplicación"""
    logger.info("Cerrando cliente n8n...")
    await n8n.close()
