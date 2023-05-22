from .loader_base import StateFileLoader

class StateFileLoaderS3(StateFileLoader):
    def __init__(self, options, credentials):
        pipeline_name = options.get('PIPELINE_NAME')
        state_location = options.get('TF_STATE_LOCATION')
        self.full_path = f'{state_location}/{pipeline_name}.json'
    def get_file(self,):
        raise NotImplementedError('get_file not implemented yet')
    def put_file(self,):
        raise NotImplementedError('put_file not implemented yet')