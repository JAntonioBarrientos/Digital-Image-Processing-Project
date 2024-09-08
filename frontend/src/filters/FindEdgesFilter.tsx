import React from 'react';

interface FindEdgesFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const FindEdgesFilter: React.FC<FindEdgesFilterProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  const applyFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true); // Activar el mensaje de "Procesando imagen..."

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await fetch('http://localhost:5000/apply-find-edges', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al aplicar el filtro de Detección de Bordes');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al aplicar el filtro de Detección de Bordes:', error);
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }
  };

  return <button onClick={applyFilter}>Aplicar Filtro Detección de Bordes</button>;
};

export default FindEdgesFilter;
