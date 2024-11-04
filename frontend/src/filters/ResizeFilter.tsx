import React, { useState } from 'react';

interface ResizeFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const ResizeFilter: React.FC<ResizeFilterProps> = ({
  selectedImage,
  setImagePreview,
  setProcessedImageUrl,
  setIsProcessing,
}) => {
  const [percentX, setPercentX] = useState<number>(100); // Estado para el porcentaje en X
  const [percentY, setPercentY] = useState<number>(100); // Estado para el porcentaje en Y

  const applyFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true); // Activar el mensaje de "Procesando imagen..."

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('percent_x', percentX.toString());
    formData.append('percent_y', percentY.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-resize', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al aplicar el filtro de redimensionamiento');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al aplicar el filtro de redimensionamiento:', error);
      alert('Error al aplicar el filtro de redimensionamiento. Introduce valores positivos a los porcentajes en X y Y.');
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }
  };

  return (
    <div>
      <h3>Aplicar Filtro de Redimensionamiento</h3>
      <label>
        Porcentaje en X (Ancho): {percentX}%
        <input
          type="number"
          min="1"
          value={percentX}
          onChange={(e) => setPercentX(parseFloat(e.target.value))}
        />
      </label>
      <br />
      <label>
        Porcentaje en Y (Alto): {percentY}%
        <input
          type="number"
          min="1"
          value={percentY}
          onChange={(e) => setPercentY(parseFloat(e.target.value))}
        />
      </label>
      <br />
      <button onClick={applyFilter}>Aplicar Filtro de Redimensionamiento</button>
    </div>
  );
};

export default ResizeFilter;
