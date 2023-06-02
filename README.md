# PDF-to-Image-Cluster

The scripts collectively serve to automate the process of downloading, converting, and processing various files from web sources. They incorporate features such as file management, web scraping, data conversion, concurrent processing, text extraction, URL downloading, file archiving, and file distribution balancing.

## File Outline

000-downloader.py is responsible for downloading files (specifically .snappy.parquet files) from a base URL. It creates the directory if it doesn't exist and downloads the files into the specified directory. It also handles large file downloads by downloading in chunks.

001-parquet-to-csv.py converts Parquet files to CSV format. It navigates through the specified directory, identifies the Parquet files, reads them into a pandas dataframe, and writes them into a CSV file. The original Parquet files are then deleted.

002-url-extractor.py extracts URLs from CSV files in a specified directory. Unique URLs are stored in a set, converted to a DataFrame, and divided into 50 equal parts. These chunks are written to separate CSV files in an output directory.

003-Main.py handles the processing of PDF files within a directory. PDFs are sorted by size and processed concurrently, with Optical Character Recognition (OCR) extracting text and bounding boxes from the PDFs. The results are saved and the original PDF files are deleted. An error handling mechanism is included for failed processing attempts.

004-tarballer.py archives files in a directory (and its subdirectories) into a tar file. The progress of the archiving process is calculated and printed for each file added to the tar file. The original directory and its contents are then deleted.

005-balancer.py balances the distribution of PDF files across several folders. It sorts all PDF files and redistributes them evenly among the folders. If the script is run as the main module, it calls the balance_folders() function.

## Project Summary

This project comprises a series of Python scripts designed to download, process, and manage datasets in various formats. The scripts are summarized as follows:

000-downloader.py: This script scrapes a specified webpage for links ending in .snappy.parquet, downloads the linked files into a specified directory, and creates the directory if it doesn't exist.

001-parquet-to-csv.py: This script converts Parquet files into CSV format. It reads the files into a pandas DataFrame, writes the DataFrame to a CSV file, and then removes the original Parquet file.

002-url-extractor.py: This script extracts URLs from CSV files. It reads the CSV files, appends the URLs to a set (ignoring duplicates), and then splits the set of URLs into 50 parts, each written to a separate CSV file.

003-download.py: This script downloads PDF files from a list of URLs. It checks for several conditions, such as whether the file has already been downloaded, the file size, and the number of pages in the PDF, before downloading the file. It also uses a ThreadPoolExecutor to download multiple PDFs in parallel.

003-Main.py: This script processes PDF files using OCR. It sorts the PDF files by size, converts them into images, extracts text and bounding boxes from the images, and then saves the results. The PDF files are processed concurrently using a process pool executor.

004-tarballer.py: This script creates a tarball (a compressed archive file) from a directory. It counts the total number of files in the directory and its subdirectories, adds the files to the tarball, and then deletes the original directory and its contents.

005-balancer.py: This script balances the distribution of PDF files across several folders. It collects the paths of all PDF files, sorts them, and then redistributes them evenly across the folders.

Each script has been carefully designed to handle exceptions and print informative error or success messages. Together, they form a robust pipeline for downloading, converting, and managing datasets.

## Order of Execution

This project is designed to be run in a specific sequence for optimal efficiency and resource usage. Here's the recommended order of execution:

000-downloader.py: This script initiates the pipeline by downloading all .snappy.parquet files linked from a specified webpage. It creates the necessary directories if they do not exist.

001-parquet-to-csv.py: This script converts the downloaded Parquet files into CSV files. It also removes the original Parquet files to save space.

002-url-extractor.py: This script extracts URLs from the converted CSV files. These URLs are subsequently used for downloading PDF files.

003-download.py: It's important to note that this script should be run with just one CSV file from the cc-strip directory at a time. This prevents your system from becoming overwhelmed with too many simultaneous downloads. This step will also create 4 temporary folders.

005-balancer.py: Before running the main processing script, run this script to ensure the PDF files are evenly distributed across the four temporary folders. This is particularly beneficial if you're using a High Performance Computing (HPC) Cluster, as it facilitates an even distribution of workload.

