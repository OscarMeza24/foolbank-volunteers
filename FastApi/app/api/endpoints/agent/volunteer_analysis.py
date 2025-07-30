from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.db.session import get_db
from app.schemas.agent.volunteer_analysis import (
    VolunteerAnalysisCreate,
    VolunteerAnalysisInDB,
    AnalysisRequest,
    AnalysisResult
)
from app.models.agent_models import VolunteerAnalysis, AnalysisStatus
from app.agent_flow.volunteer_analyzer import VolunteerAnalyzer
from app.core.security import get_current_active_user

router = APIRouter()

@router.post(
    "/analyze-volunteer",
    response_model=VolunteerAnalysisInDB,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Inicia un análisis de voluntario",
    description="""
    Inicia un análisis asíncrono de un voluntario utilizando un modelo de lenguaje.
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
    Inicia un análisis asíncrono de un voluntario.
    """
    # Verificar permisos (opcional, dependiendo de tu lógica de autorización)
    # if not current_user.is_admin and not current_user.is_analyst:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="No tiene permisos para realizar análisis"
    #     )
    
    # Crear registro de análisis en la base de datos
    db_analysis = VolunteerAnalysis(
        voluntario_id=request.voluntario_id,
        estado=AnalysisStatus.PENDING,
        parametros={
            "incluir_historico": request.incluir_historico,
            "incluir_recomendaciones": request.incluir_recomendaciones,
            "idioma": request.idioma
        }
    )
    
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    # Iniciar tarea en segundo plano
    analyzer = VolunteerAnalyzer(db)
    background_tasks.add_task(
        analyzer.analyze_volunteer,
        analysis_id=db_analysis.id
    )
    
    return db_analysis

@router.get(
    "/analysis/{analysis_id}",
    response_model=VolunteerAnalysisInDB,
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
    db_analysis = db.query(VolunteerAnalysis).filter(
        VolunteerAnalysis.id == analysis_id
    ).first()
    
    if not db_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Análisis con ID {analysis_id} no encontrado"
        )
    
    # Verificar permisos (opcional)
    # if not current_user.is_admin and db_analysis.voluntario_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="No tiene permisos para ver este análisis"
    #     )
    
    return db_analysis

@router.get(
    "/volunteer/{voluntario_id}/analyses",
    response_model=list[VolunteerAnalysisInDB],
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
    # Verificar permisos (opcional)
    # if not current_user.is_admin and voluntario_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="No tiene permisos para ver estos análisis"
    #     )
    
    analyses = db.query(VolunteerAnalysis).filter(
        VolunteerAnalysis.voluntario_id == voluntario_id
    ).order_by(
        VolunteerAnalysis.fecha_creacion.desc()
    ).offset(skip).limit(limit).all()
    
    return analyses
