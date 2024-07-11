import React from 'react';
import './NewsWidget.css'; 
import newsData from '../newsData.json'; 

const NewsWidget = () => {
  const displayedNews = newsData.slice(0, 6); 

  return (
    <div className="News-widget">
      <h2>Noticias sobre el Clima en Formosa</h2>
      <div className="News-container">
        {displayedNews.map((item, index) => (
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
  );
};

export default NewsWidget;
