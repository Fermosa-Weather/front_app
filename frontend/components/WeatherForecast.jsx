import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './WeatherForecast.css'; // Estilos CSS local para el componente

// Importar las imágenes de los íconos de clima
import rainyIcon from '../images/rainy-day.png';
import cloudyIcon from '../images/cloudy.png';

const WeatherForecast = () => {
  const [predictions, setPredictions] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await axios.get('http://localhost:5000/predictions');
        setPredictions(response.data.ultimas_predicciones); // Suponiendo que predicciones.json tiene un campo ultimas_predicciones
        setError('');
      } catch (error) {
        setError('No se pudieron cargar las predicciones.');
        setPredictions([]);
      }
    };

    fetchPredictions();
  }, []);

  const settings = {
    dots: true,
    infinite: false, // Desactivar el desplazamiento infinito
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    autoplay: false, // Desactivar autoplay
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
          infinite: false,
          dots: true
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          initialSlide: 0,
          infinite: false,
          dots: true
        }
      }
    ]
  };

  // Función para obtener la imagen del clima según la descripción
  const getWeatherIcon = (descripcionClima) => {
    switch (descripcionClima.toLowerCase()) {
      case 'lluvioso':
        return rainyIcon;
      case 'nublado':
        return cloudyIcon;
      default:
        return null;
    }
  };

  return (
    <div className="weather-forecast-container">
      <h2 className="forecast-title">Pronóstico del Tiempo</h2>
      {error && <p className="error-message">{error}</p>}
      {predictions && predictions.length > 0 ? (
        <Slider {...settings}>
          {predictions.map((prediction, idx) => (
            <div key={idx}>
              <div className="forecast-item">
                <div className="card">
                  <div className="card-body">
                    <h3 className="card-title">{prediction.fecha}</h3>
                    <div className="temperature">
                      <p className="card-text">Temperatura Máxima: {prediction.temperatura_max.toFixed(2)} °C</p>
                      <p className="card-text">Temperatura Mínima: {prediction.temperatura_min.toFixed(2)} °C</p>
                    </div>
                    {/* Mostrar la imagen del clima */}
                    {prediction.descripcion_clima && (
                      <img
                        src={getWeatherIcon(prediction.descripcion_clima)}
                        alt={prediction.descripcion_clima}
                        className="weather-icon"
                      />
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </Slider>
      ) : (
        <p className="no-data">No hay datos disponibles para mostrar.</p>
      )}
    </div>
  );
};

export default WeatherForecast;
