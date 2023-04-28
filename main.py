import os
import shutil
import numpy as np
from pdf2image import convert_from_path
from paddleocr import PaddleOCR

def extract_snapshots(image, snapshot_size=(512, 512)):
    width, height = image.size
    snapshots = []
    for y in range(0, height, snapshot_size[1]):
        for x in range(0, width, snapshot_size[0]):
            snapshot = image.crop((x, y, x + snapshot_size[0], y + snapshot_size[1]))
            snapshots.append(snapshot)
    return snapshots

def convert_pdf_to_images(pdf_path, snapshot_size=(512, 512)):
    pages = convert_from_path(pdf_path)
    snapshots = [extract_snapshots(page, snapshot_size) for page in pages]
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

def save_results(snapshots, text_and_boxes):
    output_dir = "output-images"
    os.makedirs(output_dir, exist_ok=True)

    snapshot_counter = 0
    for page, (page_snapshots, page_result) in enumerate(zip(snapshots, text_and_boxes), start=1):
        with open(f"{output_dir}/page_{page:03}.txt", "w") as output_file:
            output_file.write(f"Page {page}:\n")
            for snapshot_idx, (snapshot_image, result) in enumerate(zip(page_snapshots, page_result)):
                output_file.write(f"snapshot_{snapshot_counter + 1}:\n")
                
                # Save snapshot image
                save_snapshot_image(snapshot_image, snapshot_counter, output_dir)
                
                # Save bounding box and text information
                with open(f"{output_dir}/snapshot_{snapshot_counter:03}_bb.txt", "w") as bb_file:
                    for line in result:
                        if len(line) >= 2 and len(line[1]) > 0:
                            bbox, text = line[0], line[1][0]
                            bb_file.write(f"Bounding box: {bbox}, Text: {text}\n")
                
                snapshot_counter += 1

            output_file.write("\n")

def move_files(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        shutil.move(src_path, dst_path)

def main(pdf_path):
    snapshots = convert_pdf_to_images(pdf_path)
    text_and_boxes = extract_text_and_boxes(snapshots)
    save_results(snapshots, text_and_boxes)
    input_folder = 'output-images'
    output_folder = 'output-image-text'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through the bounding box files in the input folder
    for bb_file in os.listdir(input_folder):
        if bb_file.endswith('_bb.txt'):
            input_path = os.path.join(input_folder, bb_file)

            # Load the bounding boxes and texts
            with open(input_path, 'r') as f:
                bbox_texts = [line.strip() for line in f.readlines()]

            # Save the text to the output folder
            text_file = f"{os.path.splitext(bb_file)[0]}_txt.txt"
            text_path = os.path.join(output_folder, text_file)
            with open(text_path, 'w') as f:
                for bbox_text in bbox_texts:
                    f.write(f"{bbox_text}\n")

    # Move files from 'output-images' and 'output-image-text' to 'image-text-bbox-cluster'
    final_output_dir = 'image-text-bbox-cluster'
    move_files(input_folder, final_output_dir)
    move_files(output_folder, final_output_dir)

if __name__ == "__main__":
    pdf_path = "testpdf.pdf"
    main(pdf_path)