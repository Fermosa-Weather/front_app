import React from 'react';
import './App.css'; // Archivo de estilos CSS local
import PredictionForm from './components/PredictionForm.jsx';

const App = () => {
  return (
    <div className="App">
      <h1>Red Agrometeorologicas de Formosa</h1>
      <h1>Predicción Meteorológica</h1>

      <PredictionForm />
    </div>
  );
};

export default App;
