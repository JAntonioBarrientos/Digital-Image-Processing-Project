import { error } from 'console';
import React, { useState } from 'react';

interface RecursiveGrayFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const RecursiveGrayFilter: React.FC<RecursiveGrayFilterProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  // Valores por defecto para los inputs
  const [nVariantes, setNVariantes] = useState<number>(50); // Valor por defecto de n_variantes
  const [gridFactor, setGridFactor] = useState<number>(120); // Valor por defecto de grid_factor
  const [errorMessage, setErrorMessage] = useState<string | null>(null);  // Estado para el mensaje de error


  // Función para aplicar el filtro de imagen recursiva en escala de grises
  const applyRecursiveGrayFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('n_variantes', nVariantes.toString());
    formData.append('grid_factor', gridFactor.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-recursive-image-gray', {
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
      <h3>Aplicar Filtro de Imagen Recursiva en Escala de Grises</h3>
      <div>
        <label>
          Número de Variantes ({nVariantes}):
          <input
            type="number"
            value={nVariantes}
            onChange={(e) => setNVariantes(parseInt(e.target.value))}
            min="2"
            max="255"
            style={{ width: '20%' }}
          />
        </label>
        <label>
          Factor de Cuadrícula ({gridFactor}):
          <input
            type="number"
            value={gridFactor}
            onChange={(e) => setGridFactor(parseInt(e.target.value))}
            style={{ width: '20%' }}
          />
        </label>
      </div>
      {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}
      <button onClick={applyRecursiveGrayFilter}>Aplicar Filtro Recursivo Grayscale</button>
    </div>
  );
};

export default RecursiveGrayFilter;
