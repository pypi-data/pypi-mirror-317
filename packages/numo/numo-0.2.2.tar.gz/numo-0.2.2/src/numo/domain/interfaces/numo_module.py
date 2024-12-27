from abc import ABC, abstractmethod
from typing import Optional, Any


class NumoModule(ABC):
    """
    Abstract base class for all modules in the Numo system.

    Modules are responsible for executing specific types of operations such as:
    - Mathematical calculations
    - Unit conversions
    - Currency conversions
    - Language translations
    - Variable operations

    Each module specializes in a specific domain and implements the run method
    to handle operations within that domain.

    Important: Modules should never raise exceptions. They should return:
    - str: For successful operations
    - None: For any error or invalid input
    """

    @abstractmethod
    async def run(self, source: str) -> Optional[str]:
        """
        Execute the module's specific operation on the input string.

        Args:
            source: Preprocessed input string ready for execution

        Returns:
            str: Result as string if successful
            None: For any error or invalid input

        Example:
            >>> module = MathModule()
            >>> await module.run("1 + 2")  # Returns "3"
            >>> await module.run("invalid")  # Returns None
        """
        pass

    def _format_result(self, value: Any) -> Optional[str]:
        """
        Safely format any value to string or None.

        Args:
            value: Value to convert to string

        Returns:
            str: If value can be safely converted to string
            None: If value cannot be converted or is invalid
        """
        if value is None:
            return None

        try:
            return str(value)
        except (ValueError, TypeError):  # Catch only specific exceptions
            return None
