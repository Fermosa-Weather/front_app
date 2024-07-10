import React from 'react';
import './App.css'; // Archivo de estilos CSS local
import { useNavigate } from 'react-router-dom';

const App = () => {
  const navigate = useNavigate();

  const goToModel = () => {
    navigate('/model');
  };

  const goToMaps = () => {
    navigate('/maps');
  };

  const goToHome = () => {
    navigate('/');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>RAF (Red Agrometeorológicas de Formosa)</h1>
        <p>
          Bienvenidos a la aplicación de predicción meteorológica de la Red Agrometeorológicas de Formosa. 
          Aquí podrás obtener predicciones precisas del clima para fechas futuras, ayudándote a planificar y 
          tomar decisiones informadas.
        </p>
      </header>

      <div className="App-buttons">
        <button onClick={goToHome}>Inicio</button>
        <button onClick={goToModel}>Ir al Modelo</button>
        <button onClick={goToMaps}>Ir a Mapas</button>
      </div>
    </div>
  );
};

export default App;
