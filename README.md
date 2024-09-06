# Digital Image Processing Project - Versión Tarea 1

**Alumno:** José Antonio Barrientos Sánchez

**No. de Cuenta:** 423019269


Este proyecto es una aplicación web para el procesamiento digital de imágenes, construida utilizando **React** para el frontend y **Flask** para el backend. Permite a los usuarios cargar imágenes, aplicar filtros como escala de grises, filtros ponderados y más.

## Características

- Aplicación web construida con **React** y **Flask**.
- Soporte para varios filtros de procesamiento de imágenes.
- Desplegable usando **Docker** y **Docker Compose** para asegurar portabilidad.

## Requisitos

Antes de ejecutar este proyecto, asegúrate de tener instalados los siguientes componentes en tu máquina:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Clonar el repositorio

Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/JAntonioBarrientos/Digital-Image-Processing-Proyect.git

cd Digital-Image-Processing-Proyect

```

## Ejecutar el proyecto con Docker

Este proyecto está preparado para ejecutarse utilizando Docker Compose. Sigue los pasos a continuación para poner en marcha el frontend (React) y el backend (Flask) en contenedores de Docker.

1. Construir las imágenes de Docker
En el directorio raíz del proyecto, donde se encuentra el archivo docker-compose.yml, ejecuta el siguiente comando para construir las imágenes de Docker:

```bash
docker compose build
```

2. Iniciar los contenedores de Docker
Una vez que las imágenes de Docker se hayan construido correctamente, ejecuta el siguiente comando para iniciar los contenedores de Docker:

```bash
docker compose up
```

3. Acceder a la aplicación
Una vez que los contenedores de Docker se hayan iniciado correctamente, puedes acceder a la aplicación web en tu navegador web visitando la siguiente URL:

```
http://localhost:3000
```

## Detener los contenedores de Docker

Para detener los contenedores de Docker, ejecuta el siguiente comando en el directorio raíz del proyecto:

```bash
docker compose down
```


## Ejecución local sin Docker (opcional)

Si prefieres ejecutar el proyecto sin Docker, puedes seguir los pasos a continuación para ejecutar el frontend (React) y el backend (Flask) en tu máquina local.

### Frontend (React)

Primero, asegúrate de tener Node.js y npm instalados en tu máquina. Luego, sigue los pasos a continuación para ejecutar el frontend (React) en tu máquina local:

1. avega al directorio frontend/ en el proyecto:

```bash
cd frontend/
```

2. Instala las dependencias del frontend:

```bash

npm install
```

3. Inicia el servidor de desarrollo del frontend:

```bash
npm start
```
4. La aplicación web estará disponible en tu navegador web en la siguiente URL:

```
http://localhost:3000
```

### Ejecutar el backend (Flask)

Para ejecutar el backend (Flask) en tu máquina local, sigue los pasos a continuación:

1. Abre una nueva terminal y navega al directorio backend/ en el proyecto:

```bash
cd backend/
```

2. Crea un entorno virtual para el backend:

```bash
python3 -m venv venv
```

3. Activa el entorno virtual:

```bash
source venv/bin/activate
```

4. Instala las dependencias del backend:

```bash

pip install -r requirements.txt
```

5. Inicia el servidor del backend:

```bash
python app.py
```


## Implementación de filtros

La aplicación web admite varios filtros de procesamiento de imágenes que se pueden aplicar a las imágenes cargadas. Los filtros disponibles actualmente son:

- Escala de grises
- Escala de grises ponderada
- Efecto mica RGB

Los algoritmos fueron implementados desde cero en Python y se pueden encontrar en el directorio:

```
backend/models/filters
```

