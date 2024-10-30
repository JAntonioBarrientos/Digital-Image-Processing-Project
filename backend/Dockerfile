# 1. Imagen base con Python 3.11
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos
COPY requirements.txt .

# Actualizar pip
RUN pip install --upgrade pip

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código de la app
COPY . .

# 7. Ejecutar el script de inicialización para crear el .csv
RUN python init_data.py

# 8. Exponer el puerto en el contenedor (5000 por defecto en Flask)
EXPOSE 5000

# 9. Comando por defecto para ejecutar Flask
CMD ["python", "app.py"]
