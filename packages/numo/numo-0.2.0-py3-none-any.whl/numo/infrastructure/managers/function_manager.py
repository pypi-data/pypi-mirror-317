from typing import Dict, Callable, Any, List, Optional
import re
import math
from numo.domain.interfaces.numo_manager import NumoManager


class FunctionManager(NumoManager):
    """
    Manager for handling function calls in expressions.
    Manages function registration and execution.
    Never raises exceptions - returns original input for any error condition.
    """

    def __init__(self):
        """Initialize with function registry and pattern."""
        self._pattern = r"(\w+)\((.*?)\)"
        self._functions: Dict[str, Callable[[List[str]], Any]] = {}
        self._initialize_functions()

    def build(self, source: str) -> str:
        """
        Process input string and execute any function calls.

        Args:
            source: Input string that may contain function calls

        Returns:
            Processed string with function calls replaced by their results.
            Returns original string if any error occurs.

        Example:
            >>> manager = FunctionManager()
            >>> manager.build("nsum(1, 2, 3)")  # Returns "6"
            >>> manager.build("invalid()")     # Returns "invalid()"
        """
        if not source or not isinstance(source, str):
            return source

        try:
            # Find all function calls
            matches = list(re.finditer(self._pattern, source))
            if not matches:
                return source

            # Process each function call from right to left
            result = source
            for match in reversed(matches):
                func_name = match.group(1).lower()
                args_str = match.group(2)

                # Get function and process arguments
                func = self._functions.get(func_name)
                if not func:
                    continue

                # Parse arguments
                args = [arg.strip() for arg in args_str.split(",") if arg.strip()]
                if not args:
                    continue

                try:
                    # Execute function and format result
                    func_result = func(args)
                    if func_result is not None:
                        # Format result as float with two decimal places
                        if isinstance(func_result, (int, float)):
                            func_result = f"{float(func_result):.2f}"
                        # Replace function call with result
                        result = (
                            result[: match.start()]
                            + str(func_result)
                            + result[match.end() :]
                        )
                except:
                    continue

            return result

        except:  # Catch absolutely everything
            return source

    def add_function(self, name: str, func: Callable[[List[str]], Any]) -> None:
        """
        Add a new function to the registry.

        Args:
            name: Function name
            func: Function implementation that takes string arguments
        """
        try:
            if name and isinstance(name, str) and callable(func):
                self._functions[name.lower()] = func
        except:  # Catch absolutely everything
            pass

    def _initialize_functions(self) -> None:
        """Initialize built-in mathematical functions."""
        try:
            self._functions.update(
                {
                    # Basic Math Functions
                    "abs": lambda params: abs(float(params[0])),
                    "round": lambda params: round(float(params[0])),
                    "floor": lambda params: math.floor(float(params[0])),
                    "ceil": lambda params: math.ceil(float(params[0])),
                    # Statistical Functions
                    "sum": lambda params: sum(float(p) for p in params),
                    "avg": lambda params: sum(float(p) for p in params) / len(params),
                    "min": lambda params: min(float(p) for p in params),
                    "max": lambda params: max(float(p) for p in params),
                    # Trigonometric Functions
                    "sin": lambda params: math.sin(float(params[0])),
                    "cos": lambda params: math.cos(float(params[0])),
                    "tan": lambda params: math.tan(float(params[0])),
                    "asin": lambda params: math.asin(float(params[0])),
                    "acos": lambda params: math.acos(float(params[0])),
                    "atan": lambda params: math.atan(float(params[0])),
                    # Power and Logarithmic Functions
                    "pow": lambda params: math.pow(float(params[0]), float(params[1])),
                    "sqrt": lambda params: math.sqrt(float(params[0])),
                    "log": lambda params: math.log(float(params[0])),
                    "log10": lambda params: math.log10(float(params[0])),
                    "exp": lambda params: math.exp(float(params[0])),
                    # Additional Statistical Functions
                    "median": lambda params: sorted([float(p) for p in params])[
                        len(params) // 2
                    ],
                    "var": lambda params: sum(
                        (float(x) - sum(float(p) for p in params) / len(params)) ** 2
                        for x in params
                    )
                    / len(params),
                    "std": lambda params: math.sqrt(
                        sum(
                            (float(x) - sum(float(p) for p in params) / len(params))
                            ** 2
                            for x in params
                        )
                        / len(params)
                    ),
                    # Additional Math Functions
                    "fact": lambda params: math.factorial(int(float(params[0]))),
                    "gcd": lambda params: math.gcd(
                        int(float(params[0])), int(float(params[1]))
                    ),
                    "mod": lambda params: float(params[0]) % float(params[1]),
                }
            )
        except:  # Catch absolutely everything
            pass

    def get_available_functions(self) -> list[str]:
        """
        Get a list of all available function names.

        Returns:
            List of function names sorted alphabetically.
        """
        try:
            return sorted(list(self._functions.keys()))
        except:  # Catch absolutely everything
            return []
