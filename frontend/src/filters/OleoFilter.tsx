import { error } from 'console';
import React, { useState } from 'react';

interface OleoFilterProps {
  selectedImage: File | null;
  setImagePreview: (url: string) => void;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const OleoFilter: React.FC<OleoFilterProps> = ({ selectedImage, setImagePreview, setProcessedImageUrl, setIsProcessing }) => {
  // Valores por defecto para los inputs
  const [color, setColor] = useState<boolean>(false); // Valor por defecto de color
  const [blur, setBlur] = useState<boolean>(false); // Valor por defecto de blur
  const [blockSize, setBlockSize] = useState<number>(7); // Valor por defecto de blockSize
  const [errorMessage, setErrorMessage] = useState<string | null>(null);  // Estado para el mensaje de error

  // Función para aplicar  el filtro de imagen de oleo
  const applyOleoFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    setIsProcessing(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('color', color.toString());
    formData.append('blur', blur.toString());
    formData.append('blockSize', blockSize.toString());

    try {
      const response = await fetch('http://localhost:5000/apply-oleo-filter', {
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
      <h3>Aplicar filtro de oleo</h3>
      <div>
        <label>
          Aplicar filtro a color:
          <input
            type="checkbox"
            checked={color}
            onChange={(e) => setColor(e.target.checked)}
            style={{ marginLeft: '10px' }}
          />
        </label>
        <label>
          Aplicar filtro de oleo + blur:
          <input
            type="checkbox"
            checked={blur}
            onChange={(e) => setBlur(e.target.checked)}
            style={{ marginLeft: '10px' }}
          />
        </label>
        <label>
          Tamaño de la matriz de bloque ({blockSize}x{blockSize}):
          <input
            type="range"
            min="3"
            max="25"
            value={blockSize}
            onChange={(e) => setBlockSize(parseInt(e.target.value))}
            style={{ marginLeft: '10px' }}
          />
        </label>
      </div>
      {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}
      <button onClick={applyOleoFilter}>Aplicar Oleo</button>
    </div>
  );
};

export default OleoFilter;
