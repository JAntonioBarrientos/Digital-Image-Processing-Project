import React, { useState, useEffect } from 'react';

interface MosaicFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
  isProcessing: boolean;
}

const MosaicFilter: React.FC<MosaicFilterProps> = ({
  selectedImage,
  setImagePreview,
  setProcessedImageUrl,
  setIsProcessing,
  isProcessing,
}) => {
  const [blockWidth, setBlockWidth] = useState<number>(50);
  const [blockHeight, setBlockHeight] = useState<number>(50);
  const [upscaleFactor, setUpscaleFactor] = useState<number>(6);
  const [isBackendPreprocessing, setIsBackendPreprocessing] = useState<boolean>(false);

  useEffect(() => {
    const checkBackendStatus = async () => {
      try {
        const response = await fetch('http://localhost:5000/status');
        if (!response.ok) {
          throw new Error('Error al consultar el estado del backend');
        }
        const data = await response.json();
        setIsBackendPreprocessing(data.preprocessing);
      } catch (error) {
        console.error('Error al consultar el estado del backend:', error);
      }
    };

    checkBackendStatus();
    const interval = setInterval(checkBackendStatus, 5000); // Cada 5 segundos
    return () => clearInterval(interval);
  }, []);

  const applyFilter = async () => {
    if (isBackendPreprocessing) {
      alert('El backend está preprocesando la biblioteca de imágenes. Por favor, intenta de nuevo más tarde.');
      return;
    }

    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true);

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('block_width', blockWidth.toString());
    formData.append('block_height', blockHeight.toString());
    formData.append('upscale_factor', upscaleFactor.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-mosaic-filter', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al aplicar el filtro de Mosaico');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al aplicar el filtro de Mosaico:', error);
      alert('Hubo un error al aplicar el filtro. Por favor, intenta de nuevo con un valor mas pequeño de Upscale-Factor ó la reaplicación del filtro provocó una imagen muy grande.');
      alert('Reinicie la aplicación para intentar de nuevo.');
    } finally {
      setIsProcessing(false);
    }
  };

  const resetPreprocessing = async () => {
    setIsBackendPreprocessing(true); // Cambia a true mientras se reinicia el preprocesamiento
    try {
      const response = await fetch('http://localhost:5000/reset-preprocessing', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Error al reiniciar el preprocesamiento');
      }
      alert('Preprocesamiento reiniciado. El backend está procesando la biblioteca de imágenes.');
    } catch (error) {
      console.error('Error al reiniciar el preprocesamiento:', error);
      alert('Hubo un error al reiniciar el preprocesamiento. Por favor, intenta de nuevo.');
    }
  };

  return (
    <div>
      <h3>Aplicar Filtro de Mosaico</h3>

      {isBackendPreprocessing && (
        <div style={{ color: 'blue', marginBottom: '10px' }}>
          La biblioteca de imágenes está siendo preprocesada. Por favor, espera...
        </div>
      )}

      <label>
        <b>Upscale Factor (Aumento del tamaño de la imagen): {upscaleFactor}</b> <br />
        <input
          type="range"
          min="1"
          max="9"
          value={upscaleFactor}
          onChange={(e) => setUpscaleFactor(parseInt(e.target.value) || 1)}
          disabled={isBackendPreprocessing}
        />
        <b>Advertencia:</b> Valores altos pueden causar que la imagen <br />
        procesada sea muy grande y si no hay suficiente <br />
        memoria RAM libre el proceso se cancelará. <br />
      </label>
      <br />
      <label>
        <b>Tamaño del Bloque (Ancho en píxeles):</b>
        <input
          type="number"
          min="1"
          value={blockWidth}
          onChange={(e) => setBlockWidth(parseInt(e.target.value) || 1)}
          disabled={isBackendPreprocessing}
        />
      </label>
      <br />
      <label>
        <b>Tamaño del Bloque (Alto en píxeles):</b>
        <input
          type="number"
          min="1"
          value={blockHeight}
          onChange={(e) => setBlockHeight(parseInt(e.target.value) || 1)}
          disabled={isBackendPreprocessing}
        />
      </label>
      <br />
      <button onClick={applyFilter} disabled={isBackendPreprocessing || isProcessing}>
        {isProcessing ? 'Procesando' : 'Aplicar Filtro de Mosaico'}
      </button>
      <br />
      <b>En caso de haber agregado nuevas imagenes a la biblioteca:</b> <br />
      <button onClick={resetPreprocessing} disabled={isBackendPreprocessing}>
        Reiniciar Preprocesamiento
      </button>
    </div>
  );
};

export default MosaicFilter;
