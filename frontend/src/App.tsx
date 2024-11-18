import React, { useState, useEffect } from 'react';
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
import RemoveRedWatermarkFilter from './filters/RemoveRedWatermarkFilter';
import HalftoneFilter from './filters/HalftoneFilter';
import RandomDithering from './filters/RandomDithering';
import ClusteredDithering from './filters/ClusteredDithering';
import DispersedDithering from './filters/DispersedDithering';
import FloydSteinberg from './filters/FloydSteinberg';
import OleoFilter from './filters/OleoFilter';
import MinFilter from './filters/MinFilter';
import MaxFilter from './filters/MaxFilter';
import MosaicFilter from './filters/MosaicFilter';
import ResizeFilter from './filters/ResizeFilter';
import ImagenConMsGrises from './filters/ImagenConMsGrises';
import ImagenConMsColor from './filters/ImagenConMsColor';
import ImagenConLetrasDistintosGrises from './filters/ImagenConLetrasDistintosGrises';
import ImagenConLetrasDistintosColor from './filters/ImagenConLetrasDistintosColor';


const App: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [originalImage, setOriginalImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [processedImageUrl, setProcessedImageUrl] = useState<string | null>(null);
  const [selectedFilter, setSelectedFilter] = useState<string | null>(null);
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [isSidebarVisible, setIsSidebarVisible] = useState<boolean>(true);
  const [currentImage, setCurrentImage] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const documentationLinks: { [key: string]: { name: string; url: string } } = {
    'documentation-tarea1': {
      name: 'Tarea 1',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Tarea1.md',
    },
    'documentation-tarea2': {
      name: 'Tarea 2',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Tarea2.md',
    },
    'documentation-tarea3': {
      name: 'Tarea 3',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Tarea3.md',
    },
    'documentation-tarea4': {
      name: 'Tarea 4',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Tarea4.md',
    },
    'documentation-tarea5': {
      name: 'Tarea 5',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Tarea5.md',
    },
    'documentation-tarea6': {
      name: 'Tarea 6',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Tarea6.md',
    },
    'documentation-tarea7': {
      name: 'Tarea 7',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Tarea7.md',
    },
    'documentation-tarea8': {
      name: 'Tarea 8',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Tarea8.md',
    },
    'documentation-tarea9': {
      name: 'Tarea 9',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Tarea9.md',
    },
    'documentation-proyecto': {
      name: 'Proyecto',
      url: 'https://github.com/JAntonioBarrientos/Digital-Image-Processing-Project/tree/main/documentacion-implementacion/Proyecto.md',
    },
  };

    // useEffect para actualizar selectedImage cuando processedImageUrl cambia
    useEffect(() => {
      const updateSelectedImage = async () => {
        if (processedImageUrl) {
          try {
            const response = await fetch(processedImageUrl);
            const blob = await response.blob();
            const file = new File([blob], 'processed_image.jpg', { type: blob.type });
            setSelectedImage(file);
            setCurrentImage(file);
          } catch (error) {
            console.error('Error al convertir la URL a File:', error);
          }
        }
      };
  
      updateSelectedImage();
    }, [processedImageUrl]);
  

  // Función para descargar la imagen procesada
  const downloadImage = () => {
    if (processedImageUrl) {
      const link = document.createElement('a');
      link.href = processedImageUrl;
      link.download = 'imagen_procesada.jpg';
      link.click();
    }
  };

  // Función para manejar la carga de imágenes
    const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
      if (event.target.files && event.target.files[0]) {
        const file = event.target.files[0];
        setSelectedImage(file);
        setOriginalImage(file); // Establecer la imagen original
        setImagePreview(URL.createObjectURL(file));
        setCurrentImage(file); // Establecer la imagen actual como la imagen cargada
        setProcessedImageUrl(null); // Reiniciar la imagen procesada
      }
    };

  // Función para alternar la visibilidad de la barra lateral
  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible);
  };

  // Función para reiniciar la imagen a la original
    const resetImage = () => {
      if (originalImage) {
        setSelectedImage(originalImage);
        setCurrentImage(originalImage);
        setImagePreview(URL.createObjectURL(originalImage));
        setProcessedImageUrl(null);
        setSelectedFilter(null); // Opcional: deseleccionar el filtro actual
      }
    };

    
    // Limpieza de URLs de objetos para evitar fugas de memoria
    useEffect(() => {
      return () => {
        if (imagePreview) {
          URL.revokeObjectURL(imagePreview);
        }
        if (processedImageUrl) {
          URL.revokeObjectURL(processedImageUrl);
        }
      };
    }, [imagePreview, processedImageUrl]);


  // Función para capitalizar la primera letra (e.g., 'tarea1' -> 'Tarea1')
  const capitalize = (s: string) => {
    if (typeof s !== 'string') return '';
    return s.charAt(0).toUpperCase() + s.slice(1);
  };

  // Actualización del selectedImage solo si processedImageUrl es una imagen
  useEffect(() => {
    const updateSelectedImage = async () => {
      if (processedImageUrl) {
        // Definir una lista de extensiones de imagen
        const imageExtensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif'];
        const isImage = imageExtensions.some(ext => processedImageUrl.toLowerCase().endsWith(ext));

        if (isImage) {
          try {
            const response = await fetch(processedImageUrl);
            const blob = await response.blob();
            const file = new File([blob], 'processed_image.jpg', { type: blob.type });
            setSelectedImage(file);
            setCurrentImage(file);
          } catch (error) {
            console.error('Error al convertir la URL a File:', error);
          }
        }
        // Si no es una imagen, no hacer nada
      }
    };

    updateSelectedImage();
  }, [processedImageUrl]);


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
              <li onClick={() => setSelectedFilter('documentation-tarea1')}>Documentación</li>
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
              <li onClick={() => setSelectedFilter('documentation-tarea2')}>Documentación</li>
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
              <li onClick={() => setSelectedFilter('documentation-tarea3')}>Documentación</li>
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
              <li onClick={() => setSelectedFilter('remove-red-watermark')}>Eliminar marca de agua roja</li>
              <li onClick={() => setSelectedFilter('documentation-tarea4')}>Documentación</li>
            </ul>
          )}
        </div>
        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea5' ? null : 'tarea5')}>
            Tarea 5
          </div>
          {expandedCategory === 'tarea5' && (
            <ul>
              <li onClick={() => setSelectedFilter('halftone')}>Semitonos</li>
              <li onClick={() => setSelectedFilter('random-dithering')}>Dithering azar</li>
              <li onClick={() => setSelectedFilter('clustered-dithering')}>Dithering ordenado</li>
              <li onClick={() => setSelectedFilter('dispersed-dithering')}>Dithering disperso</li>
              <li onClick={() => setSelectedFilter('floyd-steinberg')}>Dithering Floyd-Steinberg</li>
              <li onClick={() => setSelectedFilter('documentation-tarea5')}>Documentación</li>
            </ul>
          )}
        </div>
        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea6' ? null : 'tarea6')}>
            Tarea 6
          </div>
          {expandedCategory === 'tarea6' && (
            <ul>
              <li onClick={() => setSelectedFilter('oleo')}>Filtro Oleo</li>
              <li onClick={() => setSelectedFilter('documentation-tarea6')}>Documentación</li>
            </ul>
          )}
        </div>
        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea7' ? null : 'tarea7')}>
            Tarea 7
          </div>
          {expandedCategory === 'tarea7' && (
            <ul>
              <li onClick={() => setSelectedFilter('min')}>Filtro erosion Minimo</li>
              <li onClick={() => setSelectedFilter('max')}>Filtro erosion Máximo</li> 
              <li onClick={() => setSelectedFilter('documentation-tarea7')}>Documentación</li>
            </ul>
          )}
        </div>
        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea8' ? null : 'tarea8')}>
            Tarea 8
          </div>
          {expandedCategory === 'tarea8' && (
            <ul>
              <li onClick={() => setSelectedFilter('resize')}>Escalar imagen</li>
              <li onClick={() => setSelectedFilter('documentation-tarea8')}>Documentación</li>
            </ul>
          )}
        </div>
        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'tarea9' ? null : 'tarea9')}>
            Tarea 9
          </div>
          {expandedCategory === 'tarea9' && (
            <ul>
              <li onClick={() => setSelectedFilter('letras-m-gris')}>Imagenes con M's tonos de gris</li>
              <li onClick={() => setSelectedFilter('letras-m-color')}>Imagenes con M's a color</li>
              <li onClick={() => setSelectedFilter('letras-con-distintos-gris')}>Imagenes con 'MNH#QUAD0Y2$%+. ' tonos de gris</li>
              <li onClick={() => setSelectedFilter('letras-con-distintos-color')}>Imagenes con 'MNH#QUAD0Y2$%+. ' a color</li>
              <li onClick={() => setSelectedFilter('documentation-tarea9')}>Documentación</li>
            </ul>
          )}
        </div>

        <div className="category">
          <div className="category-header" onClick={() => setExpandedCategory(expandedCategory === 'proyecto' ? null : 'proyecto')}>
            Proyecto
          </div>
          {expandedCategory === 'proyecto' && (
            <ul>
              <li onClick={() => setSelectedFilter('mosaicos')}>Filtro Mosaicos</li>
              <li onClick={() => setSelectedFilter('documentation-proyecto')}>Documentación</li>
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
            {selectedImage && selectedFilter === 'remove-red-watermark' && (
              <RemoveRedWatermarkFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'halftone' && (
              <HalftoneFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}  
            {selectedImage && selectedFilter === 'random-dithering' && (
              <RandomDithering
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'clustered-dithering' && (
              <ClusteredDithering
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'dispersed-dithering' && (
              <DispersedDithering
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'floyd-steinberg' && (
              <FloydSteinberg
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'oleo' && (
              <OleoFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'min' && (
              <MinFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'max' && (
              <MaxFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'mosaicos' && (
              <MosaicFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
                isProcessing={isProcessing} // Pasar isProcessing como prop
              />
            )}
            {selectedImage && selectedFilter === 'resize' && (
              <ResizeFilter
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {/* Componente para el filtro Letras M en Gris */}
            {originalImage && selectedFilter === 'letras-m-gris' && (
              <ImagenConMsGrises
                selectedImage={originalImage} // Pasar la imagen original
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}

            {selectedImage && selectedFilter === 'letras-m-color' && (
              <ImagenConMsColor
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'letras-con-distintos-gris' && (
              <ImagenConLetrasDistintosGrises
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}
            {selectedImage && selectedFilter === 'letras-con-distintos-color' && (
              <ImagenConLetrasDistintosColor
                selectedImage={selectedImage}
                setImagePreview={setImagePreview}
                setProcessedImageUrl={setProcessedImageUrl}
                setIsProcessing={setIsProcessing}
              />
            )}


            {/* Botón para reiniciar la imagen a la original */}
            {originalImage && (
              <button onClick={resetImage} className="reset-button">
                Reiniciar Imagen
              </button>
            )}

            {/* Botón para descargar la imagen procesada */}
            {processedImageUrl && (
              <button onClick={downloadImage} className="download-button">
                Descargar Imagen
              </button>
            )}

          {/* Sección de Documentación Siempre Desplegable */}
          {selectedFilter && selectedFilter.startsWith('documentation') && documentationLinks[selectedFilter] && (
            <div className="documentation-section">
              <h3>Documentación de {documentationLinks[selectedFilter].name}</h3>
              <div className="documentation-content">
                <p>Esta sección contiene la explicación del filtro correspondiente.</p>
                <a href={documentationLinks[selectedFilter].url} target="_blank" rel="noopener noreferrer">
                  Ver documentación en GitHub
                </a>
              </div>
            </div>
          )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
