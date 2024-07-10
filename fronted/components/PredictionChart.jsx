import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';

const PredictionChart = () => {
  const [predictions, setPredictions] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await axios.get('http://localhost:5000/predictions');
        setPredictions(response.data);
        setError('');
      } catch (error) {
        setError('Error al obtener datos del servidor');
        setPredictions([]);
      }
    };

    fetchPredictions();
  }, []);

  if (!predictions || !predictions.length) {
    return <p>No hay datos disponibles para mostrar.</p>;
  }

  const data = {
    labels: predictions.map(entry => entry.fecha),
    datasets: [
      {
        label: 'Temperatura',
        data: predictions.map(entry => entry.temperatura.toFixed(2)),
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
      },
      // Puedes agregar más datasets según los datos que quieras mostrar en el gráfico
    ],
  };

  return (
    <div className="prediction-chart">
      <h2>Predicción de Temperatura</h2>
      <Line data={data} />
    </div>
  );
};

export default PredictionChart;
