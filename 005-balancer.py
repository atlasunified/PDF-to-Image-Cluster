import os
import shutil
from collections import deque

def balance_folders():
    folders = ['tmp', 'tmp1', 'tmp2', 'tmp3']
    all_pdfs = []

    # Get all PDFs from all folders
    for folder in folders:
        for filename in os.listdir(folder):
            if filename.endswith('.pdf'):
                all_pdfs.append(os.path.join(folder, filename))

    # Sort all PDFs so we don't change the order too much
    all_pdfs.sort()

    # Redistribute PDFs evenly
    for i, pdf_file in enumerate(all_pdfs):
        target_folder = folders[i % len(folders)]
        target_file = os.path.join(target_folder, os.path.basename(pdf_file))

        # If the PDF is not already in the right folder, move it
        if pdf_file != target_file:
            shutil.move(pdf_file, target_file)

if __name__ == "__main__":
    balance_folders()
