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

# Configurar permisos antes de cambiar de usuario
RUN mkdir -p /app/logs && \
    chown -R appuser:appgroup /app && \
    chmod -R 755 /app

# Cambiar al usuario no root
USER appuser

# Copiar solo los archivos necesarios de la aplicación con permisos de solo lectura
# Archivos individuales
COPY --chown=appuser:appgroup --chmod=555 \
    ./main.py \
    ./alembic.ini \
    /app/

# Directorios
COPY --chown=appuser:appgroup --chmod=555 \
    ./app \
    ./alembic \
    ./database \
    ./FastApi \
    ./tests \
    /app/

# Crear directorios que necesiten permisos de escritura
RUN mkdir -p /app/logs && \
    chmod 755 /app/logs

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]