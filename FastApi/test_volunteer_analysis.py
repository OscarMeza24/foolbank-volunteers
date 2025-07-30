import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import SQLALCHEMY_DATABASE_URL
from app.models import Base, Voluntarios, Usuarios, VolunteerAnalysis, AnalysisStatus

# Configurar la sesión de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_volunteer_analysis():
    # Crear una nueva sesión
    db = SessionLocal()
    
    try:
        print("\n=== Iniciando pruebas de VolunteerAnalysis ===")
        
        # 1. Crear un usuario de prueba si no existe
        print("\n1. Verificando usuario de prueba...")
        usuario = db.query(Usuarios).filter_by(correo="test@example.com").first()
        
        if not usuario:
            print("Creando usuario de prueba...")
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            usuario = Usuarios(
                nombre="Test",
                apellido="User",
                correo="test@example.com",
                telefono="1234567890",
                tipo="voluntario",
                hashed_password=pwd_context.hash("testpassword"),
                is_active=True,
                is_verified=True
            )
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
            print(f"Usuario de prueba creado - ID: {usuario.usuarios_id}")
        
        # 2. Verificar voluntario
        print("\n2. Verificando voluntario...")
        voluntario = db.query(Voluntarios).filter_by(usuario_id=usuario.usuarios_id).first()
        
        if not voluntario:
            print("Creando registro de voluntario...")
            voluntario = Voluntarios(
                usuario_id=usuario.usuarios_id,
                habilidades="Python, SQL, Trabajo en equipo",
                disponibilidad="Fines de semana"
            )
            db.add(voluntario)
            db.commit()
            db.refresh(voluntario)
            print(f"Registro de voluntario creado - ID: {voluntario.voluntarios_id}")
        else:
            print(f"Voluntario encontrado - ID: {voluntario.voluntarios_id}")
            
        print(f"Voluntario encontrado - ID: {voluntario.voluntarios_id}")
        
        # 3. Crear un análisis de voluntario
        print("\n3. Creando un nuevo análisis de voluntario...")
        nuevo_analisis = VolunteerAnalysis(
            voluntario_id=voluntario.voluntarios_id,
            estado=AnalysisStatus.PENDING,
            parametros={"tipo_analisis": "evaluacion_inicial", "puntuacion": 0}
        )
        
        db.add(nuevo_analisis)
        db.commit()
        db.refresh(nuevo_analisis)
        
        print(f"Análisis creado exitosamente - ID: {nuevo_analisis.id}")
        print(f"Estado inicial: {nuevo_analisis.estado.value}")
        
        # 4. Actualizar el análisis
        print("\n4. Actualizando el análisis...")
        nuevo_analisis.estado = AnalysisStatus.COMPLETED
        nuevo_analisis.resultado = {"puntuacion_final": 85, "recomendaciones": ["Excelente desempeño"]}
        nuevo_analisis.fecha_actualizacion = datetime.utcnow()
        
        db.commit()
        db.refresh(nuevo_analisis)
        
        print(f"Estado actualizado: {nuevo_analisis.estado.value}")
        print(f"Resultados: {nuevo_analisis.resultado}")
        
        # 5. Consultar el análisis
        print("\n5. Consultando el análisis...")
        analisis_consultado = db.query(VolunteerAnalysis).filter_by(id=nuevo_analisis.id).first()
        
        if analisis_consultado:
            print(f"Análisis encontrado - ID: {analisis_consultado.id}")
            print(f"Estado: {analisis_consultado.estado.value}")
            print(f"Creado: {analisis_consultado.fecha_creacion}")
            print(f"Actualizado: {analisis_consultado.fecha_actualizacion}")
            
            # Verificar la relación con el voluntario
            print(f"\n6. Verificando la relación con el voluntario...")
            print(f"Voluntario ID: {analisis_consultado.voluntario.voluntarios_id}")
            print(f"Nombre del voluntario: {analisis_consultado.voluntario.usuario.nombre}")
            
            # Verificar la relación inversa (del voluntario a los análisis)
            print(f"\n7. Verificando la relación inversa...")
            print(f"Total de análisis para este voluntario: {len(analisis_consultado.voluntario.analisis)}")
            
        # 8. Eliminar el análisis de prueba (opcional)
        print("\n8. Limpiando datos de prueba...")
        try:
            # Eliminar análisis de prueba
            if 'nuevo_analisis' in locals():
                db.delete(nuevo_analisis)
            
            # Eliminar voluntario de prueba
            if 'voluntario' in locals():
                db.delete(voluntario)
            
            # Eliminar usuario de prueba
            if 'usuario' in locals():
                db.delete(usuario)
            
            db.commit()
            print("Datos de prueba eliminados exitosamente.")
        except Exception as e:
            print(f"Error al limpiar datos de prueba: {str(e)}")
            db.rollback()
        
        print("\n=== Pruebas completadas exitosamente ===")
        
    except Exception as e:
        print(f"\nError durante las pruebas: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_volunteer_analysis()
