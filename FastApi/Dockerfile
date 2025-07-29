# Usar una imagen base de Python
FROM python:3.9-slim as builder

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos e instalar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --user -r requirements.txt

# Segunda etapa: imagen de producción
FROM python:3.9-slim

# Crear un usuario y grupo no root
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /sbin/nologin appuser

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar las dependencias instaladas
COPY --from=builder /root/.local /root/.local

# Asegurarse de que los scripts en .local sean ejecutables
ENV PATH=/root/.local/bin:$PATH

# Copiar el código de la aplicación
COPY . .

# Crear directorio de logs y establecer permisos
RUN mkdir -p /app/logs && \
    chown -R appuser:appgroup /app && \
    chmod -R 555 /app && \
    chmod 755 /app/logs

# Cambiar al usuario no root
USER appuser

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]