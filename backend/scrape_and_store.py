import os
import time
from dotenv import load_dotenv
import pyodbc
import pandas as pd
from scrape import scrape_data  # Import the scrape function

# Load environment variables from .env file
load_dotenv()

# Access environment variables
db_server = os.getenv('DB_SERVER')
db_database = os.getenv('DB_DATABASE')
db_uid = os.getenv('DB_UID')
db_pwd = os.getenv('DB_PWD')

# Function to connect to the database
def connect_to_db():
    return pyodbc.connect(
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={db_server};'
        f'DATABASE={db_database};'
        f'UID={db_uid};'
        f'PWD={db_pwd};'
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30;'
    )

# Retrieve existing data from the database
def get_existing_data(cursor):
    cursor.execute("SELECT [Security Description], [Trades], [TTA], [Open], [High], [Low], [LTP], [LTY] FROM RegularMarket")
    rows = cursor.fetchall()
    # Convert pyodbc.Row objects to a list of tuples
    rows_as_tuples = [tuple(row) for row in rows]
    # Convert to a DataFrame for easier comparison
    existing_data = pd.DataFrame(rows_as_tuples, columns=['Security Description', 'Trades', 'TTA', 'Open', 'High', 'Low', 'LTP', 'LTY'])
    return existing_data

# Compare new scraped data with the existing data in the database
def is_data_changed(scraped_row, existing_data):
    # Check if the scraped row already exists in the database
    existing_row = existing_data[existing_data['Security Description'] == scraped_row[0]]
    
    # If no matching row exists, return True (means data is new)
    if existing_row.empty:
        return True
    
    # Compare each column (except Timestamp)
    for col in ['Trades', 'TTA', 'Open', 'High', 'Low', 'LTP', 'LTY']:
        if existing_row[col].iloc[0] != scraped_row[1]:
            return True
    return False

# Retry mechanism function
def scrape_and_store_with_retry(max_retries=3, delay=5):
    retries = 0
    while retries < max_retries:
        try:
            # Get scraped data from scrape.py
            scraped_data = scrape_data()

            if not scraped_data:
                raise ValueError("Scrape results are empty.")
            
            # Connect to DB and get existing data
            conn = connect_to_db()
            cursor = conn.cursor()
            existing_data = get_existing_data(cursor)  # Fetch existing data from the database
            
            print("Storing scraped data into Azure DB")
            
            for data_row in scraped_data:
                # Check if the data has changed by comparing it to the existing data
                if is_data_changed(data_row, existing_data):
                    print(f"Inserting new data for {data_row[0]}")
                    cursor.execute(
                        """
                        INSERT INTO RegularMarket 
                        ([Security Description], [Trades], [TTA], [Open], [High], [Low], [LTP], [LTY])
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        data_row[0], data_row[1], data_row[2], 
                        data_row[3], data_row[4], data_row[5], data_row[6], data_row[7]
                    )
            
            # Commit the transaction and close the connection
            conn.commit()
            print("Data successfully stored onto Azure DB.")
            cursor.close()
            conn.close()
            break  # Exit loop if successful
            
        except Exception as e:
            print(f"Error during scraping or storing data: {e}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying... {retries}/{max_retries}")
                time.sleep(delay)  # Wait before retrying
            else:
                print("Maximum retries reached. Exiting script.")
                exit(1)  # Exit with a non-zero status code if max retries reached

# Call the retry function
scrape_and_store_with_retry(max_retries=3, delay=5)
