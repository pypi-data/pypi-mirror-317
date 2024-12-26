from abc import ABC, abstractmethod


class NumoManager(ABC):
    """
    Abstract base class for all managers in the Numo system.

    Managers are responsible for preprocessing and transforming input strings
    before they are passed to runners for execution. They handle tasks such as:
    - Variable substitution
    - Function resolution
    - Syntax transformation
    - Input validation
    """

    @abstractmethod
    def build(self, source: str) -> str:
        """
        Process and transform the input string according to manager's responsibility.

        Args:
            source: Raw input string to be processed

        Returns:
            Processed string ready for execution

        Example:
            >>> manager = ConcreteManager()
            >>> manager.build("x = 5")  # Might transform to "5" if x was previously defined
        """
        pass
