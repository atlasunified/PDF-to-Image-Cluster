# PDF-to-Image-Cluster

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
