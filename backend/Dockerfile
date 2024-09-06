# 1. Imagen base con Python
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos
COPY requirements.txt .

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código de la app
COPY . .

# 6. Exponer el puerto en el contenedor (5000 por defecto en Flask)
EXPOSE 5000

# 7. Comando por defecto para ejecutar Flask
CMD ["python", "app.py"]
