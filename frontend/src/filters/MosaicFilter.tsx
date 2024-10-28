import React, { useState, useEffect } from 'react';

interface MosaicFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const MosaicFilter: React.FC<MosaicFilterProps> = ({
  selectedImage,
  setImagePreview,
  setProcessedImageUrl,
  setIsProcessing,
}) => {
  const [blockWidth, setBlockWidth] = useState<number>(50);
  const [blockHeight, setBlockHeight] = useState<number>(50);
  const [upscaleFactor, setUpscaleFactor] = useState<number>(4);

  useEffect(() => {
    // Si necesitas cargar datos al montar el componente, puedes hacerlo aquí
  }, []);

  const applyFilter = async () => {
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
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div>
      <h3>Aplicar Filtro de Mosaico</h3>
      <label>
        Factor de Ampliación (Upscale Factor):
        <input
          type="number"
          min="1"
          value={upscaleFactor}
          onChange={(e) => setUpscaleFactor(parseInt(e.target.value) || 1)}
        />
      </label>
      <br />
      <label>
        Tamaño del Bloque (Ancho en píxeles):
        <input
          type="number"
          min="1"
          value={blockWidth}
          onChange={(e) => setBlockWidth(parseInt(e.target.value) || 1)}
        />
      </label>
      <br />
      <label>
        Tamaño del Bloque (Alto en píxeles):
        <input
          type="number"
          min="1"
          value={blockHeight}
          onChange={(e) => setBlockHeight(parseInt(e.target.value) || 1)}
        />
      </label>
      <br />
      <button onClick={applyFilter}>Aplicar Filtro de Mosaico</button>
    </div>
  );
};

export default MosaicFilter;
