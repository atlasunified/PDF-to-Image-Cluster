import os
import tarfile
import webdataset as wds
import shutil  # Import the shutil module

def create_webdataset(directory, output_file):
    # Count total files
    total_files = sum([len(files) for r, d, files in os.walk(directory)])

    processed_files = 0
    with tarfile.open(output_file, "w:") as tar:
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                tar.add(filepath, arcname=os.path.relpath(filepath, directory))

                # Update and print the progress
                processed_files += 1
                progress_percentage = (processed_files / total_files) * 100
                print(f'Progress: {progress_percentage:.2f}%')

    # Delete the entire directory
    shutil.rmtree(directory)

# Usage
directory = "image-text-bbox-cluster2"
output_file = "output.tar"
create_webdataset(directory, output_file)