003-main.py, 003-main1.py, 003-main2.py, 003-main3.py: Finally, these scripts can be run concurrently. They perform OCR processing on the PDF files, generating text and bounding box information from the files.

Running these scripts in this order will ensure a smooth, efficient workflow. Remember to monitor your system's resource usage, particularly when downloading and processing large numbers of files.

## Web Scraping and Download Script - 000-downloader.py

Follow these steps for the execution of the script:

1. Define the `base_url`, `page_url`, and the `download_path` for the files.

2. Check if the directory specified by `download_path` exists.

3. If it does not exist, create the directory and print a message saying `"Directory [download_path] created"`.

4. Call the `scrape_and_download()` function, passing the `base_url`, `page_url`, and `download_path` as arguments. This function does the following:
   - (a) Sends a GET request to the `page_url` and parses the page content with BeautifulSoup.
   - (b) Finds all `<a>` tags in the parsed HTML (these tags usually contain hyperlinks).
   - (c) For each `<a>` tag:
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
   - (a) Tries to:
     - (i) Generate the csv filepath.
     - (ii) Read the parquet file into a pandas dataframe.
     - (iii) Write the dataframe to a csv file, specify escape character.
     - (iv) Print a success message indicating the successful conversion from Parquet to CSV.
     - (v) Remove the original parquet file.
     - (vi) Print a success message indicating the successful deletion of the Parquet file.
   - (b) If any exception occurs during Steps 2.a.i-2.a.vi, it prints an error message.

3. Define a directory string `cc-data`.

4. For each filename in the directory:
   - (a) If the filename ends with '.parquet':
     - (i) Call the `parquet_to_csv()` function on the file.

5. End of process for each Parquet file.

6. End of program.

7. End

## URL Extraction Script - 002-url-extractor.py

Follow these steps for the execution of the script:

1. Start

2. Define the function `extract_urls()`, which:
   - (a) Tries to:
     - (i) Read the csv file with specified encoding and columns.
     - (ii) Append URLs to the passed in set (duplicates will be ignored).
     - (iii) Print a success message indicating the successful extraction of URLs from the CSV file.
   - If any exception occurs during Steps 2.a.i-2.a.iii, it prints an error message.
   - Return the updated set.

3. Define a directory string `cc-data`.

4. Create an empty set to store unique URLs, named `urls_set`.

5. For each filename in the directory:
   - (a) If the filename ends with '.csv':
     - (i) Call the `extract_urls()` function on the file and update `urls_set`.

6. End of process for each CSV file.

7. Convert the `urls_set` to a DataFrame named `urls_df`.

8. Define the output directory string `cc-strip`.

9. Create the output directory if it doesn't exist.

10. Split `urls_df` into 50 equal parts and store them in `chunks`.

11. For each chunk in `chunks`:
    - (a) Write the chunk to a separate CSV file in the output directory.

12. End of process for each chunk.

13. Print a success message indicating the successful writing of unique URLs to the output directory.

14. End of program.

15. End

## PDF Download Script - 003-download.py

Follow these steps for the execution of the script:

1. Start

2. Import necessary libraries and modules.

3. Define `folders` and `downloaded_files`. Set a cyclic iterator on the `folders`.

4. Define the `download_pdf()` function:
   - (a) Extract URL and folder from the input tuple.
   - (b) Try to download the PDF:
     - (i) Extract the filename from the URL.
     - (ii) If the filename is already in the set of downloaded files, print a message and return None.
     - (iii) Open the URL and get the file size from the response header.
     - (iv) If the file size is more than 5MB, print a message and return None.
     - (v) Retrieve the file from the URL and save it in the corresponding folder.
     - (vi) Open the file with PyPDF2 and check the number of pages. If there are more than 20 pages, print a message, remove the file, and return None.
     - (vii) If all checks are passed, add the filename to the set of downloaded files, print a success message, and return the file path.
     - (viii) If there is an exception at any point, print an error message and return None.

5. Define the `process_urls()` function:
   - (a) Try to read the CSV file into a pandas DataFrame and extract the URLs.
   - (b) Pair each URL with a folder from the cyclic iterator.
   - (c) Use a ThreadPoolExecutor to download each PDF in parallel using the `download_pdf()` function.
   - (d) If there is an exception at any point, print an error message.

