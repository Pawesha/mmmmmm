# import pandas as pd

# file_path = "./dataset/output/refined_dataset.xlsx"
# df = pd.read_excel(file_path) # Loading excel file

# # Extract year, month, and day into separate columns
# df['year'] = df['DateTime'].dt.year
# df['month'] = df['DateTime'].dt.month
# df['day'] = df['DateTime'].dt.day

# # Print the DataFrame to see the results

# print(df.head(5))

from flask import Flask, jsonify, request
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

import requests

app = Flask(__name__)

# Load preprocessed data
excel_file_path = "./dataset/output/refined_dataset.xlsx"
df = pd.read_excel(excel_file_path)

df['e_year'] = df['DateTime'].dt.year
df['e_month'] = df['DateTime'].dt.month
df['e_day'] = df['DateTime'].dt.day

# Define features and target variable
features = ['e_year', 'e_month', 'e_day', 'HOUR', 'DOTW', 'IS_HOLIDAY', 'T2M','seasons_int']
X = df[features]
y = df['electricity']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Load the trained model
model = joblib.load("trained_model.pkl")

# Second Flask API URL
temperature_api_url = "http://localhost:5002"

def get_temperature_predictions(year, month, day):
    # Make a POST request to the second Flask API to get temperature predictions
    data = {
        "bs_year": year,
        "bs_month": month,
        "bs_day": day
    }
    response = requests.post(temperature_api_url, json=data)
    if response.status_code == 200:
        return response.json()["predictions"]
    else:
        # Handle error response
        return None

@app.route('/predict_demand_with_temperature', methods=['POST'])
def predict_demand_with_temperature():
    data = request.json  # Get the JSON data from the request

    # Extract data
    year = data['e_year']
    month = data['e_month']
    day = data['e_day']
    temperatures = get_temperature_predictions(year, month, day)
    
    if temperatures is None:
        return jsonify({'error': 'Failed to get temperature predictions'}), 500

    # Add temperatures to features
    data['temperatures'] = temperatures

    # Make prediction using the model
    predicted_demand = model.predict([data])[0]

    # Respond with predicted demand
    response = {
        'predicted_demand': predicted_demand
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
