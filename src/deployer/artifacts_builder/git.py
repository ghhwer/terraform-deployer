import os
import shutil

from .zipper import create_zip_from_folder

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
        command = build_git_command(source, branch, tgt_folder)
        exit_code = os.system(command)
        if exit_code != 0:
            raise RuntimeError('Git clone failed.')
        create_zip_from_folder(tgt_folder, target, include_root=include_root)
        shutil.rmtree(tgt_folder)
    else:
        command = build_git_command(source, branch, target)
        # Initialize Terraform
        exit_code = os.system(command)
        if exit_code != 0:
            raise RuntimeError('Git clone failed.')
