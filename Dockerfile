# Dockerfile para despliegue del bot en la nube
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Crear directorio para datos persistentes
RUN mkdir -p /app/data/classifications

# Exponer puerto 10000 para el servidor HTTP
EXPOSE 10000

# Comando para ejecutar el bot CON servidor HTTP
CMD ["python", "-u", "start.py"]
