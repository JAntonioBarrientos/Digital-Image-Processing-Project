// src/filters/ImagenConFraseGris.tsx
import React, { useState } from 'react';

interface ImagenConFraseGrisProps {
  selectedImage: File | null;
  setProcessedImageUrl: (url: string) => void;
  setIsProcessing: (isProcessing: boolean) => void;
}

const ImagenConFraseGris: React.FC<ImagenConFraseGrisProps> = ({
  selectedImage,
  setProcessedImageUrl,
  setIsProcessing,
}) => {
  const [gridWidth, setGridWidth] = useState<number>(5);
  const [gridHeight, setGridHeight] = useState<number>(5);
  const [phrase, setPhrase] = useState<string>('');
  const [htmlUrl, setHtmlUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const applyFilter = async () => {
    if (!selectedImage) {
      alert('Por favor, selecciona una imagen primero.');
      return;
    }

    if (!phrase.trim()) {
      alert('Por favor, ingresa una frase.');
      return;
    }

    setIsProcessing(true); // Activar el mensaje de "Procesando imagen..."
    setError(null); // Resetear cualquier error previo
    setHtmlUrl(null); // Resetear la URL previa

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('grid_width', gridWidth.toString());
    formData.append('grid_height', gridHeight.toString());
    formData.append('phrase', phrase);

    try {
      const response = await fetch('http://localhost:5000/apply-letras-frase-gris', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al aplicar el filtro LetrasFraseGris');
      }

      const data = await response.json();
      if (data.html_url) {
        setHtmlUrl(data.html_url);
        setProcessedImageUrl(data.html_url);
      } else {
        throw new Error('Respuesta inválida del servidor');
      }
    } catch (error: any) {
      console.error('Error al aplicar el filtro LetrasFraseGris:', error);
      setError(error.message || 'Ocurrió un error inesperado');
    } finally {
      setIsProcessing(false); // Desactivar el mensaje de "Procesando imagen..." cuando termine
    }
  };

  return (
    <div>
      <h3>Aplicar Filtro Letras con Frase en Gris</h3>
      <label>
        <b>Ancho del Grid (píxeles):</b>
        <input
          type="number"
          min="1"
          value={gridWidth}
          onChange={(e) => setGridWidth(parseInt(e.target.value) || 1)}
        />
      </label>
      <br />
      <label>
        <b>Alto del Grid (píxeles):</b>
        <input
          type="number"
          min="1"
          value={gridHeight}
          onChange={(e) => setGridHeight(parseInt(e.target.value) || 1)}
        />
      </label>
      <br />
      <label>
        <b>Frase:</b>
        <input
          type="text"
          value={phrase}
          onChange={(e) => setPhrase(e.target.value)}
          placeholder="Ingresa una frase"
        />
      </label>
      <br />
      <button onClick={applyFilter}>Aplicar Filtro Letras con Frase en Gris</button>

      {/* Mostrar mensajes de error */}
      {error && <p className="error-message">{error}</p>}

      {/* Mostrar la URL del HTML generado */}
      {htmlUrl && (
        <div className="html-preview">
          <h4>Resultado:</h4>
          <a href={htmlUrl} target="_blank" rel="noopener noreferrer">
            Ver Imagen con Letras y Frase en Gris
          </a>
          <br />
          {/* Opcional: Mostrar el HTML dentro de un iframe */}
          <iframe
            src={htmlUrl}
            title="Imagen con Letras y Frase en Gris"
            style={{ width: '100%', height: '500px', border: '1px solid #ccc', marginTop: '10px' }}
          ></iframe>
          <h3>HTML guardado en /backend/data/imagen_con_letras</h3>
        </div>
      )}
    </div>
  );
};

export default ImagenConFraseGris;
