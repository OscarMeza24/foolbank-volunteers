import pytest
from fastapi import status
from datetime import datetime
from app.models.models import Asignaciones, Eventos, Voluntarios, Usuarios

# Pruebas para los endpoints de asignaciones
class TestAsignaciones:
    # Prueba para obtener todas las asignaciones (GET /asignaciones)
    def test_get_asignaciones_empty(self, client):
        """Test para obtener la lista de asignaciones cuando está vacía"""
        response = client.get("/asignaciones")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    # Prueba para crear una nueva asignación (POST /add-asignaciones/)
    def test_create_asignacion(self, client, usuario_data, voluntario_data, evento_data, asignacion_data):
        """Test para crear una nueva asignación"""
        # Primero creamos un usuario, un voluntario y un evento
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        # Actualizamos los IDs en los datos de la asignación
        asignacion_data["evento_id"] = evento_id
        asignacion_data["voluntario_id"] = voluntario_id
        
        # Creamos la asignación
        response = client.post("/add-asignaciones/", json=asignacion_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["evento_id"] == evento_id
        assert data["voluntario_id"] == voluntario_id
        assert "asignaciones_id" in data

    # Prueba para obtener una asignación específica (GET /asignaciones/{asignacion_id})
    def test_get_asignacion(self, client, usuario_data, voluntario_data, evento_data, asignacion_data):
        """Test para obtener una asignación por su ID"""
        # Configuración inicial
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        asignacion_data["evento_id"] = evento_id
        asignacion_data["voluntario_id"] = voluntario_id
        
        # Creamos la asignación
        create_response = client.post("/add-asignaciones/", json=asignacion_data)
        asignacion_id = create_response.json()["asignaciones_id"]
        
        # Obtenemos la asignación
        response = client.get(f"/asignaciones/{asignacion_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["asignaciones_id"] == asignacion_id
        assert data["evento_id"] == evento_id
        assert data["voluntario_id"] == voluntario_id

    # Prueba para actualizar una asignación (PUT /update-asignaciones/)
    def test_update_asignacion(self, client, usuario_data, voluntario_data, evento_data, asignacion_data):
        """Test para actualizar una asignación existente"""
        # Configuración inicial
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        asignacion_data["evento_id"] = evento_id
        asignacion_data["voluntario_id"] = voluntario_id
        
        # Creamos la asignación
        create_response = client.post("/add-asignaciones/", json=asignacion_data)
        asignacion_id = create_response.json()["asignaciones_id"]
        
        # Datos actualizados
        updated_data = asignacion_data.copy()
        updated_data["asignaciones_id"] = asignacion_id
        updated_data["rol"] = "Coordinador"
        updated_data["estado"] = "Confirmado"
        
        # Actualizamos la asignación
        response = client.put("/update-asignaciones/", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["rol"] == "Coordinador"
        assert data["estado"] == "Confirmado"

    # Prueba para eliminar una asignación (DELETE /delete-asignaciones/{asignacion_id})
    def test_delete_asignacion(self, client, usuario_data, voluntario_data, evento_data, asignacion_data):
        """Test para eliminar una asignación"""
        # Configuración inicial
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        asignacion_data["evento_id"] = evento_id
        asignacion_data["voluntario_id"] = voluntario_id
        
        # Creamos la asignación
        create_response = client.post("/add-asignaciones/", json=asignacion_data)
        asignacion_id = create_response.json()["asignaciones_id"]
        
        # Eliminamos la asignación
        response = client.delete(f"/delete-asignaciones/{asignacion_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verificamos que ya no exista
        get_response = client.get(f"/asignaciones/{asignacion_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    # Prueba para validar la creación de una asignación con voluntario ya asignado
    def test_create_asignacion_voluntario_ya_asignado(self, client, usuario_data, voluntario_data, evento_data, asignacion_data):
        """Test para validar que no se pueda asignar dos veces al mismo voluntario al mismo evento"""
        # Configuración inicial
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        # Primera asignación
        asignacion_data["evento_id"] = evento_id
        asignacion_data["voluntario_id"] = voluntario_id
        response1 = client.post("/add-asignaciones/", json=asignacion_data)
        assert response1.status_code == status.HTTP_200_OK
        
        # Segunda asignación con los mismos datos
        response2 = client.post("/add-asignaciones/", json=asignacion_data)
        
        # Debería fallar con un error de validación
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "El voluntario ya está asignado a este evento" in response2.text
