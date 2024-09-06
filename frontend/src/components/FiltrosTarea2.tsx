import React from 'react';

interface FiltrosTarea2Props {
  expanded: boolean;
  toggleCategory: () => void;
}

const FiltrosTarea2: React.FC<FiltrosTarea2Props> = ({ expanded, toggleCategory }) => {
  return (
    <li onClick={toggleCategory}>
      Filtros Tarea 2
      {expanded && (
        <ul className="sub-menu">
          <li>Blur</li>
          <li>Motion Blur</li>
          <li>Find Edges</li>
          <li>Sharpen</li>
          <li>Emboss</li>
          <li>Promedio</li>
        </ul>
      )}
    </li>
  );
};

export default FiltrosTarea2;
