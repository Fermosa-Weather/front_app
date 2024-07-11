import React from 'react';
import PredictionForm from '../components/PredictionForm.jsx';
import './ModelPage.css'; // Archivo de estilos CSS local

const ModelPage = () => {
  return (
    <div className="model-page-container">
      <h2 className="model-page-heading">Modelo Meteorológico</h2>
      <div className="model-page-content">
        <PredictionForm />
      </div>
    </div>
  );
};

export default ModelPage;
