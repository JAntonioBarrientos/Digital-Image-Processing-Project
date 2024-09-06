import React, { useState } from 'react';
import './App.css';
import GrayscaleFilter from './filters/GrayscaleFilter';
import GrayFilterWeighted from './filters/GrayFilterWeighted';
import MicaFilter from './filters/MicaFilter';

const App: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [processedImageUrl, setProcessedImageUrl] = useState<string | null>(null);
  const [selectedFilter, setSelectedFilter] = useState<string | null>(null); // Estado para el filtro seleccionado
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null); // Estado para las categorías desplegables

  // Función para manejar la carga de imágenes
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  // Función para descargar la imagen procesada
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
      {/* Barra lateral izquierda para los filtros */}
      <aside className="sidebar">
        <h2>Filtros</h2>

        {/* Categoría de Tarea 1 */}
        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea1' ? null : 'tarea1')}>
            Tarea 1
          </div>
          {expandedCategory === 'tarea1' && (
            <ul>
              <li onClick={() => setSelectedFilter('grayscale')}>Escala de Grises</li>
              <li onClick={() => setSelectedFilter('gray-weighted')}>Filtro Ponderado</li>
              <li onClick={() => setSelectedFilter('mica')}>Filtro Mica</li>
            </ul>
          )}
        </div>

        {/* Otras categorías que puedes añadir en el futuro */}
        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea2' ? null : 'tarea2')}>
            Tarea 2
          </div>
          {expandedCategory === 'tarea2' && (
            <ul>
              <li>Filtro de Blur</li>
              <li>Filtro de Sharpen</li>
            </ul>
          )}
        </div>

        {/* Añadir más categorías aquí */}
      </aside>

      {/* Área principal para la previsualización de la imagen */}
      <main className="main-content">
        <div className="image-preview-container">
          <h2>Previsualización</h2>
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
              <img src={imagePreview} alt="Preview" />
            </div>
          )}

          {/* Mostrar botón de filtro seleccionado */}
          <div className="button-group">
            {selectedImage && selectedFilter === 'grayscale' && (
              <GrayscaleFilter selectedImage={selectedImage} setImagePreview={setImagePreview} setProcessedImageUrl={setProcessedImageUrl} />
            )}
            {selectedImage && selectedFilter === 'gray-weighted' && (
              <GrayFilterWeighted selectedImage={selectedImage} setImagePreview={setImagePreview} setProcessedImageUrl={setProcessedImageUrl} />
            )}
            {selectedImage && selectedFilter === 'mica' && (
              <MicaFilter selectedImage={selectedImage} setImagePreview={setImagePreview} setProcessedImageUrl={setProcessedImageUrl} />
            )}

            {processedImageUrl && (
              <button onClick={downloadImage} className="download-button">
                Descargar Imagen Procesada
              </button>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
