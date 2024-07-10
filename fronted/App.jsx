import React, { useState, useEffect } from 'react';
import './App.css'; // Archivo de estilos CSS local
import PredictionForm from './components/PredictionForm.jsx';
import axios from 'axios';

const App = () => {
  const [predictions, setPredictions] = useState([]);

  // Función para obtener predicciones
  const fetchPredictions = async (futureDate) => {
    try {
      const response = await axios.post('http://localhost:5000/predict', { future_date: futureDate });
      setPredictions(response.data);
    } catch (error) {
      console.error('Error al obtener predicciones:', error);
      setPredictions([]);
    }
  };

  // Llamar a la función de obtención de predicciones al montar el componente
  useEffect(() => {
    fetchPredictions('03-07-2024');  // Aquí deberías usar la fecha correcta o manejarla dinámicamente
  }, []);  // Vacío para asegurar que se ejecute solo una vez al montar

  return (
    <div className="App">
      <h1>Red Agrometeorologicas de Formosa</h1>
      <h2>Predicción Meteorológica</h2>

      <PredictionForm />

      {/* Puedes agregar otros componentes o funcionalidades aquí */}
    </div>
  );
};

export default App;
