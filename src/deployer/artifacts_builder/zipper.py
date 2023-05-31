import os
import shutil
import zipfile

def create_zip_from_folder(source, target):
    # Create the target directory if it does not exist
    target_dir = os.path.dirname(target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Create a temporary folder to hold the source files
    temp_folder = os.path.join(target_dir, '__temp__')
    os.makedirs(temp_folder)

    try:
        # Copy the source folder to the temporary folder
        shutil.copytree(source, os.path.join(temp_folder, os.path.basename(source)))

        # Create the zip file
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, temp_folder))

    finally:
        # Clean up the temporary folder
        shutil.rmtree(temp_folder)

