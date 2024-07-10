from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from model_prediction import predict_future_weather, load_data_from_json
import json
import os

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(__file__)

# Cargar modelos desde la carpeta backend
model_temp = joblib.load(os.path.join(current_dir, 'model_temp.pkl'))
model_precipitation = joblib.load(os.path.join(current_dir, 'model_precipitation.pkl'))
model_humidity = joblib.load(os.path.join(current_dir, 'model_humidity.pkl'))
model_wind_direction = joblib.load(os.path.join(current_dir, 'model_wind_direction.pkl'))

models = {
    'temperatura': model_temp,
    'precipitacion': model_precipitation,
    'humedad': model_humidity,
    'direccion_viento': model_wind_direction
}

# Cargar datos desde la carpeta backend
file_path = os.path.join(current_dir, 'RAFstationdata.json')
df = load_data_from_json(file_path)

# Ruta para obtener las predicciones
@app.route('/predictions', methods=['GET'])
def get_predictions():
    try:
        with open(os.path.join(current_dir, 'predicciones.json'), 'r') as f:
            predictions = json.load(f)
        return jsonify(predictions)
    except FileNotFoundError:
        return jsonify({'error': 'No se encontró el archivo de predicciones'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para realizar predicciones
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

