import os
import json

def read_env_file(file_path):
    # Read files
    with open(file_path) as f:
        data = f.read()
    # Parse the file input
    data = json.loads(data)
    # convert all keys to upper-case
    return {key.upper(): value for key, value in data.items()}

def parse_env_file(path):
    # Read file
    if (os.path.isfile(path)):
        return read_env_file(path)
    else:
        raise FileExistsError(f'{path} file was not found')