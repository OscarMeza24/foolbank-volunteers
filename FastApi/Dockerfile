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

# Configurar directorio de trabajo con permisos seguros
RUN mkdir -p /app/logs && \
    chown -R appuser:appgroup /app && \
    chmod -R 555 /app && \
    chmod 755 /app/logs

# Cambiar al usuario no root
USER appuser

# Copiar archivos con permisos de solo lectura (444)
COPY --chown=root:root --chmod=444 --from=stage \
    main.py \
    alembic.ini \
    /app/

# Copiar directorios con permisos de solo lectura (555)
COPY --chown=root:root --chmod=555 --from=stage \
    app \
    alembic \
    database \
    FastApi \
    tests \
    /app/

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]