import React, { useState } from 'react';

interface MicaFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void; 
}

const MicaFilter: React.FC<MicaFilterProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  const [rValue, setRValue] = useState<number>(255); // Valor inicial para R
  const [gValue, setGValue] = useState<number>(255); // Valor inicial para G
  const [bValue, setBValue] = useState<number>(255); // Valor inicial para B

  // Función para aplicar el filtro de mica
  const applyMicaFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true);

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('r_value', rValue.toString());
    formData.append('g_value', gValue.toString());
    formData.append('b_value', bValue.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-mica-filter', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al aplicar el filtro');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al aplicar el filtro:', error);
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }

  };

  return (
    <div>
      <h3>Aplicar Filtro Mica</h3>
      <div>
        <label>
          R ({rValue}):
          <input
            type="range"
            value={rValue}
            onChange={(e) => setRValue(parseInt(e.target.value))}
            min="0"
            max="255"
            style={{ width: '100%' }} // Ajusta el ancho del slider
          />
        </label>
        <label>
          G ({gValue}):
          <input
            type="range"
            value={gValue}
            onChange={(e) => setGValue(parseInt(e.target.value))}
            min="0"
            max="255"
            style={{ width: '100%' }} // Ajusta el ancho del slider
          />
        </label>
        <label>
          B ({bValue}):
          <input
            type="range"
            value={bValue}
            onChange={(e) => setBValue(parseInt(e.target.value))}
            min="0"
            max="255"
            style={{ width: '100%' }} // Ajusta el ancho del slider
          />
        </label>
      </div>
      <button onClick={applyMicaFilter}>Aplicar Filtro Mica</button>
    </div>
  );
};

export default MicaFilter;
