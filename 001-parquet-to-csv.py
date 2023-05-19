import os
import pandas as pd
import pyarrow.parquet as pq

def parquet_to_csv(parquet_filepath):
    try:
        # Generate the csv filepath
        csv_filepath = parquet_filepath.replace('.parquet', '.csv')
        
        # Read the parquet file
        dataframe = pd.read_parquet(parquet_filepath)
        
        # Write to a csv file, specify escape character
        dataframe.to_csv(csv_filepath, index=False, escapechar='\\')
        print(f'Successfully converted {parquet_filepath} to {csv_filepath}')
        
        # Remove the parquet file
        os.remove(parquet_filepath)
        print(f'Successfully deleted {parquet_filepath}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Directory containing the parquet files
directory = 'cc-data'

# Convert all parquet files in the directory to csv and delete them
for filename in os.listdir(directory):
    if filename.endswith('.parquet'):
        parquet_to_csv(os.path.join(directory, filename))
