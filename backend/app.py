from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from model_prediction import predict_future_weather, load_data_from_json

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Cargar modelos
model_temp = joblib.load('model_temp.pkl')
model_precipitation = joblib.load('model_precipitation.pkl')
model_humidity = joblib.load('model_humidity.pkl')
model_wind_direction = joblib.load('model_wind_direction.pkl')

models = {
    'temperatura': model_temp,
    'precipitacion': model_precipitation,
    'humedad': model_humidity,
    'direccion_viento': model_wind_direction
}

# Cargar datos
file_path = './RAFstationdata.json'
df = load_data_from_json(file_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    future_date = data.get('future_date')
    
    if not future_date:
        return jsonify({'error': 'La fecha futura es requerida'}), 400

    try:
        pd.to_datetime(future_date, format='%d-%m-%Y')  # Validar formato de fecha
    except ValueError:
        return jsonify({'error': 'Formato de fecha incorrecto. Use DD-MM-YYYY'}), 400

    try:
        predictions = predict_future_weather(models, df, future_date)
        return jsonify(predictions)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
