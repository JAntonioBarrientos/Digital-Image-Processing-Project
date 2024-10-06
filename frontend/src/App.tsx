import React, { useState } from 'react';
import './App.css';
import GrayscaleFilter from './filters/GrayscaleFilter';
import GrayFilterWeighted from './filters/GrayFilterWeighted';
import MicaFilter from './filters/MicaFilter';
import BlurFilter from './filters/BlurFilter'; // Filtro Blur
import CustomDiagonalFilter from './filters/CustomDiagonalFilter'; // Filtro Diagonal Personalizado
import FindEdgesFilter from './filters/FindEdgesFilter'; // Filtro Find Edges
import SharpenFilter from './filters/SharpenFilter'; // Importar filtro Sharpen
import EmbossFilter from './filters/EmbossFilter'; // Importar filtro Emboss
import MeanFilter from './filters/MeanFilter';
import RecursiveGrayFilter from './filters/RecursiveGrayFilter';
import RecursiveColorFilter from './filters/RecursiveColorFilter';
import WatermarkFilter from './filters/WatermarkFilter';
import WatermarkFilterDiagonal from './filters/WatermarkFilterDiagonal';



const App: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [processedImageUrl, setProcessedImageUrl] = useState<string | null>(null);
  const [selectedFilter, setSelectedFilter] = useState<string | null>(null); // Filtro seleccionado
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null); // Categorías
  const [isProcessing, setIsProcessing] = useState<boolean>(false); // Estado de procesamiento
  const [isSidebarVisible, setIsSidebarVisible] = useState<boolean>(true); // Controla la visibilidad de la barra lateral

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

  // Función para alternar la visibilidad de la barra lateral
  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible);
  };

  return (
    <div className="app">
      {/* Botón para retraer o mostrar la barra lateral */}
      <button className="toggle-button" onClick={toggleSidebar}>
        {isSidebarVisible ? '<<' : '>>'}
      </button>

      {/* Barra lateral izquierda (retraíble) */}
      <aside className={`sidebar ${isSidebarVisible ? '' : 'retracted'}`}>
        <h2>Filtros</h2>
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

        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea2' ? null : 'tarea2')}>
            Tarea 2
          </div>
          {expandedCategory === 'tarea2' && (
            <ul>
              <li onClick={() => setSelectedFilter('blur')}>Filtro de Blur</li>
              <li onClick={() => setSelectedFilter('custom-diagonal')}>Filtro Motion Blur</li>
              <li onClick={() => setSelectedFilter('find-edges')}>Filtro Find Edges</li>
              <li onClick={() => setSelectedFilter('sharpen')}>Filtro Sharpen</li>
              <li onClick={() => setSelectedFilter('emboss')}>Filtro Emboss</li>
              <li onClick={() => setSelectedFilter('mean')}>Filtro Promedio</li>
            </ul>
          )}
        </div>

        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea3' ? null : 'tarea3')}>
            Tarea 3
          </div>
          {expandedCategory === 'tarea3' && (
            <ul>
              <li onClick={() => setSelectedFilter('recursive-gray')}>Imagen recursiva escala de grises</li>
              <li onClick={() => setSelectedFilter('recursive-color')}>Imagen recursiva a color real</li>
            </ul>
          )}
        </div>
        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea4' ? null : 'tarea4')}>
            Tarea 4
          </div>
          {expandedCategory === 'tarea4' && (
            <ul>
              <li onClick={() => setSelectedFilter('watermark')}>Marca de agua</li>
              <li onClick={() => setSelectedFilter('watermark-diagonal')}>Marca de agua diagonal</li>
            </ul>
          )}
        </div>
      </aside>

      {/* Contenido principal */}
      <main className={`main-content ${isSidebarVisible ? '' : 'expanded'}`}>
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

          {/* Previsualización de la imagen seleccionada */}
          {imagePreview && (
            <div className="image-preview">
              <img src={imagePreview} alt="Previsualización" />
            </div>
          )}

          {/* Mostrar el mensaje de procesamiento si está en proceso */}
          {isProcessing && <p>Procesando imagen...</p>}

          {/* Mostrar el botón del filtro seleccionado */}
          <div className="button-group">
            {selectedImage && selectedFilter === 'grayscale' && (
              <GrayscaleFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'gray-weighted' && (
              <GrayFilterWeighted
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'mica' && (
              <MicaFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'blur' && (
              <BlurFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'custom-diagonal' && (
              <CustomDiagonalFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'find-edges' && (
              <FindEdgesFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'sharpen' && (  
              <SharpenFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'emboss' && (
              <EmbossFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'mean' && (
              <MeanFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'recursive-gray' && (
              <RecursiveGrayFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'recursive-color' && (
              <RecursiveColorFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'watermark' && (
              <WatermarkFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'watermark-diagonal' && (
              <WatermarkFilterDiagonal
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            
            {/* Botón para descargar la imagen procesada */}
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
