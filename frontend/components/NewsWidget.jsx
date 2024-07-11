import React from 'react';
import './NewsWidget.css'; // Importa los estilos CSS específicos para este componente
import lasLomitasImage from '../images2/laslomitas.jpg';
import capitalImage from '../images2/ciudadformosa.jfif';
import alertaRafagasImage from '../images2/clorinda.jpg';


const NewsWidget = () => {
  // Datos de ejemplo de noticias
  const newsData = [
    {
      "title": "Se esperan lluvias intensas en Las Lomitas",
      "description": "Para este fin de semana se pronostican lluvias fuertes en Las Lomitas.",
      "imageUrl": lasLomitasImage
    },
    {
      "title": "En la capital formoseña el clima seguirá frío para los próximos días",
      "description": "Se prevén bajas temperaturas durante los próximos días en la ciudad.",
      "imageUrl": capitalImage
    },
    {
      "title": "Alerta por ráfagas de viento en Clorinda",
      "description": "Se emite alerta por ráfagas de viento en Clorinda y sus alrededores.",
      "imageUrl": alertaRafagasImage
    },
  
  ];

  return (
    <div className="News-widget">
      <h2>Noticias sobre el Clima en Formosa</h2>
      <div className="News-container">
        {newsData.map((item, index) => (
          <div key={index} className="News-item">
            {item.imageUrl && (
              <img src={item.imageUrl} alt={item.title} className="News-image" />
            )}
            <div className="News-content">
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NewsWidget;
