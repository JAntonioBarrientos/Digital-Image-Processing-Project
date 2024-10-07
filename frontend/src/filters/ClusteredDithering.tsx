import { error } from 'console';
import React, { useState } from 'react';

interface ClusteredDitheringProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const ClusteredDithering: React.FC<ClusteredDitheringProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  // Valores por defecto para los inputs
  const [errorMessage, setErrorMessage] = useState<string | null>(null);  // Estado para el mensaje de error

  // Función para aplicar el filtro de imagen recursiva en escala de grises
  const applyClusteredDithering = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await fetch('http://localhost:5000/apply-clustered-dithering', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        setErrorMessage(errorData.error);
        alert('Error al aplicar el filtro');
        throw new Error('Error al aplicar el filtro');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl); // Previsualizar imagen procesada
      setProcessedImageUrl(imageUrl); // Guardar la URL de la imagen procesada
    } catch (error) {
      console.error('Error al aplicar el filtro:', error);
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }
  };

  return (
    <div>
      {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}
      <button onClick={applyClusteredDithering}>Aplicar Dithering ordenado</button>
    </div>
  );
};

export default ClusteredDithering;
