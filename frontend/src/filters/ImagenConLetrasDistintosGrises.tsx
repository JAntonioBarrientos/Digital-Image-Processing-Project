import React, { useState } from 'react';

interface ImagenConLetrasDistintosGrisesProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const ImagenConLetrasDistintosGrises: React.FC<ImagenConLetrasDistintosGrisesProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  const [blockWidth, setBlockWidth] = useState<number>(50);
  const [blockHeight, setBlockHeight] = useState<number>(50);

  const applyFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true); // Activar el mensaje de "Procesando imagen..."

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('block_width', blockWidth.toString());
    formData.append('block_height', blockHeight.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-imagen-ms-grises', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al aplicar el filtro máximo');
      }

      const data = await response.blob();
      const imageUrl = URL.createObjectURL(data);
      setImagePreview(imageUrl);
      setProcessedImageUrl(imageUrl);
    } catch (error) {
      console.error('Error al aplicar el filtro máximo:', error);
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }
  };

  return (
    <div>
      <h3>Aplicar Filtro</h3>
      <label>
        <b>Tamaño del Bloque Grid (Ancho en píxeles):</b>
        <input
          type="number"
          min="1"
          value={blockWidth}
          onChange={(e) => setBlockWidth(parseInt(e.target.value) || 1)}
        />
      </label>
      <br />
      <label>
        <b>Tamaño del Bloque Grid (Alto en píxeles):</b>
        <input
          type="number"
          min="1"
          value={blockHeight}
          onChange={(e) => setBlockHeight(parseInt(e.target.value) || 1)}
        />
      </label>
      <button onClick={applyFilter}>Aplicar Filtro Máximo</button>
    </div>
  );
};

export default ImagenConLetrasDistintosGrises;
