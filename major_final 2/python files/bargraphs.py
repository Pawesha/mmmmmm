import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

# Load the preprocessed file
excel_file_path = "/Users/paweshashrestha/Downloads/major_final 2/cleaned files/refined_data_all.xlsx"
df = pd.read_excel(excel_file_path)

# Target variable (each hr ko column)
target_columns = [str(hour) for hour in range(1, 25)]  # Update to include hours from 1 to 24

# Features (independent variables)
features = ['YEAR', 'MO', 'DY', 'DOTW', 'IS_HOLIDAY', 'T2M']  # Remove 'HR' from features
X = df[features]

# Linear regression models and their MSE, R2 values
linear_models = {}
linear_mse_values = {}
linear_r2_values = {}

# K-Nearest Neighbors (KNN) models and their MSE, R2 values
knn_models = {}
knn_mse_values = {}
knn_r2_values = {}

# Train linear regression models and calculate MSE, R2
for hour in target_columns:
    y = df[hour]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    y_linear_pred = linear_model.predict(X_test)
    
    linear_mse = mean_squared_error(y_test, y_linear_pred)
    linear_r2 = r2_score(y_test, y_linear_pred)
    
    linear_models[hour] = linear_model
    linear_mse_values[hour] = linear_mse
    linear_r2_values[hour] = linear_r2
    
    print(f'Linear Regression Mean Squared Error for hour {hour}: {linear_mse}')
    print(f'Linear Regression R-squared for hour {hour}: {linear_r2}')

# Train KNN models and calculate MSE, R2
for hour in target_columns:
    y = df[hour]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    knn_model = KNeighborsRegressor(n_neighbors=5)
    knn_model.fit(X_train_scaled, y_train)
    
    y_knn_pred = knn_model.predict(X_test_scaled)
    
    knn_mse = mean_squared_error(y_test, y_knn_pred)
    knn_r2 = r2_score(y_test, y_knn_pred)
    
    knn_models[hour] = knn_model
    knn_mse_values[hour] = knn_mse
    knn_r2_values[hour] = knn_r2
    
    print(f'KNN Mean Squared Error for hour {hour}: {knn_mse}')
    print(f'KNN R-squared for hour {hour}: {knn_r2}')

# Plotting bar graphs for R2 scores
fig, ax = plt.subplots(figsize=(12, 6))

# Linear regression R2 bars
rects3 = ax.bar(target_columns, list(linear_r2_values.values()), label='Linear Regression (R2)')

# KNN R2 bars
rects4 = ax.bar(target_columns, list(knn_r2_values.values()), label='KNN (R2)')

ax.set_xlabel('Hours')
ax.set_ylabel('R-squared (R2) Score')
ax.set_title('R2 Scores for Linear Regression and KNN Models (by Hour)')
ax.legend()
plt.show()
