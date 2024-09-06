import React, { useState, useEffect } from 'react';

const App: React.FC = () => {
    const [message, setMessage] = useState<string>('');  // Estado para el mensaje

    useEffect(() => {
        // Hacemos una solicitud GET al backend Flask
        fetch('http://localhost:5000/api/hello')
            .then(response => response.json())
            .then(data => setMessage(data.message))
            .catch(error => console.error('Error fetching the data:', error));
    }, []);

    return (
      <div>
          <h1>Frontend con React y TypeScript</h1>
          <p>Mensaje desde el backend: {message ? message : "Cargando mensaje..."}</p>
      </div>
  );
  
};

export default App;
