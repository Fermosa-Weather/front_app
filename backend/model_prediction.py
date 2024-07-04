import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
import numpy as np
import joblib
import json
import os
from tkinter import *
from tkinter import messagebox  # Para mostrar mensajes de error
import random  # Importar random para introducir variabilidad aleatoria en las predicciones

# Definir 'features' globalmente para la predicción meteorológica
features_weather = [
    'Temperatura del aire HC [°C] - promedio',
    'Punto de Rocío [°C] - promedio',
    'Radiación solar [W/m2] - promedio',
    'Humedad relativa HC [%] - promedio',
    'Velocidad de Viento [m/s] - promedio',
    'Dias desde la primera fecha'  # Nueva característica temporal
]

def load_data_from_json(file_path):
    print("Cargando datos desde JSON...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convertir los datos JSON en un DataFrame de pandas
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
    print(f"Datos cargados: {df.shape}")
    return df

def preprocess_data_weather(df):
    print("Preprocesando datos...")
    df = df.dropna(subset=features_weather[:-1] + ['Dirección de Viento [deg]'])  # Excluir la nueva característica temporal en la eliminación de NaN
    df['Dias desde la primera fecha'] = (df['Fecha / Hora'] - df['Fecha / Hora'].min()).dt.days
    X = df[features_weather].values
    y_temp = df['Temperatura del aire HC [°C] - promedio'].values
    y_precipitation = df['Precipitación [mm]'].values
    y_humidity = df['Humedad relativa HC [%] - promedio'].values
    y_wind_direction = df['Dirección de Viento [deg]'].values
    print(f"Datos preprocesados: {X.shape}")
    return X, y_temp, y_precipitation, y_humidity, y_wind_direction

def train_models(X_train, y_train_temp, y_train_precipitation, y_train_humidity, y_train_wind_direction):
    print("Entrenando modelos...")

    # Definir los parámetros para GridSearchCV
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'max_features': ['auto', 'sqrt']
    }

    # Inicializar el modelo RandomForestRegressor
    model_temp = RandomForestRegressor(random_state=42)

    # Inicializar GridSearchCV
    grid_temp = GridSearchCV(estimator=model_temp, param_grid=param_grid, cv=3, verbose=2, n_jobs=-1)

    # Entrenar el modelo de temperatura
    grid_temp.fit(X_train, y_train_temp)
    best_model_temp = grid_temp.best_estimator_
    print("Mejor modelo de temperatura encontrado.")

    # Guardar el mejor modelo de temperatura en backend/model_temp.pkl
    joblib.dump(best_model_temp, 'backend/model_temp.pkl')

    # Entrenar modelos para las otras variables
    model_precipitation = RandomForestRegressor(random_state=42, max_features='sqrt')  # Corregir max_features
    model_precipitation.fit(X_train, y_train_precipitation)
    joblib.dump(model_precipitation, 'backend/model_precipitation.pkl')

    model_humidity = RandomForestRegressor(random_state=42, max_features='sqrt')  # Corregir max_features
    model_humidity.fit(X_train, y_train_humidity)
    joblib.dump(model_humidity, 'backend/model_humidity.pkl')

    model_wind_direction = RandomForestRegressor(random_state=42, max_features='sqrt')  # Corregir max_features
    model_wind_direction.fit(X_train, y_train_wind_direction)
    joblib.dump(model_wind_direction, 'backend/model_wind_direction.pkl')

    return best_model_temp, model_precipitation, model_humidity, model_wind_direction

def predict_future_weather(models, df, future_date):
    print(f"Prediciendo para la fecha {future_date}...")
    future_date = pd.to_datetime(future_date, format='%d-%m-%Y', utc=True)
    df['Fecha / Hora'] = df['Fecha / Hora'].dt.tz_localize(None).dt.tz_localize('UTC')  # Convertir a UTC si no está tz-aware
    
    # Tomar el último registro de datos disponibles
    last_data = df.iloc[-1]
    last_features = last_data[features_weather[:-1]].values.reshape(1, -1)  # Excluir la nueva característica temporal

    # Calcular el número de días desde la última fecha registrada hasta la fecha futura
    days_since_last_date = (future_date - df['Fecha / Hora'].max()).days
    future_features = np.append(last_features, [[days_since_last_date]], axis=1)

    predictions = {}

    for key, model in models.items():
        # Predicción basada en el modelo
        prediction = model.predict(future_features)[0]
        
        # Añadir un componente aleatorio para variar las predicciones
        random_factor = random.uniform(-5, 5)  # Variabilidad aleatoria entre -5 y 5
        prediction += random_factor
        
        predictions[key] = prediction

    print(f"Predicciones: {predictions}")
    return predictions

def save_predictions_to_json(predictions, future_date, file_name="predicciones.json"):
    # Crear el directorio 'data' si no existe
    if not os.path.exists('data'):
        os.makedirs('data')
    
    predictions['fecha'] = future_date
    with open(os.path.join('data', file_name), 'w') as json_file:
        json.dump(predictions, json_file, indent=4)
    print(f"Predicciones guardadas en {file_name}")

def main():
    file_path = './backend/RAFstationdata.json'
    df = load_data_from_json(file_path)
    X_weather, y_temp, y_precipitation, y_humidity, y_wind_direction = preprocess_data_weather(df)

    X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X_weather, y_temp, test_size=0.2, random_state=42)
    X_train_precip, X_test_precip, y_train_precipitation, y_test_precipitation = train_test_split(X_weather, y_precipitation, test_size=0.2, random_state=42)
    X_train_humidity, X_test_humidity, y_train_humidity, y_test_humidity = train_test_split(X_weather, y_humidity, test_size=0.2, random_state=42)
    X_train_wind, X_test_wind, y_train_wind_direction, y_test_wind_direction = train_test_split(X_weather, y_wind_direction, test_size=0.2, random_state=42)

    best_model_temp, model_precipitation, model_humidity, model_wind_direction = train_models(
        X_train_temp, y_train_temp, y_train_precipitation, y_train_humidity, y_train_wind_direction)

    models = {
        'temperatura': best_model_temp,
        'precipitacion': model_precipitation,
        'humedad': model_humidity,
        'direccion_viento': model_wind_direction
    }

    root = Tk()
    root.title("Predicción Meteorológica Futura")

    Label(root, text="Ingrese una fecha futura (DD-MM-YYYY):").pack()
    entry_date = Entry(root)
    entry_date.pack()

    result_label = Label(root, text="")
    result_label.pack()

    def predict_button_clicked():
        future_date = entry_date.get()
        try:
            # Verificar el formato de la fecha
            pd.to_datetime(future_date, format='%d-%m-%Y')
            predictions = predict_future_weather(models, df, future_date)
            result_text = f"Predicción para {future_date}:\n"
            result_text += f"Temperatura: {predictions['temperatura']:.2f} °C\n"
            result_text += f"Precipitación: {predictions['precipitacion']:.2f} mm\n"
            result_text += f"Humedad: {predictions['humedad']:.2f} %\n"
            result_text += f"Dirección del Viento: {predictions['direccion_viento']:.2f} °\n"
            result_label.config(text=result_text)
            
            # Guardar las predicciones en un archivo JSON
            save_predictions_to_json(predictions, future_date)

        except ValueError:
            messagebox.showerror("Error de formato", "Formato de fecha incorrecto. Utilice DD-MM-YYYY.")

    Button(root, text="Predecir", command=predict_button_clicked).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
