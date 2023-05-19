import os
import pandas as pd
import numpy as np

def extract_urls(csv_filepath, urls_set):
    try:
        # Read the csv file with specified encoding
        dataframe = pd.read_csv(csv_filepath, usecols=[1], encoding='utf-8')

        # Append URLs to the set (duplicates will be ignored)
        for url in dataframe.iloc[:, 0]:
            urls_set.add(str(url))
        print(f'Successfully extracted URLs from {csv_filepath}')
    except Exception as e:
        print(f'An error occurred: {e}')

    return urls_set


# Directory containing the CSV files
directory = 'cc-data'

# Create an empty set to store unique URLs
urls_set = set()

# Extract all URLs from all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        urls_set = extract_urls(os.path.join(directory, filename), urls_set)

# Convert the set to a DataFrame
urls_df = pd.DataFrame(list(urls_set), columns=['URL'])

# Define the output directory
output_dir = 'cc-strip'
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Split the DataFrame into 50 equal parts
chunks = np.array_split(urls_df, 50)

# Write each chunk to a separate CSV file in the output directory
for i, chunk in enumerate(chunks, 1):
    chunk_filepath = os.path.join(output_dir, f'unique_urls_{i}.csv')
    chunk.to_csv(chunk_filepath, index=False, encoding='utf-8')

print(f'Successfully written unique URLs to {output_dir}')

