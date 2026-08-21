import os
import shutil
import zipfile

import hashlib
import os

def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def calculate_zip_checksum(zip_path):
    # Create a temp folder to extract the zip
    # Generate a random id for the temp folder
    temp_folder = f'/tmp/{os.urandom(8).hex()}'
    os.makedirs(temp_folder)
    checksums = {}
    # Extract the zip to the temp folder
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            file_path = zip_ref.extract(file_info.filename, path='temp_extract_folder')
            checksums[file_info.filename] = calculate_hash(file_path)
    # Clean up the temp folder
    shutil.rmtree(temp_folder)
    # Order the checksums by the file path
    ordered_checksums = {k: v for k, v in sorted(checksums.items(), key=lambda item: item[0])}
    # Create a checksum of the checksums
    checksum = hashlib.sha256(str(ordered_checksums).encode()).hexdigest()
    return checksum  

def create_zip_from_folder(source, target, include_root=False):
    print(f'creating ZIP artifact from {source} to {target}')
    # Create the target directory if it does not exist
    target_dir = os.path.dirname(target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Create a temporary folder to hold the source files
    temp_folder = os.path.join(target_dir, '__temp__')
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)

    try:
        # Copy the source folder to the temporary folder
        base_folder = os.path.basename(source)
        shutil.copytree(source, os.path.join(temp_folder, base_folder))

        # Create the zip file
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_path = os.path.relpath(file_path, temp_folder)
                    if not include_root:
                        zip_path = zip_path.replace(f'{base_folder}/', '')
                    zipf.write(file_path, zip_path)

    finally:
        # Clean up the temporary folder
        shutil.rmtree(temp_folder)