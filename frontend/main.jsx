import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App.jsx'; // Asumiendo que App.jsx está en el mismo directorio y se importa así

import 'bootstrap/dist/css/bootstrap.min.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/prediction" element={<App />} /> {/* Ruta para App */}
      </Routes>
    </Router>
  </React.StrictMode>
);
