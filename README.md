# PDF-to-Image-Cluster

## Web Scraping and Download Script

Follow these steps for the execution of the script:

1. Define the `base_url`, `page_url`, and the `download_path` for the files.

2. Check if the directory specified by `download_path` exists.

3. If it does not exist, create the directory and print a message saying `"Directory [download_path] created"`.

4. Call the `scrape_and_download()` function, passing the `base_url`, `page_url`, and `download_path` as arguments. This function does the following:
   - Sends a GET request to the `page_url` and parses the page content with BeautifulSoup.
   - Finds all `<a>` tags in the parsed HTML (these tags usually contain hyperlinks).
   - For each `<a>` tag:
     - Get the 'href' attribute of the tag, which usually represents the URL of the linked resource.
     - If the URL ends with `.snappy.parquet`, create the full URL of the file by joining the `base_url` and the URL from the 'href' attribute.
     - Print a message saying `"Downloading [full_url]"`.
     - Call the `download_file()` function with the full URL and the `download_path` as arguments. This function does the following:

5. Splits the URL to extract the filename and joins it with the `download_path`.

6. Sends a GET request to the URL with `stream=True` to download the file in chunks instead of all at once (this is beneficial for large files).

7. If the request is successful, it opens the file in write and binary modes, and writes each chunk of data into the file.

8. If any error occurs during the request, it will raise an `HTTPError`.

9. Once all chunks have been written, it returns the filename.

10. Once all `<a>` tags have been processed and all matching files have been downloaded, the script ends.

11. End.
