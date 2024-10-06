import React, { useState, useRef, useEffect } from 'react';

interface WatermarkFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const WatermarkFilter: React.FC<WatermarkFilterProps> = ({ 
  selectedImage, 
  setImagePreview, 
  setProcessedImageUrl, 
  setIsProcessing 
}) => {
  const [text, setText] = useState<string>('© Marca de Agua'); // Texto inicial de la marca de agua
  const [xCoord, setXCoord] = useState<number>(50); // Coordenada X inicial
  const [yCoord, setYCoord] = useState<number>(50); // Coordenada Y inicial
  const [alpha, setAlpha] = useState<number>(0.5); // Transparencia inicial
  const [fontSize, setFontSize] = useState<number>(100); // Tamaño de fuente inicial
  const [errorMessage, setErrorMessage] = useState<string | null>(null);  // Estado para el mensaje de error
  const imageRef = useRef<HTMLImageElement | null>(null); // Referencia para la imagen

  // Función para aplicar el filtro de marca de agua
  const applyWatermarkFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true);
    setErrorMessage(null); // Reiniciar mensaje de error al comenzar

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('text', text);
    formData.append('x_coord', xCoord.toString());
    formData.append('y_coord', yCoord.toString());
    formData.append('alpha', alpha.toString());
    formData.append('font_size', fontSize.toString()); // Añadir el tamaño de la fuente

    try {
      const response = await fetch('http://localhost:5000/apply-watermark-filter', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        setErrorMessage(errorData.error);  // Mostrar el error del servidor
        alert('Error al aplicar el filtro');
        throw new Error('Error al aplicar el filtro');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl); // Previsualizar imagen procesada
      setProcessedImageUrl(imageUrl); // Guardar la URL de la imagen procesada
    } catch (error) {
      console.error('Error al aplicar el filtro de marca de agua:', error);
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }
  };

  // Detectar cambios en xCoord y yCoord y aplicar el filtro
  useEffect(() => {
    if (selectedImage) {
      applyWatermarkFilter();
    }
  }, [xCoord, yCoord]); // Ejecutar cuando cambian las coordenadas

  // Función para manejar el clic en la imagen y actualizar las coordenadas
  const handleImageClick = (event: React.MouseEvent<HTMLImageElement>) => {
    if (imageRef.current) {
      const rect = imageRef.current.getBoundingClientRect();
      const x = event.clientX - rect.left; // Coordenada X relativa a la imagen
      const y = event.clientY - rect.top;  // Coordenada Y relativa a la imagen

      setXCoord(Math.floor(x)); // Actualizar coordenada X
      setYCoord(Math.floor(y)); // Actualizar coordenada Y
    }
  };

  return (
    <div>
      <h3>Aplicar Marca de Agua</h3>
      <div>
        <label>
          Texto:
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={{ width: '100%' }}
          />
        </label>
      </div>
      <div>
        <label>
          Coordenada X ({xCoord}):
          <input
            type="number"
            value={xCoord}
            readOnly
            style={{ width: '25%' }}
          />
        </label>
        <label>
          Coordenada Y ({yCoord}):
          <input
            type="number"
            value={yCoord}
            readOnly
            style={{ width: '25%' }}
          />
        </label>
      </div>
      <div>
        <label>
          Transparencia ({alpha}):
          <input
            type="range"
            value={alpha}
            onChange={(e) => setAlpha(parseFloat(e.target.value))}
            min="0"
            max="1"
            step="0.01"
            style={{ width: '50%' }}
          />
        </label>
      </div>
      <div>
        <label>
          Tamaño de fuente ({fontSize}px):
          <input
            type="number"
            value={fontSize}
            onChange={(e) => setFontSize(parseInt(e.target.value))}
            style={{ width: '25%' }}
          />
        </label>
      </div>

      {/* Mostrar el mensaje de error si hay alguno */}
      {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}

      {/* Previsualizar la imagen y manejar el clic */}
      {selectedImage && (
        <div style={{ marginTop: '20px' }}>
          <img
            ref={imageRef}
            src={URL.createObjectURL(selectedImage)}
            alt="Imagen seleccionada"
            onClick={handleImageClick}
            style={{ maxWidth: '100%', cursor: 'pointer' }}
          />
          <p style={{
            marginTop: '10px',
            color: '#007bff',
            fontWeight: 'bold',
            fontSize: '18px',
            textShadow: '1px 1px 2px rgba(0,0,0,0.2)',
            }}>
            Haz clic en la imagen para colocar la marca de agua y aplicar el filtro.
            </p>
        </div>
      )}
      
    </div>
  );
};

export default WatermarkFilter;
