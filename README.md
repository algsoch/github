PDF to CSV Converter
A Python utility that extracts tables from PDF files and converts them to CSV format.

Overview
This tool scans a directory for PDF files and extracts tables from each PDF using two different methods:

First attempts extraction using tabula-py (Java-based PDF parser)
Falls back to pdfplumber if tabula extraction fails
Each PDF file is converted to a corresponding CSV file with the same base name.

Features
Automatic processing of multiple PDF files
Two extraction methods for maximum compatibility
Detailed logging of extraction process
Combines all tables from a PDF into a single CSV file
Maintains original filename (just changes extension to .csv)
Requirements
Python 3.6+
Java Runtime Environment (JRE) - required for tabula-py
Required Python packages:
pandas
pdfplumber
tabula-py
glob
logging
Installation
Clone this repository:
Install the required Python packages:
Ensure Java is installed on your system (required by tabula-py)
Usage
Place your PDF files in the same directory as the script or specify the directory in the code
Run the script:
How It Works
The script finds all PDF files in the current directory
For each PDF, it:
Tries to extract tables using tabula-py
If that fails, it uses pdfplumber as a fallback
Combines all tables into a single DataFrame
Saves the result as a CSV file with the same name as the PDF
Troubleshooting
If you see ImportError: cannot import name 'read_pdf' from 'tabula', make sure you've installed tabula-py, not tabula
If tabula-py extraction fails, check that Java is properly installed
If both extraction methods fail, your PDF may not contain extractable tables
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
