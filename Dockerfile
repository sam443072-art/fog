# Dockerfile para Google Cloud Run

FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto 8080 (requerido por Cloud Run)
EXPOSE 8080

# Comando para ejecutar la aplicación
# main.py ya está configurado para leer el puerto de Render/Railway
CMD ["python", "main.py"]
