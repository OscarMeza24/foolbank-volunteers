import pytest
from fastapi import status
from datetime import datetime, timedelta
from app.models.models import Eventos

# Pruebas para los endpoints de eventos
class TestEventos:
    # Prueba para obtener todos los eventos (GET /eventos)
    def test_get_eventos_empty(self, client):
        """Test para obtener la lista de eventos cuando está vacía"""
        response = client.get("/eventos")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    # Prueba para crear un nuevo evento (POST /add-eventos/)
    def test_create_evento(self, client, evento_data):
        """Test para crear un nuevo evento"""
        response = client.post("/add-eventos/", json=evento_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == evento_data["nombre"]
        assert data["ubicacion"] == evento_data["ubicacion"]
        assert "eventos_id" in data

    # Prueba para obtener un evento específico (GET /eventos/{evento_id})
    def test_get_evento(self, client, evento_data):
        """Test para obtener un evento por su ID"""
        # Primero creamos un evento
        create_response = client.post("/add-eventos/", json=evento_data)
        evento_id = create_response.json()["eventos_id"]
        
        # Luego lo obtenemos
        response = client.get(f"/eventos/{evento_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["eventos_id"] == evento_id
        assert data["nombre"] == evento_data["nombre"]

    # Prueba para actualizar un evento (PUT /update-eventos/)
    def test_update_evento(self, client, evento_data):
        """Test para actualizar un evento existente"""
        # Primero creamos un evento
        create_response = client.post("/add-eventos/", json=evento_data)
        evento_id = create_response.json()["eventos_id"]
        
        # Datos actualizados
        updated_data = evento_data.copy()
        updated_data["eventos_id"] = evento_id
        updated_data["nombre"] = "Evento Actualizado"
        updated_data["ubicacion"] = "Nueva Ubicación"
        
        # Actualizamos el evento
        response = client.put("/update-eventos/", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == "Evento Actualizado"
        assert data["ubicacion"] == "Nueva Ubicación"

    # Prueba para eliminar un evento (DELETE /delete-eventos/{evento_id})
    def test_delete_evento(self, client, evento_data):
        """Test para eliminar un evento"""
        # Primero creamos un evento
        create_response = client.post("/add-eventos/", json=evento_data)
        evento_id = create_response.json()["eventos_id"]
        
        # Luego lo eliminamos
        response = client.delete(f"/delete-eventos/{evento_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verificamos que ya no exista
        get_response = client.get(f"/eventos/{evento_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    # Prueba para validar la creación de un evento con fecha pasada
    def test_create_evento_fecha_pasada(self, client, evento_data):
        """Test para validar que no se pueda crear un evento con fecha pasada"""
        # Configuramos una fecha pasada
        fecha_pasada = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        evento_data["fecha"] = fecha_pasada
        
        # Intentamos crear el evento
        response = client.post("/add-eventos/", json=evento_data)
        
        # Debería fallar con un error de validación
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "La fecha del evento no puede ser en el pasado" in response.text

    # Prueba para validar la creación de un evento sin voluntarios necesarios
    def test_create_evento_sin_voluntarios(self, client, evento_data):
        """Test para validar que no se pueda crear un evento sin especificar voluntarios necesarios"""
        # Eliminamos el campo voluntarios_necesarios
        del evento_data["voluntarios_necesarios"]
        
        # Intentamos crear el evento
        response = client.post("/add-eventos/", json=evento_data)
        
        # Debería fallar con un error de validación
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
