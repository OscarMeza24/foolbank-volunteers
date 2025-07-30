from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.db.session import get_db
from app.schemas.agent.volunteer_analysis import (
    VolunteerAnalysisCreate,
    VolunteerAnalysisInDB,
    AnalysisRequest,
    AnalysisResult
)
from app.agent_flow.volunteer_analyzer import VolunteerAnalyzer
from app.core.security import get_current_active_user

router = APIRouter()

@router.post(
    "/analyze-volunteer",
    response_model=Dict[str, Any],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Inicia un análisis de voluntario",
    description="""
    Inicia un análisis asíncrono de un voluntario utilizando un flujo de n8n.
    Devuelve inmediatamente con un ID de análisis que puede usarse para consultar el estado.
    """
)
async def analyze_volunteer(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Inicia un análisis asíncrono de un voluntario utilizando n8n.
    """
    analyzer = VolunteerAnalyzer(db)
    return await analyzer.start_analysis(
        voluntario_id=request.voluntario_id,
        params={
            "incluir_historico": request.incluir_historico,
            "incluir_recomendaciones": request.incluir_recomendaciones,
            "idioma": request.idioma
        }
    )

@router.get(
    "/analysis/{analysis_id}",
    response_model=Dict[str, Any],
    summary="Obtiene el estado de un análisis",
    description="""
    Consulta el estado de un análisis de voluntario por su ID.
    """
)
async def get_analysis_status(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Obtiene el estado de un análisis por su ID.
    """
    analyzer = VolunteerAnalyzer(db)
    return await analyzer.get_analysis_status(analysis_id)

@router.get(
    "/volunteer/{voluntario_id}/analyses",
    response_model=List[Dict[str, Any]],
    summary="Obtiene todos los análisis de un voluntario",
    description="""
    Devuelve todos los análisis realizados para un voluntario específico.
    """
)
async def get_volunteer_analyses(
    voluntario_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Obtiene todos los análisis realizados para un voluntario.
    """
    analyzer = VolunteerAnalyzer(db)
    
    # Obtener análisis de la base de datos
    analyses = db.query(VolunteerAnalysis).filter(
        VolunteerAnalysis.voluntario_id == voluntario_id
    ).order_by(
        VolunteerAnalysis.fecha_creacion.desc()
    ).offset(skip).limit(limit).all()
    
    # Convertir a formato de diccionario
    return [
        {
            "analysis_id": a.id,
            "voluntario_id": a.voluntario_id,
            "estado": a.estado.value,
            "fecha_creacion": a.fecha_creacion,
            "fecha_actualizacion": a.fecha_actualizacion,
            "error": a.error,
            "resultado": a.resultado
        }
        for a in analyses
    ]

# Webhook para que n8n actualice el estado de los análisis
@router.post(
    "/webhook/analysis-update",
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def update_analysis_webhook(
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Webhook que n8n usa para actualizar el estado de un análisis.
    No está documentado en la API pública.
    """
    try:
        analysis_id = data.get("analysis_id")
        status_update = data.get("status")
        result = data.get("result")
        error = data.get("error")
        
        if not analysis_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se requiere el ID del análisis"
            )
        
        # Obtener el análisis de la base de datos
        db_analysis = db.query(VolunteerAnalysis).filter(
            VolunteerAnalysis.id == analysis_id
        ).first()
        
        if not db_analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Análisis con ID {analysis_id} no encontrado"
            )
        
        # Actualizar el estado
        if status_update == "completed":
            db_analysis.estado = AnalysisStatus.COMPLETED
            db_analysis.resultado = result
        elif status_update == "failed":
            db_analysis.estado = AnalysisStatus.FAILED
            db_analysis.error = error
        else:
            db_analysis.estado = status_update
        
        db_analysis.fecha_actualizacion = datetime.utcnow()
        db.commit()
        
        return {"status": "success", "message": "Análisis actualizado correctamente"}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error en el webhook de actualización: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la actualización: {str(e)}"
        )
