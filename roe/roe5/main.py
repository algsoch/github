import os
import csv
import glob
from bs4 import BeautifulSoup

def extract_business_details(html_file):
    """Extract business details from an HTML file."""
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        # Find all tables containing business information
        tables = soup.find_all('table', class_='table')
        businesses = []
        
        for table in tables:
            # Extract business name from the first row header
            business_name = table.find('th').text.strip()
            
            # Initialize dictionary to store business details
            business_details = {'business_name': business_name}
            
            # Extract all details from the table rows
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                cells = row.find_all('td')
                # Process cells in pairs (key-value)
                for i in range(0, len(cells), 2):
                    if i+1 < len(cells):
                        key = cells[i].text.strip()
                        value = cells[i+1].text.strip()
                        business_details[key] = value
                        
                        # If there are more cells in the row, process them too
                        if i+3 < len(cells):
                            key2 = cells[i+2].text.strip()
                            value2 = cells[i+3].text.strip()
                            business_details[key2] = value2
            
            businesses.append(business_details)
        
        return businesses

def main():
    # Path to the directory containing HTML files
    html_dir = r'c:/github/roe/roe5/'
    
    # Find all HTML files in the directory
    html_files = glob.glob(os.path.join(html_dir, 'biz-*.html'))
    
    all_businesses = []
    
    # Process each HTML file
    for html_file in html_files:
        businesses = extract_business_details(html_file)
        all_businesses.extend(businesses)
    
    if not all_businesses:
        print("No business data found.")
        return
    
    # Get all unique field names to use as CSV headers
    fieldnames = set()
    for business in all_businesses:
        fieldnames.update(business.keys())
    
    # Write data to CSV
    csv_file = os.path.join(html_dir, 'businesses.csv')
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted(list(fieldnames)))
        writer.writeheader()
        writer.writerows(all_businesses)
    
    print(f"Extracted {len(all_businesses)} businesses from {len(html_files)} HTML files.")
    print(f"Data saved to {csv_file}")

if __name__ == '__main__':
    main()