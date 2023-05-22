from .aws_provider import ProviderAWS

class Credentials():
    def __init__(self, options):
        expect_credentials = options.get('EXPECT_SECRETS_FOR')
        self.providers = {}
        for expect in expect_credentials:
            if expect  == 'AWS':
                self.providers[expect] = ProviderAWS(options)
            else:
                raise ValueError(f'Error while parsing "EXPECT_SECRETS_FOR": {expect} is not supported!')
