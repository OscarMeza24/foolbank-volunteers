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

# Copiar archivos con permisos de solo lectura
# Archivos individuales
COPY --chown=appuser:appgroup --chmod=444 \
    ./main.py \
    ./alembic.ini \
    /app/

# Copiar directorios con permisos mínimos
RUN mkdir -p /app/app && \
    mkdir -p /app/alembic && \
    mkdir -p /app/database && \
    mkdir -p /app/FastApi && \
    mkdir -p /app/tests && \
    chmod 555 /app/app /app/alembic /app/database /app/FastApi /app/tests

# Copiar contenido de los directorios con permisos de solo lectura
COPY --chown=appuser:appgroup --chmod=444 \
    ./app/ /app/app/
COPY --chown=appuser:appgroup --chmod=444 \
    ./alembic/ /app/alembic/
COPY --chown=appuser:appgroup --chmod=444 \
    ./database/ /app/database/
COPY --chown=appuser:appgroup --chmod=444 \
    ./FastApi/ /app/FastApi/
COPY --chown=appuser:appgroup --chmod=444 \
    ./tests/ /app/tests/

# Asegurar permisos de solo lectura en todos los archivos
RUN find /app -type f -exec chmod 444 {} \; && \
    find /app -type d -exec chmod 555 {} \;

# Crear directorios que necesiten permisos de escritura
RUN mkdir -p /app/logs && \
    chmod 755 /app/logs

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]