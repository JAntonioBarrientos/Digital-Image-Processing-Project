import React, { useState } from 'react';

interface CustomDiagonalFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const CustomDiagonalFilter: React.FC<CustomDiagonalFilterProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  const [intensity, setIntensity] = useState<number>(1); // Estado para la intensidad del filtro diagonal

  const applyFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true); // Activar el mensaje de "Procesando imagen..."

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('intensity', intensity.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-custom-diagonal-filter', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al aplicar el filtro diagonal');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al aplicar el filtro diagonal:', error);
    } finally {
      setIsProcessing(false); 
    }
  };

  return (
    <div>
      <h3>Filtro Motion Blur</h3>
      <label>
        Intensidad del Filtro: {intensity}
        <input
          type="range"
          min="1"
          max="25"
          value={intensity}
          onChange={(e) => setIntensity(parseInt(e.target.value))}
        />
      </label>
      <button onClick={applyFilter}>Aplicar Filtro Motion Blur</button>
    </div>
  );
};

export default CustomDiagonalFilter;
