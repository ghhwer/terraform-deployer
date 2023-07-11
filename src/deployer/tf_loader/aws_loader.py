from .loader_base import StateFileLoader
import boto3
import os

def separate_s3_uri(s3_uri):
    s3_uri = s3_uri.strip()
    if s3_uri.startswith('s3://'):
        s3_uri = s3_uri[5:]  # Remove the 's3://' prefix

    bucket_name, _, prefix = s3_uri.partition('/')
    return bucket_name, prefix

def download_s3_file(session, s3_uri, destination_path):
    try:
        bucket_name, prefix = separate_s3_uri(s3_uri)
        s3 = session.client('s3')
        s3.download_file(bucket_name, prefix, destination_path)
    except Exception as e:
        print(f"Error downloading S3 file: {str(e)}")
        raise e

def upload_file_to_s3(session, source_path, s3_uri):
    try:
        s3 = session.client('s3')
        bucket_name, prefix = separate_s3_uri(s3_uri)
        s3.upload_file(source_path, bucket_name, prefix)
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
        raise e

def check_s3_file_exists(session, s3_uri):
    s3 = session.client('s3')
    bucket_name, prefix = separate_s3_uri(s3_uri)
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    for obj in response.get('Contents', []):
        if obj['Key'] == prefix:
            return True
    return False

class StateFileLoaderS3(StateFileLoader):
    def __init__(self, options, credentials):
        pipeline_name = options.get('PIPELINE_NAME')
        state_location = options.get('TF_STATE_LOCATION')
        # Self Stuff
        self.chdir = options.get('TERRAFORM_CHDIR')
        self.remote_path = f'{state_location}/{pipeline_name}/terraform.tfstate'
        self.local_path = f'{self.chdir}/terraform.tfstate'
        self.session = credentials.providers['AWS'].session

    def get_file(self,):
        # Delete Local file if it exists
        if os.path.exists(self.local_path):
            os.remove(self.local_path)
            print("Local state file has been removed")
        else:
            print("State file does not exist locally yet")
        if(check_s3_file_exists(self.session, self.remote_path)):
            download_s3_file(self.session, self.remote_path, self.local_path)
            print(f'Remote file: {self.remote_path} has been downloaded')
        else:
            print(f'Remote file: {self.remote_path} does not exist, not syncing')

    def put_file(self,):
        if(os.path.isfile(self.local_path)):
            upload_file_to_s3(self.session, self.local_path, self.remote_path)
        else:
            print(f'Local file: {self.local_path} does not exist, not syncing')