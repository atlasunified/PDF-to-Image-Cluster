import os
from pdf2image import convert_from_path
from PIL import Image
import torch
import easyocr
import cv2
import numpy as np
from paddleocr import PaddleOCR

## USE THIS TO IMPLEMENT YOUR GPU
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# torch.cuda.init()

input_folder = 'output-images'
output_folder = 'output-image-text'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'], gpu=True)
## SAME HERE
# reader = easyocr.Reader(['en'], device=device)

# Iterate through the images in the input folder
for image_file in os.listdir(input_folder):
    if image_file.endswith('.png') or image_file.endswith('.jpg'):
        input_path = os.path.join(input_folder, image_file)

        # Perform OCR on the image
        result = reader.readtext(input_path)

        # Extract the recognized text
        text = '\n'.join([item[1] for item in result])

        # Save the text to the output folder
        text_file = f"{os.path.splitext(image_file)[0]}_txt.txt"
        text_path = os.path.join(output_folder, text_file)
        with open(text_path, 'w') as f:
            f.write(text)

input_folder = 'output-images'
output_folder = 'output-image-bb'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize the PaddleOCR model
ocr = PaddleOCR(lang='en')

# Iterate through the images in the input folder
for image_file in os.listdir(input_folder):
    if image_file.endswith('.png') or image_file.endswith('.jpg'):
        input_path = os.path.join(input_folder, image_file)
        img = cv2.imread(input_path)

        # Perform OCR on the image
        result = ocr.ocr(img)

        # Draw bounding boxes around the recognized text
        for line in result:
            box = line[0]
            text = line[1][0]
            box_points = np.array([[int(point[0]), int(point[1])] for point in box], np.int32)
            cv2.polylines(img, [box_points], True, (0, 255, 0), 2)
            cv2.putText(img, text, tuple(box_points[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Save the image with bounding boxes
        output_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_bbox.jpg")
        cv2.imwrite(output_path, img)