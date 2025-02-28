import csv

# Load the CSV files into lists
with open('output.csv', 'r') as output_file:
    output_reader = csv.reader(output_file)
    output_data = list(output_reader)

with open('STATION_WQI.csv', 'r') as wqi_file:
    wqi_reader = csv.reader(wqi_file)
    wqi_data = list(wqi_reader)

# Extract headers
output_header = output_data[0]
wqi_header = wqi_data[0]

# Create a dictionary for WQI data with STATION CODE as the key
wqi_dict = {row[0]: row[1] for row in wqi_data[1:]}

# Prepare the result data
result_data = [['PINCODE', 'WQI', 'status']]

# Iterate through the output data and compare with WQI data
for row in output_data[1:]:
    station = row[0]
    pincode = row[1]
    if station in wqi_dict:
        wqi_value = float(wqi_dict[station])
        status = 'unsafe' if wqi_value < 50 else 'safe'
        result_data.append([pincode, wqi_value, status])

# Save the result to a new CSV file
with open('check.csv', 'w', newline='') as check_file:
    writer = csv.writer(check_file)
    writer.writerows(result_data)

# Print the result data
for row in result_data:
    print(row)
