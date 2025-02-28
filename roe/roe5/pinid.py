import pandas as pd
import os

# Get the full path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the CSV file
businesses_csv_path = os.path.join(script_dir, 'businesses.csv')

try:
    # Read the CSV file with full path
    df = pd.read_csv(businesses_csv_path)
    
    # Check if required columns exist
    if 'postal_code' in df.columns and 'business_id' in df.columns:
        # Select only the postal_code and business_id columns
        result_df = df[['postal_code', 'business_id']]
        
        # Save to pinid.csv
        result_df.to_csv(os.path.join(script_dir, 'pinid.csv'), index=False)
        
        print(f"Successfully extracted {len(result_df)} records to pinid.csv")
    else:
        missing_cols = []
        if 'postal_code' not in df.columns:
            missing_cols.append('postal_code')
        if 'business_id' not in df.columns:
            missing_cols.append('business_id')
        print(f"Error: Missing required columns: {', '.join(missing_cols)}")
        
except Exception as e:
    print(f"Error reading businesses.csv: {e}")
    print(f"Attempted to read from: {businesses_csv_path}")