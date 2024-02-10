import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from math import sqrt
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score, KFold
import time
from joblib import dump
import os

start_time = time.time()

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

def vaue():
     pass


def train_linear_regression(X_train, y_train):
    return LinearRegression().fit(X_train, y_train)

def train_knn(X_train, y_train, n_neighbors=5):
    n_neighbors = min(n_neighbors, len(X_train))
    return KNeighborsRegressor(n_neighbors=n_neighbors).fit(X_train, y_train)

def train_xgboost(X_train, y_train):
    return XGBRegressor().fit(X_train, y_train)


# grid_search.fit(X_train, y_train)
        
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


def save_true_predicted_values(models, X_test, y_test, file_path="./dataset/output/true.xlsx"):
    result_df = pd.DataFrame({'True': y_test})
    for name, model in models.items():
        y_pred = predict(model, X_test)
        result_df[f'{name}_P'] = y_pred
    result_df.to_excel(file_path, index=False)

# Train linear regression, KNN, XGBoost models
models = {}
models['linear_regression'] = train_linear_regression(X_train, y_train)
models['knn'] = train_knn(X_train, y_train)
models['xgboost'] = train_xgboost(X_train, y_train)


# Evaluate models and store true and predicted values in an Excel file
results = evaluate_models(models, X_test, y_test)
df_evaluation_metric = pd.DataFrame(results)
print(df_evaluation_metric)

# Save the DataFrame to an Excel file
df_evaluation_metric.to_excel("./dataset/output/scores.xlsx", index=True)

# Save true and predicted values to an Excel file
save_true_predicted_values(models,X_test, y_test)

# Save the XGBoost model
xgboost_model_file_path = "./xgboost_model.joblib"
dump(models['xgboost'], xgboost_model_file_path)
print(f"XGBoost model saved to {xgboost_model_file_path}")
print('Last part executed.')



#asti processing time sodheko thyo so haldeko hai herna lai
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Processing time: {elapsed_time} seconds")