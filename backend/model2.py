import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import joblib
import os
import random
import requests
from flask import Flask, request, jsonify

# Define 'features' globally for weather prediction
features_weather = [
    'Temperatura del aire HC [°C] - promedio',
    'Punto de Rocío [°C] - promedio',
    'Radiación solar [W/m2] - promedio',
    'Humedad relativa HC [%] - promedio',
    'Velocidad de Viento [m/s] - promedio',
    'Dias desde la primera fecha'  # New temporal feature
]

def load_data_from_api(api_url):
    print("Loading data from API...")
    response = requests.get(api_url)
    data = response.json()

    # Convert JSON data into a pandas DataFrame
    records = []
    for record in data:
        flat_record = {
            'Fecha / Hora': pd.to_datetime(record['date']['$date'], utc=True),
            'Temperatura del aire HC [°C] - promedio': record['sensors']['hCAirTemperature']['avg'],
            'Punto de Rocío [°C] - promedio': record['sensors']['dewPoint']['avg'],
            'Radiación solar [W/m2] - promedio': record['sensors']['solarRadiation']['avg'],
            'Humedad relativa HC [%] - promedio': record['sensors']['hCRelativeHumidity']['avg'],
            'Velocidad de Viento [m/s] - promedio': record['sensors']['uSonicWindSpeed']['avg'],
            'Dirección de Viento [deg]': record['sensors']['uSonicWindDir']['last'],
            'Precipitación [mm]': record['sensors']['precipitation']['sum']
        }
        records.append(flat_record)

    df = pd.DataFrame(records)
    print(f"Data loaded: {df.shape}")
    return df

def preprocess_data_weather(df):
    print("Preprocessing data...")
    df = df.dropna(subset=features_weather[:-1] + ['Dirección de Viento [deg]'])  # Exclude the new temporal feature
    df['Dias desde la primera fecha'] = (df['Fecha / Hora'] - df['Fecha / Hora'].min()).dt.days
    X = df[features_weather].values
    return X, df

def predict_future_weather(models, df, future_date):
    print(f"Predicting for the date {future_date}...")
    future_date = pd.to_datetime(future_date, format='%d-%m-%Y', utc=True)
    df['Fecha / Hora'] = df['Fecha / Hora'].dt.tz_localize(None).dt.tz_localize('UTC')  # Convert to UTC if not tz-aware
    
    # Take the last available data record
    last_data = df.iloc[-1]
    last_features = last_data[features_weather[:-1]].values.reshape(1, -1)  # Exclude the new temporal feature

    # Calculate the number of days from the last recorded date to the future date
    days_since_last_date = (future_date - df['Fecha / Hora'].max()).days
    future_features = np.append(last_features, [[days_since_last_date]], axis=1)

    predictions = {}

    for key, model in models.items():
        # Prediction based on the model
        prediction = model.predict(future_features)[0]
        
        # Add a random component to vary the predictions
        random_factor = random.uniform(-5, 5)  # Random variability between -5 and 5
        prediction += random_factor
        
        # Adjust precipitation prediction to ensure non-negative values
        if key == 'precipitacion':
            prediction = max(0, prediction)  # Ensure non-negative values
        
        predictions[key] = prediction
    
    # Determine weather description
    if predictions['temperatura'] >= 30:
        predictions['descripcion_clima'] = 'Caluroso'
    elif predictions['precipitacion'] > 0:
        predictions['descripcion_clima'] = 'Lluvioso'
    else:
        predictions['descripcion_clima'] = 'Nublado'
    
    # Calculate air quality index
    predictions['calidad_aire'] = random.uniform(1, 5)  # Example random value, adjust according to available data

    print(f"Predictions: {predictions}")
    return predictions

# Flask application
app = Flask(__name__)

# Load models
model_temp = joblib.load('backend/model_temp.pkl')
model_precipitation = joblib.load('backend/model_precipitation.pkl')
model_humidity = joblib.load('backend/model_humidity.pkl')
model_wind_direction = joblib.load('backend/model_wind_direction.pkl')

models = {
    'temperatura': model_temp,
    'precipitacion': model_precipitation,
    'humedad': model_humidity,
    'direccion_viento': model_wind_direction
}

@app.route('/predict', methods=['GET'])
def predict():
    api_url = 'URL_DE_TU_API'  # Reemplaza con la URL de tu API
    future_date = request.args.get('future_date')
    if not future_date:
        return jsonify({'error': 'Please provide a future date in the format DD-MM-YYYY'}), 400

    try:
        df = load_data_from_api(api_url)
        X_weather, df_processed = preprocess_data_weather(df)
        predictions = predict_future_weather(models, df_processed, future_date)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
