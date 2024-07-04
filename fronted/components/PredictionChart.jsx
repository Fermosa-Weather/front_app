import React from 'react';
import { Line } from 'react-chartjs-2';

const PredictionChart = ({ data }) => {
  if (!data || !data.length) {
    return <p>No hay datos disponibles para mostrar.</p>;
  }

  // Aquí puedes continuar con el renderizado del gráfico usando los datos
  return (
    <div className="prediction-chart">
      <Line
        data={{
          labels: data.map(entry => entry.date),  // Ejemplo: Suponiendo que `date` es un campo en tu objeto de datos
          datasets: [
            {
              label: 'Temperatura',
              data: data.map(entry => entry.temperature),  // Ejemplo: Suponiendo que `temperature` es un campo en tu objeto de datos
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              fill: true,
            },
            // Aquí puedes agregar más datasets según los datos que quieras mostrar en el gráfico
          ],
        }}
        options={{
          responsive: true,
          maintainAspectRatio: false,
        }}
      />
    </div>
  );
};

export default PredictionChart;
