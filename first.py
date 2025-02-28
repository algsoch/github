import pdfplumber
import pandas as pd
import sqlite3

pdf_path = "W1.pdf"

# Path to the SQLite database file
db_path = "pincode_station.db"

# Connect to the database
conn = sqlite3.connect(db_path)

# Create a cursor object
cursor = conn.cursor()

# Query to find tables containing the specified columns
query = """
SELECT name FROM sqlite_master 
WHERE type='table' AND name IN (
    SELECT tbl_name FROM sqlite_master 
    WHERE sql LIKE '%station%' AND sql LIKE '%pin code%'
);
"""

# Execute the query
cursor.execute(query)

# Fetch all matching table names
tables = cursor.fetchall()

# Print the table names
for table in tables:
    print(f"Table found: {table[0]}")

    # Query to retrieve data from the found table
    cursor.execute(f"SELECT * FROM {table[0]}")
    rows = cursor.fetchall()

    # Print the retrieved rows
    for row in rows:
        import csv
        with open('output.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            l=[row[0],row[1]]
            writer.writerow(l)
        print(row)

# Close the cursor and connection
cursor.close()
conn.close()

# Extract tables from the PDF and save them as CSV files
# with pdfplumber.open(pdf_path) as pdf:
#     for page_num, page in enumerate(pdf.pages, start=1):
#         table = page.extract_table()
#         if table:
#             # Convert the table to a DataFrame
#             df = pd.DataFrame(table[1:], columns=table[0])
#             print(f"Table from page {page_num}")
#             print(df)  # Prints each table as a DataFrame
#             # Save each table to a separate CSV file
#             df.to_csv(f"table_page_{page_num}.csv", index=False)

