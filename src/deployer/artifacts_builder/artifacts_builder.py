import json
import os
from .zipper import create_zip_from_folder

def zip_archive_runner(zip_archive_definition):
    zip_artifacts = zip_archive_definition
    for i, zip_artifact in enumerate(zip_artifacts):
        if 'source' in zip_artifact and 'target' in zip_artifact:
            source = zip_artifact['source']
            target = zip_artifact['target']
            include_root = zip_artifact.get('include_root', False)
            create_zip_from_folder(source, target, include_root=include_root)
        else:
            raise ValueError(f"Error while parsing ZIP_ARTIFACTS, no source or target found at index {i}")

class ArtifactsBuilder:
    def __init__(self, file_path='.artifacts.json'):
        self.file_path = file_path

    def run(self):
        print(f"Artifact builder is running...")
        
        if not os.path.exists(self.file_path):
            print(f"No artifacts to build")
            return

        with open(self.file_path) as file:
            artifacts = json.load(file)

        if 'ZIP_ARTIFACTS' in artifacts:
            zip_archive_runner(artifacts['ZIP_ARTIFACTS'])
