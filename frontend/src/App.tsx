import React, { useState } from 'react';
import './App.css';
import FiltrosTarea1 from './components/FiltrosTarea1';
import FiltrosTarea2 from './components/FiltrosTarea2';
import FiltrosTarea3 from './components/FiltrosTarea3';
import FiltrosTarea4 from './components/FiltrosTarea4';

const App: React.FC = () => {
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);

  // Función para manejar la expansión y contracción de categorías
  const toggleCategory = (category: string) => {
    setExpandedCategory(expandedCategory === category ? null : category);
  };

  // Función para manejar la subida de imágenes
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedImage(event.target.files[0]);
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <ul>
          <FiltrosTarea1
            expanded={expandedCategory === 'Filtros Tarea 1'}
            toggleCategory={() => toggleCategory('Filtros Tarea 1')}
          />
          <FiltrosTarea2
            expanded={expandedCategory === 'Filtros Tarea 2'}
            toggleCategory={() => toggleCategory('Filtros Tarea 2')}
          />
          <FiltrosTarea3
            expanded={expandedCategory === 'Filtros Tarea 3'}
            toggleCategory={() => toggleCategory('Filtros Tarea 3')}
          />
          <FiltrosTarea4
            expanded={expandedCategory === 'Filtros Tarea 4'}
            toggleCategory={() => toggleCategory('Filtros Tarea 4')}
          />
        </ul>
      </aside>
      <main className="content">
        <h1>Procesamiento Digital de Imágenes</h1>
        <div className="upload-section">
          <label htmlFor="file-upload" className="custom-file-upload">
            Cargar Imagen
          </label>
          <input
            id="file-upload"
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            style={{ display: 'none' }} // Ocultamos el input real y usamos un botón personalizado
          />
        </div>
        {selectedImage && (
          <div className="image-preview">
            <h3>Imagen seleccionada:</h3>
            <img src={URL.createObjectURL(selectedImage)} alt="Selected" />
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
