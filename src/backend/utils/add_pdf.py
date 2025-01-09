import shutil
import os

def add_pdf(file_path):
    target_dir = "../../test_data/input"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    shutil.copy(file_path, target_dir)
    print(f"PDF added to {target_dir}")
