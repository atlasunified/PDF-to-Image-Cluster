import os
import pandas as pd
import urllib.request
import concurrent.futures
import itertools

from PyPDF2 import PdfFileReader

folders = ['tmp', 'tmp1', 'tmp2', 'tmp3']
downloaded_files = set()
folder_cycle = itertools.cycle(folders)  # create a cycle iterator for the folders

def download_pdf(data):
    url, folder = data
    try:
        filename = url.split("/")[-1]
        if filename in downloaded_files:
            print(f'Skipping {filename} as it has already been downloaded.')
            return None

        response = urllib.request.urlopen(url)
        file_size = int(response.headers['Content-Length'])
        max_size = 5 * 1024 * 256  # 1.1MB in bytes

        if file_size > max_size:
            print(f'Skipping file from {url} because it is larger than 5MB')
            return None

        filepath = f'{folder}/{filename}'
        urllib.request.urlretrieve(url, filepath)
        
        with open(filepath, 'rb') as file:
            pdf = PdfFileReader(file)
            page_count = pdf.getNumPages()

            if page_count > 20:
                print(f'Skipping file from {url} because it has more than 20 pages')
                os.remove(filepath)
                return None

        downloaded_files.add(filename)
        print(f'Successfully downloaded file from {url} to {filepath}')
        return filepath  # Return filepath on success
    except Exception as e:
        print(f'Error downloading file from {url}: {e}')
        return None  # Return None on failure

def process_urls(csv_filepath):
    try:
        dataframe = pd.read_csv(csv_filepath)
        urls = dataframe['URL']
        urls_folders = [(url, next(folder_cycle)) for url in urls]  # pair each url with a folder
        with concurrent.futures.ThreadPoolExecutor() as executor:
            filenames = list(executor.map(download_pdf, urls_folders))
    except Exception as e:
        print(f'An error occurred while processing the URLs in {csv_filepath}: {e}')

if __name__ == "__main__":
    directory = 'cc-strip'

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    csv_files = [filename for filename in os.listdir(directory) if filename.endswith('.csv')]

    if csv_files:
        for filename in csv_files:
            process_urls(os.path.join(directory, filename))
    else:
        print("No CSV files found in the directory.")
