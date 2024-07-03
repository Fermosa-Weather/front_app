import React, { useState } from 'react';
import axios from 'axios';
import './PredictionForm.css'; // Archivo de estilos CSS local

const PredictionForm = () => {
  const [futureDate, setFutureDate] = useState('');
  const [predictions, setPredictions] = useState({});
  const [error, setError] = useState('');

  const handleDateChange = (e) => {
    setFutureDate(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/predict', { future_date: futureDate });
      setPredictions(response.data);
      setError('');
    } catch (error) {
      setError('No se pudo realizar la predicción. Verifica la fecha ingresada.');
      setPredictions({});
    }
  };

  return (
    <div className="prediction-form-container">
      <form className="prediction-form" onSubmit={handleSubmit}>
        <label htmlFor="futureDate">Ingrese una fecha futura (DD-MM-YYYY):</label>
        <input
          type="text"
          id="futureDate"
          name="futureDate"
          value={futureDate}
          onChange={handleDateChange}
          required
        />
        <button type="submit">Predecir</button>
      </form>

      {error && <p className="error">{error}</p>}

      {predictions && Object.keys(predictions).length > 0 && (
        <div className="predictions">
          <h3>Predicciones para {futureDate}:</h3>
          <p>Temperatura: {predictions.temperatura.toFixed(2)} °C</p>
          <p>Precipitación: {predictions.precipitacion.toFixed(2)} mm</p>
          <p>Humedad: {predictions.humedad.toFixed(2)} %</p>
          <p>Dirección del Viento: {predictions.direccion_viento.toFixed(2)} grados</p>
        </div>
      )}
    </div>
  );
};

export default PredictionForm;
