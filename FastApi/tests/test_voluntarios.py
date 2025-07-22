import pytest
from fastapi import status
from app.models.models import Voluntarios, Usuarios

# Pruebas para los endpoints de voluntarios
class TestVoluntarios:
    # Prueba para obtener todos los voluntarios (GET /voluntarios)
    def test_get_voluntarios_empty(self, client):
        """Test para obtener la lista de voluntarios cuando está vacía"""
        response = client.get("/voluntarios")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    # Prueba para crear un nuevo voluntario (POST /add-voluntarios/)
    def test_create_voluntario(self, client, usuario_data, voluntario_data):
        """Test para crear un nuevo voluntario"""
        # Primero creamos un usuario asociado
        user_response = client.post("/add-usuarios/", json=usuario_data)
        assert user_response.status_code == status.HTTP_200_OK
        
        # Luego creamos el voluntario
        response = client.post("/add-voluntarios/", json=voluntario_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["habilidades"] == voluntario_data["habilidades"]
        assert data["usuario_id"] == voluntario_data["usuario_id"]
        assert "voluntarios_id" in data

    # Prueba para obtener un voluntario específico (GET /voluntarios/{voluntario_id})
    def test_get_voluntario(self, client, usuario_data, voluntario_data):
        """Test para obtener un voluntario por su ID"""
        # Primero creamos un usuario y un voluntario
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        create_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = create_response.json()["voluntarios_id"]
        
        # Luego lo obtenemos
        response = client.get(f"/voluntarios/{voluntario_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["voluntarios_id"] == voluntario_id
        assert data["usuario_id"] == user_id

    # Prueba para actualizar un voluntario (PUT /update-voluntarios/)
    def test_update_voluntario(self, client, usuario_data, voluntario_data):
        """Test para actualizar un voluntario existente"""
        # Primero creamos un usuario y un voluntario
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        create_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = create_response.json()["voluntarios_id"]
        
        # Datos actualizados
        updated_data = voluntario_data.copy()
        updated_data["voluntarios_id"] = voluntario_id
        updated_data["habilidades"] = "Nuevas habilidades"
        updated_data["disponibilidad"] = "Entre semana"
        
        # Actualizamos el voluntario
        response = client.put("/update-voluntarios/", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["habilidades"] == "Nuevas habilidades"
        assert data["disponibilidad"] == "Entre semana"

    # Prueba para eliminar un voluntario (DELETE /delete-voluntarios/{voluntario_id})
    def test_delete_voluntario(self, client, usuario_data, voluntario_data):
        """Test para eliminar un voluntario"""
        # Primero creamos un usuario y un voluntario
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        create_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = create_response.json()["voluntarios_id"]
        
        # Luego lo eliminamos
        response = client.delete(f"/delete-voluntarios/{voluntario_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verificamos que ya no exista
        get_response = client.get(f"/voluntarios/{voluntario_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    # Prueba para validar la creación de un voluntario con usuario inexistente
    def test_create_voluntario_invalid_user(self, client, voluntario_data):
        """Test para validar que no se pueda crear un voluntario con un usuario inexistente"""
        # Intentamos crear un voluntario con un usuario que no existe
        voluntario_data["usuario_id"] = 9999  # ID que no existe
        response = client.post("/add-voluntarios/", json=voluntario_data)
        
        # Debería fallar con un error de validación
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "El usuario especificado no existe" in response.text
