from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import PredictionErrorDisplay, mean_squared_error, r2_score, accuracy_score

from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from math import sqrt

from sklearn.model_selection import cross_val_score, KFold
import time

start_time = time.time()

app = Flask(__name__)

# Load preprocessed data
excel_file_path = "/Users/kumudshrestha/Documents/major_final 2/cleaned files/refined_data_all.xlsx"

df = pd.read_excel(excel_file_path)

# Define features and target variable
features = ['YEAR', 'MO', 'DY', 'HR', 'DOTW', 'IS_HOLIDAY', 'T2M']
X = df[features]
y = df['electricity']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

def vaue():
    pass

def train_xgboost(X_train, y_train):
    return XGBRegressor().fit(X_train, y_train)

def predict(model, X_test):
    return model.predict(X_test)

def calculate_metrics(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = sqrt(mse)
    r_squared = r2_score(y_true, y_pred)
    return mse, rmse, r_squared

def evaluate_models(models, X_test, y_test):
    results = {}
    for name, model in models.items():
        y_pred = predict(model, X_test)
        mse, rmse, r_squared = calculate_metrics(y_test, y_pred)
        results[name] = {'MSE': mse, 'RMSE': rmse, 'r2_score': r_squared}
    return results

def save_true_predicted_values(models, X_test, y_test, file_path="/Users/kumudshrestha/Documents/major_final 2/true.xlsx"):
    result_df = pd.DataFrame({'True': y_test})
    for name, model in models.items():
        y_pred = predict(model, X_test)
        result_df[f'{name}_P'] = y_pred
    result_df.to_excel(file_path, index=False)

# Train linear regression, KNN, XGBoost models
models = {}
models['xgboost'] = train_xgboost(X_train, y_train)


def validate_input(data):
    required_keys = ['bs_year', 'bs_month', 'bs_day', 'day_of_week_number', 'is_holiday', 'selected_model', 'temperatures']

    for key in required_keys:
        if key not in data:
            return False, f'Missing required key: {key}'

    for key in ['bs_year', 'bs_month', 'bs_day', 'day_of_week_number']:
        if not isinstance(data[key], int):
            return False, f'{key} should be an integer'

    if 'is_holiday' in data:
        if not isinstance(data['is_holiday'], int):
            return False, 'is_holiday should be an integer (0 or 1)'

    if 'temperatures' in data:
        if not isinstance(data['temperatures'], list):
            return False, 'temperatures should be a list'
    
    return True, None


@app.route('/predict_demand', methods=['POST'])
def predict_demand():
    try:
        data = request.json  # Get the JSON data from the request

        # Validate the input data format
        is_valid, error_message = validate_input(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        data = request.json  # Get the JSON data from the request
        app.logger.info(f"Received data: {data}")


        # Extract data
        day_of_week_number = data['day_of_week_number']
        is_holiday = data['is_holiday']
        bs_year = data['bs_year']
        bs_month = data['bs_month']
        bs_day = data['bs_day']
        ad_date = data['ad_date']
        selected_model = data['selected_model']
        temperatures = data['temperatures']
        prediction_hours = list(range(1, 25))

        print(f"BS Date: {bs_year}/{bs_month}/{bs_day}, "
              f"Day of Week: {day_of_week_number}, "
              f"Is Holiday: {is_holiday}, "
              f"Selected Model: {selected_model}, "
              f"Temperatures: {temperatures}")

        # Example: Predict demand using the specified model
        model = models[selected_model]
        if len(temperatures) != 24:
            return jsonify({'error': 'Temperatures should be a list of 24 values'}), 400
        prediction_data = pd.DataFrame({
            'YEAR': [bs_year] * len(prediction_hours) ,
            'MO': [bs_month] * len(prediction_hours),
            'DY': [bs_day] * len(prediction_hours),
            'HR': prediction_hours,
            'DOTW': [day_of_week_number]*len(prediction_hours),
            'IS_HOLIDAY': [is_holiday] * len(prediction_hours),
            'T2M': temperatures
        })
      


        predicted_demand = predict(model, prediction_data)
        # Check if the selected model is XGBoost
        if selected_model == 'xgboost':
    # Convert NumPy arrays to lists for XGBoost predictions
         predicted_demand = predicted_demand.tolist()

        # Example: Respond with a success message and predicted demand
        response = {
            'message': f'Demand predictions received from the backend for BS Date: {bs_year}/{bs_month}/{bs_day}:',
            'predictions': [{'hour': h, 'demand': round(d, 2)} for h, d in zip(range(1, 25), predicted_demand)]
        }
        print(response)
        return jsonify(response), 200
        
       

    except Exception as e:
        # Handle any errors that might occur during processing
        response = {'error': str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)

# Perform cross-validation with the best model
k_fold = KFold(n_splits=5, shuffle=True, random_state=42)
cross_val_scores = cross_val_score(models['svm'], X_train, y_train, cv=k_fold, scoring='neg_mean_squared_error', n_jobs=-1)
print("Cross-Validation Scores:", -cross_val_scores)
print("Mean Cross-Validation RMSE:", -cross_val_scores.mean())

# Evaluate models and store true and predicted values in an Excel file
results = evaluate_models(models, X_test, y_test)
df_evaluation_metric = pd.DataFrame(results)
print(df_evaluation_metric)

# Save the DataFrame to an Excel file
df_evaluation_metric.to_excel("/Users/kumudshrestha/Documents/major_final 2/metrics.xlsx", index=True)

# Save true and predicted values to an Excel file
save_true_predicted_values(models, X_test, y_test)

print('Last part executed.')

