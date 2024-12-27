from typing import Optional
from numo.services.math_service import MathService
from numo.domain.interfaces.numo_module import NumoModule


class MathModule(NumoModule):
    """
    Mathematical operations module.
    Provides safe evaluation of mathematical expressions using MathService.

    Features:
    - Basic arithmetic operations (+, -, *, /, %, ^)
    - Mathematical functions (abs, sqrt, pow, etc.)
    - Safe evaluation with input validation
    - Protection against dangerous operations
    """

    async def run(self, source: str) -> Optional[str]:
        """
        Safely evaluate a mathematical expression.

        Args:
            source: Mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)")

        Returns:
            str: Result as string if successful
            None: For any error or invalid input

        Example:
            >>> module = MathModule()
            >>> await module.run("2 + 2")  # Returns "4.00"
            >>> await module.run("1 / 0")  # Returns None
        """
        return MathService.safe_eval(source)
