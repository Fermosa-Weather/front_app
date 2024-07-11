import React from 'react';
import './App.css'; // Estilos CSS local
import { useNavigate } from 'react-router-dom'; 
import WeatherForecast from './components/WeatherForecast.jsx'; // Importa el componente WeatherForecast
import NewsWidget from './components/NewsWidget.jsx'; // Importa el componente NewsWidget

const App = () => {
  const navigate = useNavigate(); 

  const goToModel = () => {
    navigate('/model'); 
  };

  const goToMaps = () => {
    navigate('/maps'); 
  };

  const goToHome = () => {
    navigate('/'); // Navega a la ruta raíz '/' al hacer clic en el botón
  };

  return (
    <div className="background-container"> {/* Contenedor para el fondo degradado */}
      <div className="App"> {/* Este div es el contenedor principal */}
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
          <button onClick={goToModel}>Hacer Predicciones</button>
          <button onClick={goToMaps}>Ver Mapas de Estaciones</button>
        </div>

        <WeatherForecast /> {/* Componente WeatherForecast debajo de los botones */}

        <NewsWidget /> {/* Componente NewsWidget */}
      </div>
    </div>
  );
};

export default App;
