from abc import ABC, abstractmethod

class StateFileLoader(ABC):
    @abstractmethod
    def get_file(self, options):
        pass
    @abstractmethod
    def put_file(self, options, new_state_file_path):
        pass
