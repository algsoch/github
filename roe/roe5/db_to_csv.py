import sqlite3
import csv
import os

def db_to_csv(db_path, csv_path):
    """
    Extract data from SQLite database and save to CSV file.
    
    Args:
        db_path (str): Path to the SQLite database file
        csv_path (str): Path where the CSV file will be saved
    """
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if not tables:
        print(f"No tables found in {db_path}")
        conn.close()
        return
    
    # We'll use the first table found (or you can specify a table name)
    table_name = tables[0][0]
    print(f"Using table: {table_name}")
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Get all the data
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    
    # Write to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write the header
        csv_writer.writerow(columns)
        
        # Write the data rows
        csv_writer.writerows(data)
    
    print(f"Data exported to {csv_path}")
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    # Paths to the database and CSV files
    db_path = os.path.join(os.path.dirname(__file__), "violations.db")
    csv_path = os.path.join(os.path.dirname(__file__), "violations.csv")
    
    # Extract data from DB to CSV
    db_to_csv(db_path, csv_path)