# Digital Image Processing Project  

**Alumno:** José Antonio Barrientos Sánchez

**No. de Cuenta:** 423019269

Este proyecto es una aplicación web para el procesamiento digital de imágenes del curso de Procesamiento Digital de Imágenes de la Facultad de Ciencias UNAM semestre 2025-1.

## Características

- Aplicación web construida con **React** y **Flask**.
- Desplegable usando **Docker** y **Docker Compose** para asegurar portabilidad.
- Optimizado para rendimiento utilizando **multiprocessing** y **vectorización** en Python.

## Requisitos

Antes de ejecutar este proyecto, asegúrate de tener instalados los siguientes componentes en tu máquina:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Clonar el repositorio

Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project.git

cd Digital-Image-Processing-Project

```

## Incluir imagenes para FILTRO MOSAICO (PROYECTO)

Las imagenes con las que se alimenta el filtro mosaico se deben colocar en la carpeta:
    
```
     backend/models/data/image_library/
```

Para mas información sobre el filtro mosaico, revisar el archivo:

[documentacion-implementacion/Proyecto.md](documentacion-implementacion/Proyecto.md)


## Ejecutar el proyecto con Docker

Este proyecto está preparado para ejecutarse utilizando Docker Compose. Sigue los pasos a continuación para poner en marcha el frontend (React) y el backend (Flask) en contenedores de Docker.

En el directorio raíz del proyecto, donde se encuentra el archivo docker-compose.yml, ejecuta el siguiente comando para construir las imágenes de Docker e iniciar los contenedores:

```bash
docker compose up --build
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

1. Navega al directorio frontend/ en el proyecto:

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

Los algoritmos fueron implementados desde cero en Python apoyandonos de operaciones vectorizadas y multiprocessing para mejorar el rendimiento de los filtros incluidas en las librerías de Python como OpenCV y Numpy.

La explicación detallada de cada filtro, su pseudocódigo y su implementación en Python se encuentra en la carpeta: `documentacion-implementacion/`

- [documentacion-implementacion/Proyecto.md](documentacion-implementacion/Proyecto.md)

- [documentacion-implementacion/Tarea1.md](documentacion-implementacion/Tarea1.md)

- [documentacion-implementacion/Tarea2.md](documentacion-implementacion/Tarea2.md)

- [documentacion-implementacion/Tarea3.md](documentacion-implementacion/Tarea3.md)

- [documentacion-implementacion/Tarea4.md](documentacion-implementacion/Tarea4.md)

- [documentacion-implementacion/Tarea5.md](documentacion-implementacion/Tarea5.md)

- [documentacion-implementacion/Tarea6.md](documentacion-implementacion/Tarea6.md)

- [documentacion-implementacion/Tarea7.md](documentacion-implementacion/Tarea7.md)

- [documentacion-implementacion/Tarea8.md](documentacion-implementacion/Tarea8.md)

- [documentacion-implementacion/Tarea9.md](documentacion-implementacion/Tarea9.md)


La aplicación web admite varios filtros de procesamiento de imágenes que se pueden aplicar a las imágenes cargadas. Los filtros disponibles actualmente son:

- Imagenes recursivas en escala de grises
- Imagenes recursivas en escala de grises ponderada
- Crear marcas de agua
- Dithering
- Filtro Oleo a blanco y negro y color
- Filtro de Erosión, máximo y mínimo.

