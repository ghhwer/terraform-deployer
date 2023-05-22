from commons.checker import options_present
from .base_providers import ProviderChecker
import os
import boto3

class ProviderAWS(ProviderChecker):
    def __init__(self, options):
        options_present(
            ["ACCESS_KEY", "SECRET_ACCESS_KEY", "AWS_REGION"], options
        )
        self.apply_provider(options)
        print('AWS credentials loaded')

    def apply_provider(self, options):
        os.environ["AWS_ACCESS_KEY_ID"] = options['ACCESS_KEY']
        os.environ["AWS_SECRET_ACCESS_KEY"] = options['SECRET_ACCESS_KEY']
        self.session = boto3.Session(
            aws_access_key_id = options['ACCESS_KEY'],
            aws_secret_access_key = options['SECRET_ACCESS_KEY'],
            region_name = options['AWS_REGION']
        )