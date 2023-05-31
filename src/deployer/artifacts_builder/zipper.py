import os
import shutil
import zipfile

def create_zip_from_folder(source, target, include_root=False):
    # Create the target directory if it does not exist
    target_dir = os.path.dirname(target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Create a temporary folder to hold the source files
    temp_folder = os.path.join(target_dir, '__temp__')
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