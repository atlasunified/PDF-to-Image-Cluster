import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_file(url, download_path):
    local_filename = url.split('/')[-1]
    local_filename = os.path.join(download_path, local_filename)
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

def scrape_and_download(base_url, page_url, download_path):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    for link in soup.find_all('a'):
        url = link.get('href')
        if url and '.snappy.parquet' in url:
            full_url = urljoin(base_url, url)
            print(f'Downloading {full_url}')
            download_file(full_url, download_path)

base_url = 'http://3080.rom1504.fr/n/text/text38M/'
page_url = 'http://3080.rom1504.fr/n/text/text38M/'
download_path = 'cc-data'  # modify this as per your requirements

# Create target Directory if it doesn't exist
if not os.path.exists(download_path):
    os.mkdir(download_path)
    print("Directory " , download_path ,  " created ")

scrape_and_download(base_url, page_url, download_path)
