import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import httpx
import json
import math
from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.models.agent_models import VolunteerAnalysis, AnalysisStatus
from app.schemas.agent.volunteer_analysis import AnalysisResult, AnalysisRequest
from app.core.config import settings
from .n8n_integration import n8n

logger = logging.getLogger(__name__)

class VolunteerAnalyzer:
    """
    Servicio para analizar voluntarios utilizando un modelo de lenguaje.
    Ahora integrado con n8n para la orquestación del flujo de trabajo.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.openai_api_key = settings.OPENAI_API_KEY
    
    async def start_analysis(self, voluntario_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inicia el análisis de un voluntario a través del flujo de n8n.
        
        Args:
            voluntario_id: ID del voluntario a analizar
            params: Parámetros adicionales para el análisis
            
        Returns:
            Dict con el ID del análisis y estado actual
        """
        try:
            # Crear registro inicial en la base de datos
            db_analysis = VolunteerAnalysis(
                voluntario_id=voluntario_id,
                estado=AnalysisStatus.PENDING,
                parametros=params
            )
            
            self.db.add(db_analysis)
            self.db.commit()
            self.db.refresh(db_analysis)
            
            # Iniciar el flujo en n8n
            await n8n.trigger_volunteer_analysis(voluntario_id, params)
            
            return {
                "status": "started",
                "analysis_id": db_analysis.id,
                "voluntario_id": voluntario_id,
                "estado": db_analysis.estado.value
            }
            
        except Exception as e:
            logger.error(f"Error al iniciar el análisis: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al iniciar el análisis: {str(e)}"
            )
    
    async def get_analysis_status(self, analysis_id: int) -> Dict[str, Any]:
        """
        Obtiene el estado actual de un análisis.
        
        Args:
            analysis_id: ID del análisis a consultar
            
        Returns:
            Dict con los detalles del análisis
        """
        db_analysis = self.db.query(VolunteerAnalysis).filter(
            VolunteerAnalysis.id == analysis_id
        ).first()
        
        if not db_analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Análisis con ID {analysis_id} no encontrado"
            )
        
        return {
            "analysis_id": db_analysis.id,
            "voluntario_id": db_analysis.voluntario_id,
            "estado": db_analysis.estado.value,
            "fecha_creacion": db_analysis.fecha_creacion,
            "fecha_actualizacion": db_analysis.fecha_actualizacion,
            "error": db_analysis.error,
            "resultado": db_analysis.resultado
        }
    
    async def _get_volunteer_data(self, voluntario_id: int) -> Dict[str, Any]:
        """Obtiene los datos del voluntario desde la API interna."""
        # En un entorno real, esto haría una llamada HTTP a la API de voluntarios
        # Por ahora, simulamos la obtención de datos
        return {
            "id": voluntario_id,
            "nombre": "Ejemplo",
            "apellido": "Voluntario",
            "habilidades": ["Comunicación", "Trabajo en equipo", "Liderazgo"],
            "disponibilidad": "Fines de semana"
        }
    
    async def _get_volunteer_events(self, voluntario_id: int) -> Dict[str, Any]:
        """Obtiene el historial de eventos del voluntario."""
        # En un entorno real, esto haría una llamada HTTP a la API de eventos
        # Por ahora, devolvemos datos de ejemplo
        return {
            "total_eventos": 5,
            "eventos": [
                {"id": 1, "nombre": "Evento 1", "fecha": "2023-01-15", "rol": "Coordinador", "calificacion": 4.5},
                {"id": 2, "nombre": "Evento 2", "fecha": "2023-02-20", "rol": "Voluntario", "calificacion": 5.0},
                {"id": 3, "nombre": "Evento 3", "fecha": "2023-03-10", "rol": "Líder de equipo", "calificacion": 4.0},
            ],
            "calificacion_promedio": 4.5
        }
    
    async def _get_geocode(self, direccion: str) -> Optional[Tuple[float, float]]:
        """Obtiene las coordenadas geográficas de una dirección usando OpenRouteService."""
        url = f"{settings.OPENROUTE_BASE_URL}/geocode/search"
        headers = {
            "Authorization": settings.OPENROUTE_API_KEY,
            "Content-Type": "application/json"
        }
        params = {"text": direccion, "size": 1}
        
        try:
            async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("features") and len(data["features"]) > 0:
                    lon, lat = data["features"][0]["geometry"]["coordinates"]
                    return (lat, lon)
                return None
                
        except httpx.HTTPStatusError as e:
            logging.error(f"Error en geocodificación: {e.response.text}")
            return None
        except Exception as e:
            logging.error(f"Error inesperado en geocodificación: {str(e)}")
            return None
    
    async def _calculate_distance_matrix(
        self, 
        origins: List[Tuple[float, float]], 
        destinations: List[Tuple[float, float]]
    ) -> Optional[List[List[float]]]:
        """Calcula la matriz de distancias entre orígenes y destinos."""
        url = f"{settings.OPENROUTE_BASE_URL}/matrix/driving-car"
        headers = {
            "Authorization": settings.OPENROUTE_API_KEY,
            "Content-Type": "application/json"
        }
        
        payload = {
            "locations": [list(coord) for coord in (origins + destinations)],
            "sources": list(range(len(origins))),
            "destinations": list(range(len(origins), len(origins) + len(destinations))),
            "metrics": ["distance"],
            "units": "km"
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
                response = await client.post(
                    url, 
                    headers=headers, 
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                
                # Convertir distancias a kilómetros
                return [
                    [dist / 1000.0 for dist in row] 
                    for row in data.get("distances", [])
                ]
                
        except Exception as e:
            logging.error(f"Error al calcular matriz de distancias: {str(e)}")
            return None
    
    async def _generate_analysis(
        self, 
        voluntario_data: Dict[str, Any],
        historial_eventos: Dict[str, Any],
        idioma: str = "es"
    ) -> AnalysisResult:
        """
        Genera un análisis del voluntario utilizando OpenRouteService para análisis de ubicación.
        """
        # Obtener ubicación del voluntario
        ubicacion_voluntario = await self._get_geocode(voluntario_data.get("direccion", ""))
        
        # Obtener ubicaciones de eventos futuros
        eventos_futuros = await self._get_future_events()
        
        # Calcular distancias a eventos futuros si hay ubicación
        compatibilidad_eventos = {}
        if ubicacion_voluntario:
            ubicaciones_eventos = []
            eventos_con_ubicacion = []
            
            for evento in eventos_futuros:
                if "ubicacion" in evento:
                    ubicacion = await self._get_geocode(evento["ubicacion"])
                    if ubicacion:
                        ubicaciones_eventos.append(ubicacion)
                        eventos_con_ubicacion.append(evento)
            
            if ubicaciones_eventos:
                distancias = await self._calculate_distance_matrix(
                    [ubicacion_voluntario], 
                    ubicaciones_eventos
                )
                
                if distancias:
                    for i, evento in enumerate(eventos_con_ubicacion):
                        distancia_km = distancias[0][i] if i < len(distancias[0]) else float('inf')
                        # Calcular puntuación de compatibilidad basada en distancia
                        if distancia_km <= settings.AGENT_MAX_DISTANCE_KM:
                            puntuacion = 1.0 - (distancia_km / settings.AGENT_MAX_DISTANCE_KM)
                            compatibilidad_eventos[evento["nombre"]] = round(puntuacion, 2)
        
        # Calcular habilidades destacadas (ejemplo simplificado)
        habilidades_voluntario = set(voluntario_data.get("habilidades", []))
        habilidades_destacadas = []
        
        for evento in historial_eventos.get("eventos", []):
            habilidades_evento = set(evento.get("habilidades_requeridas", []))
            habilidades_comunes = habilidades_voluntario.intersection(habilidades_evento)
            habilidades_destacadas.extend(habilidades_comunes)
        
        # Contar ocurrencias de habilidades
        from collections import Counter
        habilidades_contadas = Counter(habilidades_destacadas)
        habilidades_destacadas = [h for h, _ in habilidades_contadas.most_common(3)]
        
        # Generar resumen basado en la participación
        total_eventos = historial_eventos.get("total_eventos", 0)
        calificacion_promedio = historial_eventos.get("calificacion_promedio", 0)
        
        if total_eventos == 0:
            resumen = "Nuevo voluntario sin historial de participación."
        elif calificacion_promedio >= 4.5:
            resumen = "Voluntario altamente valorado con excelente desempeño en eventos."
        elif calificacion_promedio >= 3.5:
            resumen = "Voluntario con buen desempeño y participación constante."
        else:
            resumen = "Voluntario que podría beneficiarse de mayor capacitación."
        
        # Crear resultado del análisis
        return AnalysisResult(
            voluntario_id=voluntario_data["id"],
            resumen=resumen,
            fortalezas=[
                f"Ha participado en {total_eventos} eventos",
                f"Calificación promedio: {calificacion_promedio:.1f}/5.0"
            ] + (["Ubicación óptima para eventos cercanos"] if ubicacion_voluntario else []),
            areas_mejora=[
                "Podría mejorar en puntualidad" if calificacion_promedio < 4.0 else "",
                "Considerar más capacitación" if calificacion_promedio < 3.5 else ""
            ],
            recomendaciones=[
                "Asignar a eventos cercanos" if compatibilidad_eventos else "",
                "Considerar para liderazgo" if calificacion_promedio >= 4.5 else ""
            ],
            eventos_participados=total_eventos,
            calificacion_promedio=calificacion_promedio,
            ultima_participacion=historial_eventos.get("eventos", [{}])[0].get("fecha", "N/A"),
            habilidades_destacadas=habilidades_destacadas,
            compatibilidad_eventos_futuros=compatibilidad_eventos
        )
    
    async def _get_future_events(self) -> List[Dict[str, Any]]:
        """Obtiene los eventos futuros desde la API interna."""
        # En un entorno real, esto haría una llamada HTTP a la API de eventos
        # Por ahora, devolvemos datos de ejemplo
        return [
            {
                "id": 1,
                "nombre": "Recaudación de fondos",
                "fecha": "2023-08-15",
                "ubicacion": "Calle Falsa 123, Ciudad de México",
                "habilidades_requeridas": ["Comunicación", "Ventas"]
            },
            {
                "id": 2,
                "nombre": "Capacitación de voluntarios",
                "fecha": "2023-08-20",
                "ubicacion": "Avenida Siempre Viva 742, Ciudad de México",
                "habilidades_requeridas": ["Enseñanza", "Paciencia"]
            }
        ]
