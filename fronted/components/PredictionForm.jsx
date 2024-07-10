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
      <div className="prediction-form">
        <h2 className="form-title">Predicción Meteorológica</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="futureDate">Ingrese una fecha futura (DD-MM-YYYY):</label>
            <input
              type="text"
              id="futureDate"
              name="futureDate"
              value={futureDate}
              onChange={handleDateChange}
              required
            />
          </div>
          <button type="submit" className="submit-button">Predecir</button>
        </form>
      </div>

      {error && <p className="error">{error}</p>}

      {predictions && Object.keys(predictions).length > 0 ? (
        <div className="predictions">
          <h3>Predicciones para {futureDate}:</h3>
          <p>Temperatura: {predictions.temperatura.toFixed(2)} °C</p>
          <p>Precipitación: {predictions.precipitacion.toFixed(2)} mm</p>
          <p>Humedad: {predictions.humedad.toFixed(2)} %</p>
          <p>Dirección del Viento: {predictions.direccion_viento.toFixed(2)} grados</p>
          <p>Descripción del Clima: {predictions.descripcion_clima}</p>
          <p>Calidad del Aire: {predictions.calidad_aire.toFixed(2)}</p>
        </div>
      ) : (
        <p className="no-data">No hay datos disponibles para mostrar.</p>
      )}
    </div>
  );
};

export default PredictionForm;
