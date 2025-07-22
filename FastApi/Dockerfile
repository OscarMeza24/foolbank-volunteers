# Usar una imagen base de Python
FROM python:3.9-slim

# Crear un usuario y grupo no root
RUN addgroup --system appgroup && \
    adduser --system --no-create-home --disabled-password appuser --ingroup appgroup

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos e instalar dependencias
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt && \
    # Asegurarse de que el directorio sea accesible por el usuario no root
    chown -R appuser:appgroup /app

# Cambiar al usuario no root
USER appuser

# Copiar solo los archivos necesarios de la aplicación
COPY --chown=appuser:appgroup ./main.py /app/
COPY --chown=appuser:appgroup ./app /app/app
COPY --chown=appuser:appgroup ./alembic.ini /app/
COPY --chown=appuser:appgroup ./alembic /app/alembic
COPY --chown=appuser:appgroup ./database /app/database
COPY --chown=appuser:appgroup ./FastApi /app/FastApi
COPY --chown=appuser:appgroup ./tests /app/tests

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]