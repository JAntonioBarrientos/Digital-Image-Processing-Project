# High-Performance Image Processing API  

A robust web application and REST API designed for digital image processing. This project features a collection of custom-implemented algorithms optimized for performance using vectorization and multiprocessing.

## Key Features

- Custom Algorithm Implementation: Core image filters and processing logic built from scratch using NumPy and OpenCV for low-level data handling.

- Optimized Performance: Leverages Python's multiprocessing for parallel execution and vectorization to handle large image matrices efficiently.

- Modern Web Interface: Clean and responsive UI built with React.

## Tech Stack
- Backend: Python, Flask, NumPy, OpenCV.

- Frontend: React, JavaScript (ES6+).

- DevOps: Docker, Docker Compose.


## Implementation Details

Every filter includes detailed documentation, including pseudocode and logic explanations. You can explore the core implementations in the documentacion-implementacion/ directory:

Main Project: Mosaic Filter

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation & Deployment

### Clone the repository:

```bash
git clone https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project.git

cd Digital-Image-Processing-Project

```



### Setup Mosaic Library(Optional)
If you wish to use the Mosaic filter, place your source image library in:
    
```
     backend/models/data/image_library/
```

### Run with Docker


Launch the entire stack (Frontend + Backend) with a single command:

```bash
docker compose up --build
```
### Access the App
Open your browser and navigate to:

```
http://localhost:3000
```


## Manual Setup (Development Mode)
If you prefer to run the components separately without Docker:

### Backend (Flask)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

### Frontend (React)

```bash
cd frontend
npm install
npm start
```


## Optimization Note

The core of this project focuses on reducing computational time. By replacing standard nested loops with NumPy vectorization, we achieved significant speedups in matrix manipulation, while the Multiprocessing module ensures that CPU-intensive filters utilize all available cores.


## License
Distributed under the MIT License. See LICENSE for more information.
