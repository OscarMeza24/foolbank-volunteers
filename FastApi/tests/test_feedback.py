import pytest
from fastapi import status
from app.models.models import Feedback, Eventos, Voluntarios, Usuarios

# Pruebas para los endpoints de feedback
class TestFeedback:
    # Prueba para obtener todos los feedbacks (GET /feedback)
    def test_get_feedback_empty(self, client):
        """Test para obtener la lista de feedbacks cuando está vacía"""
        response = client.get("/feedback")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    # Prueba para crear un nuevo feedback (POST /add-feedback/)
    def test_create_feedback(self, client, usuario_data, voluntario_data, evento_data, feedback_data):
        """Test para crear un nuevo feedback"""
        # Configuración inicial
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        # Actualizamos los IDs en los datos del feedback
        feedback_data["evento_id"] = evento_id
        feedback_data["voluntario_id"] = voluntario_id
        
        # Creamos el feedback
        response = client.post("/add-feedback/", json=feedback_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["evento_id"] == evento_id
        assert data["voluntario_id"] == voluntario_id
        assert data["calificacion"] == feedback_data["calificacion"]
        assert "feedback_id" in data

    # Prueba para obtener un feedback específico (GET /feedback/{feedback_id})
    def test_get_feedback(self, client, usuario_data, voluntario_data, evento_data, feedback_data):
        """Test para obtener un feedback por su ID"""
        # Configuración inicial
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        feedback_data["evento_id"] = evento_id
        feedback_data["voluntario_id"] = voluntario_id
        
        # Creamos el feedback
        create_response = client.post("/add-feedback/", json=feedback_data)
        feedback_id = create_response.json()["feedback_id"]
        
        # Obtenemos el feedback
        response = client.get(f"/feedback/{feedback_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["feedback_id"] == feedback_id
        assert data["evento_id"] == evento_id
        assert data["voluntario_id"] == voluntario_id

    # Prueba para actualizar un feedback (PUT /update-feedback/)
    def test_update_feedback(self, client, usuario_data, voluntario_data, evento_data, feedback_data):
        """Test para actualizar un feedback existente"""
        # Configuración inicial
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        feedback_data["evento_id"] = evento_id
        feedback_data["voluntario_id"] = voluntario_id
        
        # Creamos el feedback
        create_response = client.post("/add-feedback/", json=feedback_data)
        feedback_id = create_response.json()["feedback_id"]
        
        # Datos actualizados
        updated_data = feedback_data.copy()
        updated_data["feedback_id"] = feedback_id
        updated_data["calificacion"] = 4  # Cambiamos la calificación
        updated_data["comentario"] = "Muy buena experiencia, pero hay áreas de mejora"
        
        # Actualizamos el feedback
        response = client.put("/update-feedback/", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["calificacion"] == 4
        assert "áreas de mejora" in data["comentario"]

    # Prueba para eliminar un feedback (DELETE /delete-feedback/{feedback_id})
    def test_delete_feedback(self, client, usuario_data, voluntario_data, evento_data, feedback_data):
        """Test para eliminar un feedback"""
        # Configuración inicial
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        feedback_data["evento_id"] = evento_id
        feedback_data["voluntario_id"] = voluntario_id
        
        # Creamos el feedback
        create_response = client.post("/add-feedback/", json=feedback_data)
        feedback_id = create_response.json()["feedback_id"]
        
        # Eliminamos el feedback
        response = client.delete(f"/delete-feedback/{feedback_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verificamos que ya no exista
        get_response = client.get(f"/feedback/{feedback_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    # Prueba para validar la calificación fuera de rango
    def test_create_feedback_invalid_rating(self, client, usuario_data, voluntario_data, evento_data, feedback_data):
        """Test para validar que la calificación esté dentro del rango permitido (1-5)"""
        # Configuración inicial
        user_response = client.post("/add-usuarios/", json=usuario_data)
        user_id = user_response.json()["usuarios_id"]
        
        voluntario_data["usuario_id"] = user_id
        voluntario_response = client.post("/add-voluntarios/", json=voluntario_data)
        voluntario_id = voluntario_response.json()["voluntarios_id"]
        
        evento_response = client.post("/add-eventos/", json=evento_data)
        evento_id = evento_response.json()["eventos_id"]
        
        # Intentamos crear un feedback con calificación inválida
        feedback_data["evento_id"] = evento_id
        feedback_data["voluntario_id"] = voluntario_id
        feedback_data["calificacion"] = 6  # Valor fuera de rango
        
        response = client.post("/add-feedback/", json=feedback_data)
        
        # Debería fallar con un error de validación
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Probamos con un valor mínimo inválido
        feedback_data["calificacion"] = 0
        response = client.post("/add-feedback/", json=feedback_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
