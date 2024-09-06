import React from 'react';

interface FiltrosTarea4Props {
  expanded: boolean;
  toggleCategory: () => void;
}

const FiltrosTarea4: React.FC<FiltrosTarea4Props> = ({ expanded, toggleCategory }) => {
  return (
    <li onClick={toggleCategory}>
      Filtros Tarea 4
      {expanded && (
        <ul className="sub-menu">
          <li>Borrar marca de agua</li>
          <li>Editor para poner marcas de agua</li>
        </ul>
      )}
    </li>
  );
};

export default FiltrosTarea4;
