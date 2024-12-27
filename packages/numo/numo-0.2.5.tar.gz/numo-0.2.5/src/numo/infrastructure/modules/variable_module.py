import re
from typing import Optional
from numo.services.math_service import MathService
from numo.domain.interfaces.numo_module import NumoModule


class VariableModule(NumoModule):
    """
    Variable management module.
    Handles variable definition, assignment, and evaluation operations.
    Supports various assignment formats and value processing.
    """

    def __init__(self):
        """Initialize with variable pattern."""
        self._pattern = r"(\w+)\s*[:=]\s*(.+)"

    async def run(self, source: str) -> Optional[str]:
        """
        Performs variable definition and assignment operation.

        Args:
            source (str): Source code line to process (e.g., "x = 5")

        Returns:
            Optional[str]: Variable value if successful, None if failed
        """
        match = re.match(self._pattern, source)
        if not match:
            return None

        variable_name = match.group(1)
        variable_value = match.group(2)
        processed_value = MathService.safe_eval(variable_value)
        if processed_value is not None:
            return str(processed_value)
        return variable_value
