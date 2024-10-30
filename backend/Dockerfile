# backend/Dockerfile

# 1. Imagen base con Python 3.11
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# 3. Instalar dependencias del sistema necesarias para OpenCV
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# 4. Copiar el archivo de requerimientos
COPY requirements.txt .

# Actualizar pip
RUN pip install --upgrade pip

# 5. Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el resto del código de la app (excluyendo data/ gracias a .dockerignore)
COPY . .

# 7. Copiar el script de entrada
COPY entrypoint.sh .

# 8. Establecer el script de entrada
ENTRYPOINT ["./entrypoint.sh"]

# 9. Exponer el puerto en el contenedor (5000 por defecto en Flask)
EXPOSE 5000

# 10. Comando por defecto para ejecutar Flask
CMD ["python", "app.py"]
