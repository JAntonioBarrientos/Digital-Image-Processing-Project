#!/bin/bash
set -e

# Ejecutar el script de inicialización para crear el .csv
echo "Ejecutando init_data.py para generar el CSV..."
python init_data.py

# Iniciar la aplicación Flask
echo "Iniciando la aplicación Flask..."
exec "$@"
