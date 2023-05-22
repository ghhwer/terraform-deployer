from abc import ABC, abstractmethod

class ProviderChecker(ABC):
    @abstractmethod
    def apply_provider(self, options):
        pass
