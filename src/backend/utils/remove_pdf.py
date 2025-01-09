import shutil
import os

def remove_pdf(file_path):
    target_dir = "../../test_data/input"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"PDF removed from {target_dir}")
    else:
        print(f"PDF not found in {target_dir}")
