import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
import numpy as np
import joblib
import json
import os
from tkinter import *
from tkinter import messagebox  
import random 

# Define 'features' globally for weather prediction
features_weather = [
    'Temperatura del aire HC [°C] - promedio',
    'Punto de Rocío [°C] - promedio',
    'Radiación solar [W/m2] - promedio',
    'Humedad relativa HC [%] - promedio',
    'Velocidad de Viento [m/s] - promedio',
    'Dias desde la primera fecha' 
]

def load_data_from_json(file_path):
    print("Loading data from JSON...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
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
    df = df.dropna(subset=features_weather[:-1] + ['Dirección de Viento [deg]'])  # Exclude the new temporal feature in NaN removal
    df['Dias desde la primera fecha'] = (df['Fecha / Hora'] - df['Fecha / Hora'].min()).dt.days
    X = df[features_weather].values
    y_temp = df['Temperatura del aire HC [°C] - promedio'].values
    y_precipitation = df['Precipitación [mm]'].values
    y_humidity = df['Humedad relativa HC [%] - promedio'].values
    y_wind_direction = df['Dirección de Viento [deg]'].values
    print(f"Data preprocessed: {X.shape}")
    return X, y_temp, y_precipitation, y_humidity, y_wind_direction

def train_models(X_train, y_train_temp, y_train_precipitation, y_train_humidity, y_train_wind_direction):
    print("Training models...")

    # Define parameters for GridSearchCV
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'max_features': ['auto', 'sqrt']
    }

    # Initialize the RandomForestRegressor model
    model_temp = RandomForestRegressor(random_state=42)

    # Initialize GridSearchCV
    grid_temp = GridSearchCV(estimator=model_temp, param_grid=param_grid, cv=3, verbose=2, n_jobs=-1)

    # Train the temperature model
    grid_temp.fit(X_train, y_train_temp)
    best_model_temp = grid_temp.best_estimator_
    print("Best temperature model found.")

    # Save the best temperature model in backend/model_temp.pkl
    model_temp_path = os.path.join('backend', 'model_temp.pkl')
    joblib.dump(best_model_temp, model_temp_path)
    print(f"Temperature model saved in {model_temp_path}")

    # Train models for the other variables
    model_precipitation = RandomForestRegressor(random_state=42, max_features='sqrt')  # Correct max_features
    model_precipitation.fit(X_train, y_train_precipitation)
    model_precipitation_path = os.path.join('backend', 'model_precipitation.pkl')
    joblib.dump(model_precipitation, model_precipitation_path)
    print(f"Precipitation model saved in {model_precipitation_path}")

    model_humidity = RandomForestRegressor(random_state=42, max_features='sqrt')  # Correct max_features
    model_humidity.fit(X_train, y_train_humidity)
    model_humidity_path = os.path.join('backend', 'model_humidity.pkl')
    joblib.dump(model_humidity, model_humidity_path)
    print(f"Humidity model saved in {model_humidity_path}")

    model_wind_direction = RandomForestRegressor(random_state=42, max_features='sqrt')  # Correct max_features
    model_wind_direction.fit(X_train, y_train_wind_direction)
    model_wind_direction_path = os.path.join('backend', 'model_wind_direction.pkl')
    joblib.dump(model_wind_direction, model_wind_direction_path)
    print(f"Wind direction model saved in {model_wind_direction_path}")

    return best_model_temp, model_precipitation, model_humidity, model_wind_direction

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

def save_predictions_to_json(predictions, future_date, file_name="predicciones.json"):
    # Create 'backend' directory if it doesn't exist
    if not os.path.exists('backend'):
        os.makedirs('backend')
    
    file_path = os.path.join('backend', file_name)
    predictions['fecha'] = future_date
    
    with open(file_path, 'w') as json_file:
        json.dump(predictions, json_file, indent=4)
        json_file.write('\n')
    
    print(f"Predictions saved in {file_path}")

def main():
    file_path = './backend/RAFstationdata.json'
    df = load_data_from_json(file_path)
    X_weather, y_temp, y_precipitation, y_humidity, y_wind_direction = preprocess_data_weather(df)

    X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X_weather, y_temp, test_size=0.2, random_state=42)
    X_train_precip, X_test_precip, y_train_precipitation, y_test_precipitation = train_test_split(X_weather, y_precipitation, test_size=0.2, random_state=42)
    X_train_humidity, X_test_humidity, y_train_humidity, y_test_humidity = train_test_split(X_weather, y_humidity, test_size=0.2, random_state=42)
    X_train_wind_dir, X_test_wind_dir, y_train_wind_direction, y_test_wind_direction = train_test_split(X_weather, y_wind_direction, test_size=0.2, random_state=42)

    models = {}
    models['temperatura'], models['precipitacion'], models['humedad'], models['direccion_viento'] = train_models(X_train_temp, y_train_temp, y_train_precipitation, y_train_humidity, y_train_wind_direction)

    root = Tk()
    root.title("Weather Prediction")
    root.geometry("400x300")

    def predict_and_save():
        future_date = entry.get()
        try:
            predictions = predict_future_weather(models, df, future_date)
            save_predictions_to_json(predictions, future_date)
            messagebox.showinfo("Prediction Results", f"Predictions saved successfully!\n\n{predictions}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to predict: {str(e)}")

    label = Label(root, text="Enter future date (DD-MM-YYYY): ")
    label.pack(pady=10)

    entry = Entry(root, width=20)
    entry.pack()

    predict_button = Button(root, text="Predict", command=predict_and_save)
    predict_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()