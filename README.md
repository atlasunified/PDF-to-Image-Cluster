# PDF-to-Image-Cluster

## Web Scraping and Download Script - 000-downloader.py

Follow these steps for the execution of the script:

1. Define the `base_url`, `page_url`, and the `download_path` for the files.

2. Check if the directory specified by `download_path` exists.

3. If it does not exist, create the directory and print a message saying `"Directory [download_path] created"`.

4. Call the `scrape_and_download()` function, passing the `base_url`, `page_url`, and `download_path` as arguments. This function does the following:
   - a) Sends a GET request to the `page_url` and parses the page content with BeautifulSoup.
   - b) Finds all `<a>` tags in the parsed HTML (these tags usually contain hyperlinks).
   - c) For each `<a>` tag:
     - (i) Get the 'href' attribute of the tag, which usually represents the URL of the linked resource.
     - (ii) If the URL ends with `.snappy.parquet`, create the full URL of the file by joining the `base_url` and the URL from the 'href' attribute.
     - (iii) Print a message saying `"Downloading [full_url]"`.
     - (iv) Call the `download_file()` function with the full URL and the `download_path` as arguments. This function does the following:

5. Splits the URL to extract the filename and joins it with the `download_path`.

6. Sends a GET request to the URL with `stream=True` to download the file in chunks instead of all at once (this is beneficial for large files).

7. If the request is successful, it opens the file in write and binary modes, and writes each chunk of data into the file.

8. If any error occurs during the request, it will raise an `HTTPError`.

9. Once all chunks have been written, it returns the filename.

10. Once all `<a>` tags have been processed and all matching files have been downloaded, the script ends.

11. End.

## Parquet to CSV Conversion Script - 001-parquet-to-csv.py

Follow these steps for the execution of the script:

1. Start

2. Define the function `parquet_to_csv()`, which:
   - a) Tries to:
     - (i) Generate the csv filepath.
     - (ii) Read the parquet file into a pandas dataframe.
     - (iii) Write the dataframe to a csv file, specify escape character.
     - (iv) Print a success message indicating the successful conversion from Parquet to CSV.
     - (v) Remove the original parquet file.
     - (vi) Print a success message indicating the successful deletion of the Parquet file.
   - b) If any exception occurs during Steps 2.a.i-2.a.vi, it prints an error message.

3. Define a directory string `cc-data`.

4. For each filename in the directory:
   - a) If the filename ends with '.parquet':
     - (i) Call the `parquet_to_csv()` function on the file.

5. End of process for each Parquet file.

6. End of program.

7. End
