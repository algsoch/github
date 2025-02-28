import os
import pandas as pd
import pdfplumber
import glob
import logging
# Fix the import statement
import tabula

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_pdf_to_csv(pdf_path):
    """
    Convert a PDF file to a CSV file with the same base name.
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Generate output file path
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.dirname(pdf_path)
        csv_path = os.path.join(output_dir, f"{base_name}.csv")
        
        logger.info(f"Converting {pdf_path} to {csv_path}")
        
        # Try tabula-py first
        try:
            # Read all tables from the PDF with tabula - fixed function call
            all_tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
            
            if all_tables and len(all_tables) > 0:
                # Combine all tables into one DataFrame
                combined_df = pd.concat(all_tables, ignore_index=True)
                
                # Save to CSV
                combined_df.to_csv(csv_path, index=False)
                logger.info(f"Successfully converted {pdf_path} to {csv_path} using tabula-py")
                return True
        except Exception as e:
            logger.warning(f"Tabula extraction failed: {e}. Trying pdfplumber...")
        
        # If tabula fails, try pdfplumber
        all_data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                
                for table in tables:
                    if table:
                        # Convert the table to pandas DataFrame
                        if len(table) > 0:
                            headers = table[0]
                            data = table[1:]
                            df = pd.DataFrame(data, columns=headers)
                            all_data.append(df)
        
        # If we found tables with pdfplumber
        if all_data:
            # Combine all tables into one DataFrame
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Save to CSV
            combined_df.to_csv(csv_path, index=False)
            logger.info(f"Successfully converted {pdf_path} to {csv_path} using pdfplumber")
            return True
        else:
            logger.warning(f"No tables found in {pdf_path}")
            return False
            
    except Exception as e:
        logger.error(f"Error converting {pdf_path}: {e}")
        return False

def main():
    """
    Main function to find and convert PDF files
    """
    # Directory containing PDF files (current directory)
    pdf_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all PDF files in the directory
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {pdf_dir}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to convert")
    
    # Convert each PDF file to CSV
    for pdf_file in pdf_files:
        convert_pdf_to_csv(pdf_file)
    
    logger.info("PDF to CSV conversion complete")

if __name__ == "__main__":
    main()