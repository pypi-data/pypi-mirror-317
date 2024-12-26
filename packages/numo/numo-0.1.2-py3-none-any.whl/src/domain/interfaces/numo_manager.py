from abc import ABC, abstractmethod

class NumoManager(ABC):
    @abstractmethod
    def build(self, source: str) -> str:
        """Process and transform the input string."""
        pass 