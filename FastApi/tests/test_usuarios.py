import pytest
from fastapi import status
from app.models.models import Usuarios

# Pruebas para los endpoints de usuarios
class TestUsuarios:
    # Prueba para obtener todos los usuarios (GET /usuarios)
    def test_get_usuarios_empty(self, client):
        """Test para obtener la lista de usuarios cuando está vacía"""
        response = client.get("/usuarios")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    # Prueba para crear un nuevo usuario (POST /add-usuarios/)
    def test_create_usuario(self, client, usuario_data):
        """Test para crear un nuevo usuario"""
        response = client.post("/add-usuarios/", json=usuario_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == usuario_data["nombre"]
        assert data["correo"] == usuario_data["correo"]
        assert "usuarios_id" in data

    # Prueba para obtener un usuario específico (GET /usuarios/{usuario_id})
    def test_get_usuario(self, client, usuario_data):
        """Test para obtener un usuario por su ID"""
        # Primero creamos un usuario
        create_response = client.post("/add-usuarios/", json=usuario_data)
        usuario_id = create_response.json()["usuarios_id"]
        
        # Luego lo obtenemos
        response = client.get(f"/usuarios/{usuario_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["usuarios_id"] == usuario_id
        assert data["nombre"] == usuario_data["nombre"]

    # Prueba para actualizar un usuario (PUT /update-usuarios/)
    def test_update_usuario(self, client, usuario_data):
        """Test para actualizar un usuario existente"""
        # Primero creamos un usuario
        create_response = client.post("/add-usuarios/", json=usuario_data)
        usuario_id = create_response.json()["usuarios_id"]
        
        # Datos actualizados
        updated_data = usuario_data.copy()
        updated_data["nombre"] = "Nombre Actualizado"
        updated_data["telefono"] = "9876543210"
        
        # Actualizamos el usuario
        response = client.put("/update-usuarios/", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == "Nombre Actualizado"
        assert data["telefono"] == "9876543210"

    # Prueba para eliminar un usuario (DELETE /delete-usuarios/{usuario_id})
    def test_delete_usuario(self, client, usuario_data):
        """Test para eliminar un usuario"""
        # Primero creamos un usuario
        create_response = client.post("/add-usuarios/", json=usuario_data)
        usuario_id = create_response.json()["usuarios_id"]
        
        # Luego lo eliminamos
        response = client.delete(f"/delete-usuarios/{usuario_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verificamos que ya no exista
        get_response = client.get(f"/usuarios/{usuario_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    # Prueba para validar la creación de un usuario con datos inválidos
    def test_create_usuario_invalid_data(self, client):
        """Test para validar la creación de un usuario con datos inválidos"""
        invalid_data = {
            "nombre": "",  # Nombre vacío no permitido
            "correo": "no-es-un-correo",  # Formato de correo inválido
            "tipo": "tipo_invalido"  # Tipo no permitido
        }
        response = client.post("/add-usuarios/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Prueba para verificar la duplicación de correo electrónico
    def test_duplicate_email(self, client, usuario_data):
        """Test para verificar que no se puedan crear usuarios con el mismo correo"""
        # Creamos el primer usuario
        response1 = client.post("/add-usuarios/", json=usuario_data)
        assert response1.status_code == status.HTTP_200_OK
        
        # Intentamos crear otro usuario con el mismo correo
        usuario_data_2 = usuario_data.copy()
        usuario_data_2["usuarios_id"] = 2  # ID diferente
        response2 = client.post("/add-usuarios/", json=usuario_data_2)
        
        # Debería fallar con un error de validación
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "El correo electrónico ya está registrado" in response2.text
