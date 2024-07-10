import React from 'react';
import './App.css'; // Estilos CSS local
import { useNavigate } from 'react-router-dom'; // Importa useNavigate desde react-router-dom

// Importa los datos estáticos de noticias
import newsData from './newsData.json';

const App = () => {
  const navigate = useNavigate(); // Usa useNavigate para obtener la función de navegación

  const goToModel = () => {
    navigate('/model'); // Navega a la ruta '/model' al hacer clic en el botón
  };

  const goToMaps = () => {
    navigate('/maps'); // Navega a la ruta '/maps' al hacer clic en el botón
  };

  const goToHome = () => {
    navigate('/'); // Navega a la ruta raíz '/' al hacer clic en el botón
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

      <div className="News-widget">
        <h2>Noticias sobre el Clima en Formosa</h2>
        <div className="News-container">
          {newsData.map((item, index) => (
            <div key={index} className="News-item">
              <img src={item.imageUrl} alt={item.title} className="News-image" />
              <div className="News-content">
                <h3>{item.title}</h3>
                <p>{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
