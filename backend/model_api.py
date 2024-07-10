import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

class WeatherModel:
    def __init__(self, model_file):
        self.model = joblib.load(model_file)

    def predict(self, input_data):
        input_df = pd.DataFrame([input_data])
        return self.model.predict(input_df)

class PredictionService:
    def __init__(self):
        model_dir = os.path.dirname(__file__)
        self.model_temp = WeatherModel(os.path.join(model_dir, 'model_temp.pkl'))
        self.model_precipitation = WeatherModel(os.path.join(model_dir, 'model_precipitation.pkl'))
        self.model_humidity = WeatherModel(os.path.join(model_dir, 'model_humidity.pkl'))
        self.model_wind_direction = WeatherModel(os.path.join(model_dir, 'model_wind_direction.pkl'))

    def make_predictions_for_date(self, input_data):
        temp_prediction = self.model_temp.predict(input_data)
        precipitation_prediction = self.model_precipitation.predict(input_data)
        humidity_prediction = self.model_humidity.predict(input_data)
        wind_direction_prediction = self.model_wind_direction.predict(input_data)

        predictions = {
            'temperature_prediction': temp_prediction[0],
            'precipitation_prediction': precipitation_prediction[0],
            'humidity_prediction': humidity_prediction[0],
            'wind_direction_prediction': wind_direction_prediction[0]
        }
        return predictions

prediction_service = PredictionService()

@app.route('/api/predictions', methods=['POST'])
def predict():
    try:
        input_data = request.json
        predictions = prediction_service.make_predictions_for_date(input_data)
        response = {'status': 'success', 'predictions': predictions}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)
