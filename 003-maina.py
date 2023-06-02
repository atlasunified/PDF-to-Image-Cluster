import concurrent.futures
import os
import shutil
import numpy as np
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
import random
from PIL import Image

def convert_pdf_to_images(pdf_path, min_snapshot_size=336, max_snapshot_size=768):
    pages = convert_from_path(pdf_path)
    snapshots = [extract_snapshots(page, random_snapshot_size(min_snapshot_size, max_snapshot_size)) for page in pages]
    return snapshots

def random_snapshot_size(min_size, max_size):
    snapshot_size = random.randint(min_size, max_size)
    return (snapshot_size, snapshot_size)

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
            page_result.extend(result)
        results.append(page_result)
    return results

def save_snapshot_image(image, snapshot_idx, output_dir):
    image_path = f"{output_dir}/snapshot_{snapshot_idx:03}.png"
    image.save(image_path)

def save_results(snapshots, text_and_boxes, output_folder, resized_size=(336, 336)):
    os.makedirs(output_folder, exist_ok=True)

    snapshot_counter = 0
    for page, (page_snapshots, page_result) in enumerate(zip(snapshots, text_and_boxes), start=1):
        with open(f"{output_folder}/page_{page:03}.txt", "w") as output_file:
            output_file.write(f"Page {page}:\n")
            for snapshot_idx, (snapshot_image, result) in enumerate(zip(page_snapshots, page_result)):
                output_file.write(f"snapshot_{snapshot_counter + 1}:\n")
                
                image_path = f"{output_folder}/snapshot_{snapshot_counter:03}.png"
                save_snapshot_image(snapshot_image, snapshot_counter, output_folder)
                
                img_width, img_height = snapshot_image.size
                
                bb_file_path = f"{output_folder}/snapshot_{snapshot_counter:03}_bb.txt"
                with open(bb_file_path, "w") as bb_file:
                    for line in result:
                        if len(line) >= 2 and len(line[1]) > 0:
                            bbox = [[coord[0] / img_width, coord[1] / img_height] for coord in line[0]]
                            text = line[1][0]
                            bb_file.write(f"Bounding box: {bbox}, Text: {text}\n")
                    bb_file.flush()
                    os.fsync(bb_file.fileno())
                
                if os.stat(bb_file_path).st_size == 0:
                    os.remove(bb_file_path)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                else:
                    with Image.open(image_path) as img:
                        resized_img = img.resize(resized_size)
                        resized_img.save(image_path)
                        
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

# Removed URL processing and download functions

def main(pdf_path, output_folder):
    # Get the basename of the PDF file (without the '.pdf' extension)
    pdf_basename = os.path.basename(pdf_path).rsplit('.', 1)[0]
    
    # Check if the OCR result for this PDF file already exists
    if os.path.exists(os.path.join('pdf-img-cluster', pdf_basename)):
        print(f"Skipping {pdf_path} because it has already been OCR'd.")
        
        # Remove the processed PDF file
        os.remove(pdf_path)
        return

    try:
        snapshots = convert_pdf_to_images(pdf_path)
        text_and_boxes = extract_text_and_boxes(snapshots)
        save_results(snapshots, text_and_boxes, output_folder)
        move_files('output-images', output_folder)
    except Exception as e:
        print(f"Failed to process {pdf_path} due to error: {str(e)}")
        # If the PDF file is corrupted or unreadable, delete it
        os.remove(pdf_path)
        return

    # Remove the processed PDF file
    os.remove(pdf_path)

if __name__ == "__main__":
    # Directory containing the PDF files
    directory = 'tmp'

    if os.path.exists(directory):
        # Get the list of PDF files, including those in subdirectories
        pdf_files = [os.path.join(dirpath, filename)
                     for dirpath, dirnames, filenames in os.walk(directory)
                     for filename in filenames if filename.endswith('.pdf')]

        if pdf_files:
            # Order the PDF files by size (smallest first)
            pdf_files.sort(key=os.path.getsize)

            # Use a process pool to process each PDF file
            with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = {executor.submit(main, pdf_file, 'image-text-bbox-cluster2/' + os.path.basename(pdf_file).split('.')[0]): pdf_file for pdf_file in pdf_files}
                
                for future in concurrent.futures.as_completed(futures):
                    pdf_file = futures[future]
                    try:
                        future.result()  # If the function completed without error, this will be None
                    except Exception as exc:
                        print(f'{pdf_file} generated an exception: {exc}')
                    else:
                        print(f'{pdf_file} processed successfully')
        else:
            print("No PDF files found in the directory.")
    else:
        print(f"The directory {directory} does not exist.")
