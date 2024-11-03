import React, { useState } from 'react';

interface RemoveRedWatermarkFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const RemoveRedWatermarkFilter: React.FC<RemoveRedWatermarkFilterProps> = ({
  selectedImage,
  setImagePreview,
  setProcessedImageUrl,
  setIsProcessing,
}) => {
  const [sensitivity, setSensitivity] = useState<number>(100); // Estado para la sensibilidad

  const applyFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true); // Activar el mensaje de "Procesando imagen..."

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('sensitivity', sensitivity.toString());

    try {
      const response = await fetch('http://localhost:5000/remove-red-watermark', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al eliminar la marca de agua roja');
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al eliminar la marca de agua roja:', error);
      alert(`Error: ${(error as Error).message}`);
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }
  };

  return (
    <div>
      <h3>Eliminar Marca de Agua Roja</h3>
      <p>Este filtro elimina marcas de agua rojas de las imagenes proporcionadas en clase.</p>
      <label>
        Sensibilidad de Detección de Rojo: {sensitivity}
        <input
          type="range"
          min="0"
          max="255"
          value={sensitivity}
          onChange={(e) => setSensitivity(parseInt(e.target.value))}
        />
      </label>
      <button onClick={applyFilter} disabled={!selectedImage}>
        Eliminar Marca de Agua Roja
      </button>
    </div>
  );
};

export default RemoveRedWatermarkFilter;
