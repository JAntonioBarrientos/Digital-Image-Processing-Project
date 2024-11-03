import { error } from 'console';
import React, { useState } from 'react';

interface HalftoneFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const HalftoneFilter: React.FC<HalftoneFilterProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  // Valores por defecto para los inputs
  const [nVariantes, setNVariantes] = useState<number>(6); // Valor por defecto de n_variantes
  const [fullResolution, setFullResolution] = useState<boolean>(true); // Bandera para indicar si es HD
  const [errorMessage, setErrorMessage] = useState<string | null>(null);  // Estado para el mensaje de error

  // Función para aplicar el filtro de imagen recursiva en escala de grises
  const applyHalftoneFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('n_variantes', nVariantes.toString());
    formData.append('full_resolution', fullResolution.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-halftones-filter', {
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
      <h3>Aplicar semitonos con puntos de distintos tamaños</h3>
      <div>
        <label>
          Número de semitonos ({nVariantes}):
          <input
            type="range"
            value={nVariantes}
            onChange={(e) => setNVariantes(parseInt(e.target.value))}
            min="4"
            max="8"
            style={{ width: '20%' }}
          />
        </label>
      </div>
      {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}
      <button onClick={applyHalftoneFilter}>Aplicar Semitonos</button>
    </div>
  );
};

export default HalftoneFilter;
