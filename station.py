import pandas as pd
from geopy.distance import geodesic

# Load the CSV and Parquet files into DataFrames
output_df = pd.read_csv('output.csv')
pincode_coordinates_df = pd.read_parquet('pincode_coordinates.parquet')

# Print the column names to verify
print("Output CSV columns:", output_df.columns)
print("Pincode Coordinates Parquet columns:", pincode_coordinates_df.columns)

# Convert the 'STATION' column to string to ensure consistency
output_df['STATION'] = output_df['STATION'].astype(str)

# Ensure the 'PINCODE' column exists in both DataFrames
if 'PINCODE' in output_df.columns and 'Pincode' in pincode_coordinates_df.columns:
    # Merge with pincode coordinates
    merged_df = pd.merge(output_df, pincode_coordinates_df, left_on='PINCODE', right_on='Pincode')

    # Calculate distances and find the closest pair of cities
    min_distance = float('inf')
    closest_pair = None

    for i in range(len(merged_df)):
        for j in range(i + 1, len(merged_df)):
            coord1 = (merged_df.iloc[i]['Latitude'], merged_df.iloc[i]['Longitude'])
            coord2 = (merged_df.iloc[j]['Latitude'], merged_df.iloc[j]['Longitude'])
            distance = geodesic(coord1, coord2).kilometers
            if distance < min_distance:
                min_distance = distance
                closest_pair = (merged_df.iloc[i]['PINCODE'], merged_df.iloc[j]['PINCODE'])

    # Print the closest pair of cities
    if closest_pair:
        print(f"The closest pair of cities are {closest_pair[0]} and {closest_pair[1]} with a distance of {min_distance} km")
    else:
        print("No closest pair found.")
else:
    print("Required columns 'PINCODE' or 'Pincode' not found in the DataFrames.")