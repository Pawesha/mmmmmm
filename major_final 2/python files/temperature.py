import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load your Excel file into a pandas DataFrame
file_path = '/Users/paweshashrestha/Downloads/major_final 2/temperature_only.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')  # Specify the engine, use 'xlrd' if needed

# Feature Engineering
df['datetime'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY', 'HOUR']], errors='coerce')
df['hour_of_day'] = df['datetime'].dt.hour

# Split Data
X = df[['YEAR', 'MONTH', 'DAY', 'HOUR']]  # Features
y = df['TEMPERATURE']  # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Model Evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Print Predicted Values
print("temp Predicted Values:")
print(y_pred)
