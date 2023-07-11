import json
import os
from .zipper import create_zip_from_folder
from .git import fetch_from_git_repo

def zip_archive_runner(zip_archive_definition):
    for i, zip_artifact in enumerate(zip_archive_definition):
        if 'source' in zip_artifact and 'target' in zip_artifact:
            source = zip_artifact['source']
            target = zip_artifact['target']
            include_root = zip_artifact.get('include_root', False)
            create_zip_from_folder(source, target, include_root=include_root)
        else:
            raise ValueError(f"Error while parsing ZIP_ARTIFACTS: no source or target found at index {i}")

def git_fetch_runner(git_fetch_definition):
    for i, git_artifact in enumerate(git_fetch_definition):
        if 'source' in git_artifact and 'target' in git_artifact and 'branch' in git_artifact:
            source = git_artifact['source']
            branch = git_artifact['branch']
            target = git_artifact['target']
            include_root = git_artifact.get('include_root', False)
            fetch_from_git_repo(source, branch, target, include_root)
        else:
            raise ValueError(f"Error while parsing GIT_ARTIFACTS: either source, target or branch is missing at index {i}")

class ArtifactsBuilder:
    def __init__(self, file_path='.artifacts.json'):
        self.file_path = file_path

    def run(self):       
        if not os.path.exists(self.file_path):
            print(f"No artifacts to build")
            return

        with open(self.file_path) as file:
            artifacts = json.load(file)

        if 'ZIP_ARTIFACTS' in artifacts:
            zip_archive_runner(artifacts['ZIP_ARTIFACTS'])
        if 'GIT_ARTIFACTS' in artifacts:
            git_fetch_runner(artifacts['GIT_ARTIFACTS'])