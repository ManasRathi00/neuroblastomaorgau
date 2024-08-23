import os
from dotenv import load_dotenv
import pandas as pd
from pyairtable import Api
import numpy as np

# Load environment variables from .env file
load_dotenv()

api = Api(api_key=os.environ['AIRTABLE_API_KEY'])

def upsert_csv_to_airtable(csv_file_path, airtable_base_id = os.environ['BASE_ID'], api_key = os.environ['AIRTABLE_API_KEY']):
    # Extract the base filename without the directory or extension
    required_file_name = os.path.basename(csv_file_path).replace(".csv", "")
    print(csv_file_path)
    # # Read the CSV file
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
    df.replace({np.nan: None, np.inf: None, -np.inf: None}, inplace=True)
    # Initialize Airtable
    table = api.table(base_id=airtable_base_id, table_name= required_file_name)
    # # Upsert records to Airtable
    for index, row in df.iterrows():
        record_data = row.to_dict()
        print(record_data)
        try:
            table.create(record_data)
        except:
            print("Failure in creating record")

    #     # Search for a matching record
    #     matching_records = table.search(primary_key, record_data[primary_key])
        
    #     if matching_records:
    #         # Update existing record
    #         record_id = matching_records[0]['id']
    #         airtable.update(record_id, record_data)
    #     else:
    #         # Insert new record
    #         airtable.insert(record_data)