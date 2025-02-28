import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('BOD20.csv')

# Ensure the 'NEW WQI' column is of type float
df['NEW WQI'] = pd.to_numeric(df['NEW WQI'], errors='coerce')

# Find the row with the minimum WQI value
min_wqi_row = df.loc[df['NEW WQI'].idxmin()]

# Extract the station and WQI value
min_station = min_wqi_row['STATION']
min_wqi = min_wqi_row['NEW WQI']

# Print the station with the least WQI value
print(f"The station with the least WQI value is {min_station} with a WQI of {min_wqi}")