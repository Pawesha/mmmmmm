import pandas as pd

file_path = "./dataset/output/refined_dataset.xlsx"
df = pd.read_excel(file_path) # Loading excel file

# Extract year, month, and day into separate columns
df['year'] = df['DateTime'].dt.year
df['month'] = df['DateTime'].dt.month
df['day'] = df['DateTime'].dt.day

# Print the DataFrame to see the results

print(df.head(5))