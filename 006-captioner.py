import os
os.environ["USE_FP16"] = "1"

from transformers import Blip2Processor, Blip2ForConditionalGeneration
from accelerate import Accelerator
import torch
from PIL import Image

# Initialize the transformer model
accelerator = Accelerator()
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
model = accelerator.prepare(model)

def caption_images(image_folder):
    # Initialize the counter
    image_counter = 0

    for dirpath, dirnames, filenames in os.walk(image_folder):
        for filename in filenames:
            if filename.endswith(".png"):
                image_path = os.path.join(dirpath, filename)
                raw_image = Image.open(image_path).convert("RGB")

                # Preprocess the image with Blip2Processor
                inputs = processor(images=raw_image, return_tensors="pt").to(accelerator.device)

                # Generate a caption
                with torch.no_grad():
                    outputs = model.generate(**inputs, max_new_tokens=50)  # I set it to 50, adjust as needed
                caption = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()

                # Save the caption to a .txt file with the same base name as the image file
                base_filename = os.path.splitext(filename)[0]
                caption_filename = f"{base_filename}_cap.txt"
                caption_path = os.path.join(dirpath, caption_filename)

                with open(caption_path, "w") as f:
                    f.write(caption)

                # Increment the counter and print out the current count
                image_counter += 1
                print(f"Images captioned so far: {image_counter}")

if __name__ == "__main__":
    # The rest of your script here
    caption_images('image-text-bbox-cluster')
