import React from 'react';

interface FiltrosTarea1Props {
  expanded: boolean;
  toggleCategory: () => void;
}

const FiltrosTarea1: React.FC<FiltrosTarea1Props> = ({ expanded, toggleCategory }) => {
  return (
    <li onClick={toggleCategory}>
      Filtros Tarea 1
      {expanded && (
        <ul className="sub-menu">
          <li>Gray Promedio</li>
          <li>Gray Ponderado Ojo humano</li>
          <li>Efecto mica RGB</li>
        </ul>
      )}
    </li>
  );
};

export default FiltrosTarea1;
