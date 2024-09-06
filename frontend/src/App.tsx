import React, { useState } from 'react';
import './App.css';
import FiltrosTarea1 from './components/FiltrosTarea1';
import FiltrosTarea2 from './components/FiltrosTarea2';
import FiltrosTarea3 from './components/FiltrosTarea3';
import FiltrosTarea4 from './components/FiltrosTarea4';
import GrayscaleFilter from './filters/GrayscaleFilter';
import GrayFilterWeighted from './filters/GrayFilterWeighted';

const App: React.FC = () => {
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [processedImageUrl, setProcessedImageUrl] = useState<string | null>(null);

  const toggleCategory = (category: string) => {
    setExpandedCategory(expandedCategory === category ? null : category);
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const downloadImage = () => {
    if (processedImageUrl) {
      const link = document.createElement('a');
      link.href = processedImageUrl;
      link.download = 'imagen_procesada.jpg';
      link.click();
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <ul>
          <FiltrosTarea1 expanded={expandedCategory === 'Filtros Tarea 1'} toggleCategory={() => toggleCategory('Filtros Tarea 1')} />
          <FiltrosTarea2 expanded={expandedCategory === 'Filtros Tarea 2'} toggleCategory={() => toggleCategory('Filtros Tarea 2')} />
          <FiltrosTarea3 expanded={expandedCategory === 'Filtros Tarea 3'} toggleCategory={() => toggleCategory('Filtros Tarea 3')} />
          <FiltrosTarea4 expanded={expandedCategory === 'Filtros Tarea 4'} toggleCategory={() => toggleCategory('Filtros Tarea 4')} />
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
            style={{ display: 'none' }}
          />
        </div>
        {imagePreview && (
          <div className="image-preview">
            <h3>Vista previa:</h3>
            <img src={imagePreview} alt="Preview" />
          </div>
        )}
        {selectedImage && (
          <div>
            <GrayscaleFilter selectedImage={selectedImage} setImagePreview={setImagePreview} setProcessedImageUrl={setProcessedImageUrl} />
            <GrayFilterWeighted selectedImage={selectedImage} setImagePreview={setImagePreview} setProcessedImageUrl={setProcessedImageUrl} />
          </div>
        )}
        {processedImageUrl && (
          <button onClick={downloadImage} style={{ marginTop: '10px' }}>
            Descargar Imagen Procesada
          </button>
        )}
      </main>
    </div>
  );
};

export default App;
