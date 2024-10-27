import React, { useState } from 'react';

interface MinFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const MinFilter: React.FC<MinFilterProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  const [radius, setRadius] = useState<number>(1); // Estado para el radio del filtro mínimo

  const applyFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true); // Activar el mensaje de "Procesando imagen..."

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('radius', radius.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-min-filter', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al aplicar el filtro mínimo');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al aplicar el filtro mínimo:', error);
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }
  };

  return (
    <div>
      <h3>Aplicar Filtro Mínimo</h3>
      <label>
        Radio del Filtro: {radius}
        <input
          type="range"
          min="1"
          max="25"
          value={radius}
          onChange={(e) => setRadius(parseInt(e.target.value))}
        />
      </label>
      <button onClick={applyFilter}>Aplicar Filtro Mínimo</button>
    </div>
  );
};

export default MinFilter;
