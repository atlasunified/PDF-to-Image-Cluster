import os
import shutil
import numpy as np
import pandas as pd
import urllib.request
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
from PIL import Image

def convert_pdf_to_images(pdf_path, snapshot_size=(512, 512)):
    pages = convert_from_path(pdf_path)
    snapshots = [extract_snapshots(page, snapshot_size) for page in pages]
       
    return snapshots

def extract_snapshots(image, snapshot_size=(512, 512)):
    width, height = image.size
    snapshots = []
    for y in range(0, height, snapshot_size[1]):
        for x in range(0, width, snapshot_size[0]):
            snapshot = image.crop((x, y, x + snapshot_size[0], y + snapshot_size[1]))
            snapshots.append(snapshot)
    return snapshots

def extract_text_and_boxes(snapshots):
    ocr = PaddleOCR(lang='en', show_log=False)
    results = []
    for page_snapshots in snapshots:
        page_result = []
        for img in page_snapshots:
            img_array = np.array(img)
            result = ocr.ocr(img_array)
            # Flatten the result and extend the page_result list.
            page_result.extend(result)
        results.append(page_result)
    return results


def save_snapshot_image(image, snapshot_idx, output_dir):
    image_path = f"{output_dir}/snapshot_{snapshot_idx:03}.png"
    image.save(image_path)

def save_results(snapshots, text_and_boxes, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    snapshot_counter = 0
    for page, (page_snapshots, page_result) in enumerate(zip(snapshots, text_and_boxes), start=1):
        with open(f"{output_folder}/page_{page:03}.txt", "w") as output_file:
            output_file.write(f"Page {page}:\n")
            for snapshot_idx, (snapshot_image, result) in enumerate(zip(page_snapshots, page_result)):
                output_file.write(f"snapshot_{snapshot_counter + 1}:\n")
                
                # Save snapshot image
                image_path = f"{output_folder}/snapshot_{snapshot_counter:03}.png"
                save_snapshot_image(snapshot_image, snapshot_counter, output_folder)
                
                # Get the dimensions of the snapshot image for normalization
                img_width, img_height = snapshot_image.size
                
                # Save bounding box and text information
                bb_file_path = f"{output_folder}/snapshot_{snapshot_counter:03}_bb.txt"
                with open(bb_file_path, "w") as bb_file:
                    for line in result:
                        if len(line) >= 2 and len(line[1]) > 0:
                            # Normalize bounding box coordinates
                            bbox = [[coord[0] / img_width, coord[1] / img_height] for coord in line[0]]
                            text = line[1][0]
                            bb_file.write(f"Bounding box: {bbox}, Text: {text}\n")
                    bb_file.flush()
                    os.fsync(bb_file.fileno())
                
                # Check if bounding box text file is empty and if so delete it and its corresponding image
                if os.stat(bb_file_path).st_size == 0:
                    os.remove(bb_file_path)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        
                snapshot_counter += 1
            output_file.flush()
            os.fsync(output_file.fileno())

def move_files(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        shutil.move(src_path, dst_path)

def download_pdf(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        print(f'Successfully downloaded file from {url} to {filename}')
        return 'complete'
    except Exception as e:
        print(f'Error downloading file from {url}: {e}')
        return 'error'

def process_urls(csv_filepath):
    try:
        # Read the csv file
        dataframe = pd.read_csv(csv_filepath)

        # Process each URL
        for url in dataframe['URL']:
            filename = url.split("/")[-1]
            output_folder = 'image-text-bbox-cluster/' + filename.split('.')[0] 

            # Download the PDF
            pdf_filepath = f'tmp/{filename}'
            success = download_pdf(url, pdf_filepath)
            if success:
                # Process the PDF
                main(pdf_filepath, output_folder)

                # Move the PDF to the output folder
                shutil.move(pdf_filepath, output_folder)
            else:
                print(f'Skipping URL {url} due to download error')
    except Exception as e:
        print(f'An error occurred while processing the URLs in {csv_filepath}: {e}')


def main(pdf_path, output_folder):
    snapshots = convert_pdf_to_images(pdf_path)
    text_and_boxes = extract_text_and_boxes(snapshots)
    save_results(snapshots, text_and_boxes, output_folder)
    move_files('output-images', output_folder)

if __name__ == "__main__":
    # Directory containing the CSV files
    directory = 'cc-strip'

    # Ensure the temporary directory for downloaded PDFs exists
    os.makedirs('tmp', exist_ok=True)

    csv_files = [filename for filename in os.listdir(directory) if filename.endswith('.csv')]

    if csv_files:
        # Process all URLs in all CSV files in the directory
        for filename in csv_files:
            process_urls(os.path.join(directory, filename))
    else:
        # If there are no CSV files, process all PDF files in the 'tmp' directory directly
        for filename in os.listdir('tmp'):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join('tmp', filename)
                output_folder = 'image-text-bbox-cluster/' + filename.split('.')[0]
                main(pdf_path, output_folder)
