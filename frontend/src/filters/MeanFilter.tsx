import React from 'react';

interface MeanFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const MeanFilter: React.FC<MeanFilterProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  const applyFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true); // Mostrar "Procesando imagen..."

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await fetch('http://localhost:5000/apply-mean-filter', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al aplicar el filtro de Promedio');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al aplicar el filtro de Promedio:', error);
    } finally {
      setIsProcessing(false); // Ocultar "Procesando imagen..." cuando termine
    }
  };

  return <button onClick={applyFilter}>Aplicar Filtro de Promedio</button>;
};

export default MeanFilter;
