import React from 'react';

interface FiltrosTarea3Props {
  expanded: boolean;
  toggleCategory: () => void;
}

const FiltrosTarea3: React.FC<FiltrosTarea3Props> = ({ expanded, toggleCategory }) => {
  return (
    <li onClick={toggleCategory}>
      Filtros Tarea 3
      {expanded && (
        <ul className="sub-menu">
          <li>Imágenes recursivas en tonos gris</li>
          <li>Imágenes recursivas color real</li>
        </ul>
      )}
    </li>
  );
};

export default FiltrosTarea3;