6. If the script is run as the main module:
   - (a) Create all folders if they don't exist.
   - (b) Get the list of all CSV files in the specified directory.
   - (c) If there are any CSV files, process each one with the `process_urls()` function.
   - (d) If there are no CSV files, print a message.

7. End


## PDF Processing Script - 003-main.py

Follow these steps for the execution of the script:

1. Start

2. Define a directory string `tmp`.

3. Check if the `tmp` directory exists.

4. If the directory does not exist, print a message indicating that the directory does not exist, and go to Step 15 (End).

5. If the directory does exist, retrieve a list of PDF files within the directory, including any subdirectories.

6. If there are no PDF files in the directory, print a message saying "No PDF files found in the directory", and go to Step 15 (End).

7. If there are PDF files, sort them by size (from smallest to largest).

8. Create a process pool executor to handle multiple tasks concurrently.

9. For each PDF file, submit a task to the executor which calls the `main()` function, passing in the PDF file and a string which will serve as the output folder.

10. For each future in the order they complete:
    - (a) If the future resulted in an exception, print a message saying "[PDF file] generated an exception: [exception details]".
    - (b) If the future completed without error, print a message saying "[PDF file] processed successfully".
    - (c) Repeat Step 10 until all futures are processed.

11. The `main()` function:
    - (a) Checks if the OCR result for the current PDF file already exists. If it does, it prints a message, removes the PDF file, and ends.
    - (b) If the OCR result doesn't exist, it tries to:
      - (i) Convert the PDF to images (randomly sized snapshots between 336 and 768 pixels).
      - (ii) Extract text and bounding boxes from the images using OCR. The OCR results include both the bounding boxes coordinates (normalized to the size of the snapshot image) and the associated text.
      - (iii) Save the results. For each snapshot, it saves both the image and a text file containing the bounding box and text data. The image is saved in PNG format, and if no bounding boxes were found for the snapshot, both the image and the text file are deleted. Otherwise, the snapshot image is resized to a size of 336x336 pixels before being saved.
      - (iv) Move the processed files to a new location.
    - (c) If any error occurs during Steps 11.b.i-11.b.iv, it prints an error message, removes the PDF file, and ends.
    - (d) If no errors occur, it removes the PDF file and ends.

12. End of `main()`

13. End of process for each PDF file.

14. End of program.

15. End

## Tarball Creation Script - 004-tarballer.py

Follow these steps for the execution of the script:

1. Start

2. Define the directory name as `image-text-bbox-cluster` and the output file name as `output.tar`.

3. Call the `create_webdataset()` function, passing the directory and output file names as parameters.

4. In the `create_webdataset()` function:
   - (a) Count the total number of files in the directory and all its subdirectories.
   - (b) Initialize a count of processed files at zero.
   - (c) Open the output file as a tar file for writing.
   - (d) For each file in the directory and its subdirectories:
     - (i) Generate the file's full path.
     - (ii) Add the file to the tar file, preserving the file's relative path within the directory.
     - (iii) Increment the count of processed files.
     - (iv) Calculate the progress as a percentage of the total number of files.
     - (v) Print the progress.
   - (e) After all files have been added to the tar file, close the tar file.
   - (f) Delete the original directory and all its contents.

5. End

## Folder Balancing Script - 005-balancer.py

Follow these steps for the execution of the script:

1. Start

2. Define the `balance_folders()` function.

3. In the `balance_folders()` function:
   - (a) Define the names of the folders that need to be balanced as 'tmp', 'tmp1', 'tmp2', 'tmp3'.
   - (b) Initialize an empty list to store the paths of all PDF files.
   - (c) For each folder:
     - (i) For each file in the folder:
       - If the file ends with '.pdf', append its path to the list of all PDF files.
   - (d) Sort all PDF files to maintain the order.
   - (e) Redistribute the PDF files evenly across the folders:
     - (i) For each index and PDF file in the sorted list:
       - Determine the target folder based on the index and the number of folders.
       - Generate the target file path in the target folder.
       - If the PDF file is not already in the target folder, move it there.

4. If the script is run as the main module, call the `balance_folders()` function.

5. End
