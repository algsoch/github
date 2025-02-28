import pandas as pd
import datetime

# Read the CSV file
df = pd.read_csv('violations.csv')

# Convert the date column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Extract day of week (0 = Monday, 1 = Tuesday, etc.)
df['day_of_week'] = df['date'].dt.dayofweek

# Filter for Moderate Risk violations that occurred on Mondays (day_of_week = 0)
monday_moderate_risk = df[(df['risk_category'] == 'Moderate Risk') & (df['day_of_week'] == 0)]

# Group by business_id and count occurrences
result = monday_moderate_risk.groupby('business_id').size().reset_index(name='monday_moderate_risk_count')

# Sort by count in descending order
result = result.sort_values('monday_moderate_risk_count', ascending=False)

# Print the results
print(result.head())# Print the first few rows
print(result.tail())# Print the last few rows
print(result['business_id'].iloc[0])# Print the business_id with the highest count
# Print the first few rows
# print(result.head())
print(len(list(result['business_id'])))# Print the business_id with the highest count