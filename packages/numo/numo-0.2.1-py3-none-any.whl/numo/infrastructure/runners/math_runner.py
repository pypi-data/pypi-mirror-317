from typing import Optional, Any
import ast
import operator
from numo.services.math_service import MathService
from numo.domain.interfaces.numo_runner import NumoRunner


class MathRunner(NumoRunner):
    """
    Runner for safely evaluating mathematical expressions.
    Uses AST-based evaluation instead of eval() for security.
    Never raises exceptions - returns None for any error condition.
    """

    # Supported operators and their implementations
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    def __init__(self):
        """Initialize with validation settings."""
        self._max_length = 1000  # Maximum expression length
        self._max_depth = 20  # Maximum AST depth

    async def run(self, source: str) -> Optional[str]:
        """
        Safely evaluate a mathematical expression.

        Args:
            source: Mathematical expression to evaluate

        Returns:
            str: Result as string if successful
            None: For any error or invalid input

        Example:
            >>> runner = MathRunner()
            >>> await runner.run("2 + 2")  # Returns "4"
            >>> await runner.run("1 / 0")  # Returns None
        """
        return MathService.safe_eval(source)

        # Basic validation
        if not source or not isinstance(source, str):
            return None

        if len(source) > self._max_length:
            return None

        try:
            # Parse and evaluate
            node = ast.parse(source, mode="eval")
            if not self._is_safe_ast(node):
                return None

            result = self._evaluate_node(node.body)
            if result is None:
                return None

            return self._format_result(result)

        except:  # Catch absolutely everything
            return None

    def _is_safe_ast(self, node: ast.AST, depth: int = 0) -> bool:
        """
        Recursively validate the AST to ensure it only contains safe operations.

        Args:
            node: AST node to validate
            depth: Current recursion depth

        Returns:
            True if AST is safe, False otherwise
        """
        try:
            if depth > self._max_depth:
                return False

            # Only allow specific node types
            allowed = (
                ast.Expression,
                ast.Num,
                ast.Constant,
                ast.BinOp,
                ast.UnaryOp,
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.Pow,
                ast.Mod,
                ast.USub,
            )

            if not isinstance(node, allowed):
                return False

            return all(
                self._is_safe_ast(child, depth + 1)
                for child in ast.iter_child_nodes(node)
            )

        except:  # Catch absolutely everything
            return False

    def _evaluate_node(self, node: Any) -> Optional[float]:
        """
        Recursively evaluate an AST node.

        Args:
            node: AST node to evaluate

        Returns:
            float: Calculated result if successful
            None: For any error or invalid input
        """
        try:
            if isinstance(node, (ast.Num, ast.Constant)):
                return float(node.n)

            elif isinstance(node, ast.BinOp):
                left = self._evaluate_node(node.left)
                if left is None:
                    return None

                right = self._evaluate_node(node.right)
                if right is None:
                    return None

                op = self.OPERATORS.get(type(node.op))
                if op is None:
                    return None

                try:
                    # Special handling for power operation
                    if isinstance(node.op, ast.Pow):
                        if abs(right) > 100:  # Limit for large exponents
                            return None
                        result = op(left, right)
                        if isinstance(result, complex):  # Prevent complex numbers
                            return None
                        return float(result)
                    return float(op(left, right))
                except:
                    return None

            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
                value = self._evaluate_node(node.operand)
                if value is None:
                    return None
                return -value

            return None

        except:  # Catch absolutely everything
            return None

    def _format_result(self, value: float) -> str:
        """Format the result as a string with one decimal place."""
        try:
            return f"{float(value):.2f}"
        except:
            return str(value)
