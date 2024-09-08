import React, { useState } from 'react';

interface BlurFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const BlurFilter: React.FC<BlurFilterProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  const [blurIntensity, setBlurIntensity] = useState<number>(1); // Estado para la intensidad del blur

  const applyFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true); // Activar el mensaje de "Procesando imagen..."

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('intensity', blurIntensity.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-blur', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al aplicar el filtro de Blur');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al aplicar el filtro de Blur:', error);
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }
  };

  return (
    <div>
      <h3>Aplicar Filtro de Blur</h3>
      <label>
        Intensidad del Blur: {blurIntensity}
        <input
          type="range"
          min="1"
          max="25"
          value={blurIntensity}
          onChange={(e) => setBlurIntensity(parseInt(e.target.value))}
        />
      </label>
      <button onClick={applyFilter}>Aplicar Filtro de Blur</button>
    </div>
  );
};

export default BlurFilter;
