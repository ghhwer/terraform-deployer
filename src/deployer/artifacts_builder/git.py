import os
import shutil
import hashlib

from .zipper import create_zip_from_folder, calculate_zip_checksum

build_git_command = lambda source, branch, dest: f'git clone {source} -b {branch} {dest}'

def fetch_from_git_repo(source, branch, target, include_root=False):
    print(f'Fetching remote repo from from {source} and materializing it at: {target}')
    # Create the target directory if it does not exist
    is_zip_target = '.zip' in target

    target_dir = os.path.dirname(target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # if it is a zip target, clone then zip
    if is_zip_target:

        # Create a temporary folder to hold the source files
        tgt_folder = '/tmp/git-clone'
        tgt_zip = '/tmp/git-clone.zip'
        # Prior failed runs leave these behind and block the next clone.
        for path in (tgt_folder, tgt_zip):
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.exists(path):
                os.remove(path)

        try:
            command = build_git_command(source, branch, tgt_folder)
            exit_code = os.system(command)
            if exit_code != 0:
                raise RuntimeError('Git clone failed.')
            # Remove the .git folder
            shutil.rmtree(os.path.join(tgt_folder, '.git'))
            create_zip_from_folder(tgt_folder, tgt_zip, include_root=include_root)

            # Check if the checksum of the new source is different from the old one
            # 1. Check if the target exists
            if os.path.exists(target):
                print(f'Target {target} exists.')
                # 2. If it exists, check if the source has changed
                old_checksum = calculate_zip_checksum(target)
                new_checksum = calculate_zip_checksum(tgt_zip)
                print(f'Old checksum: {old_checksum}')
                print(f'New checksum: {new_checksum}')
                if old_checksum == new_checksum:
                    print(f'No changes in the source. Keeping the old target.')
                    if os.path.exists(tgt_zip):
                        os.remove(tgt_zip)
                else:
                    # 3. If the source has changed, replace the target
                    print(f'Source has changed. Replacing the target.')
                    shutil.move(tgt_zip, target)
            else:
                shutil.move(tgt_zip, target)
        finally:
            if os.path.isdir(tgt_folder):
                shutil.rmtree(tgt_folder)
            if os.path.exists(tgt_zip):
                os.remove(tgt_zip)
    else:
        if os.path.isdir(target):
            shutil.rmtree(target)
        elif os.path.exists(target):
            os.remove(target)
        command = build_git_command(source, branch, target)
        # Initialize Terraform
        exit_code = os.system(command)
        if exit_code != 0:
            raise RuntimeError('Git clone failed.')
