from typing import List, Optional, Callable, Any, Type
from numo.domain.interfaces.numo_manager import NumoManager
from numo.domain.interfaces.numo_module import NumoModule
from numo.infrastructure.managers import VariableManager, FunctionManager
from numo.infrastructure.modules import (
    TranslateModule,
    UnitModule,
    CurrencyModule,
    MathModule,
    VariableModule,
)


class Numo:
    """
    Numo: A comprehensive mathematical and conversion engine.

    Features:
    - Mathematical operations and functions
    - Unit conversions (length, weight, time, etc.)
    - Currency conversions with real-time rates
    - Language translations
    - Variable management
    - Custom module support

    Example:
        >>> numo = Numo()
        >>> await numo.calculate("2 + 2")  # Basic math
        >>> await numo.calculate("5 km to miles")  # Unit conversion
        >>> await numo.calculate("100 USD to EUR")  # Currency conversion
        >>> await numo.calculate("hello in spanish")  # Translation
    """

    def __init__(self):
        """Initialize Numo with default managers and modules."""
        self._managers: List[NumoManager] = [
            VariableManager(),
            FunctionManager(),
        ]

        self._modules: List[NumoModule] = [
            TranslateModule(),
            UnitModule(),
            CurrencyModule(),
            MathModule(),
            VariableModule(),
        ]

    async def calculate(self, lines: List[str]) -> List[Optional[str]]:
        """
        Process multiple lines of input through the Numo engine.

        Args:
            lines: List of input strings to process

        Returns:
            List of results, None if processing failed

        Example:
            >>> results = await numo.calculate([
            ...     "x = 5",
            ...     "y = x * 2",
            ...     "y km to miles"
            ... ])
        """
        processed_sources = self._preprocess_input_lines(lines)
        return await self._execute_modules(processed_sources)

    def get_available_functions(self) -> List[str]:
        """
        Get a list of all available mathematical functions.

        Returns:
            List of function names sorted alphabetically.

        Example:
            >>> numo = Numo()
            >>> numo.get_available_functions()
            ['abs', 'acos', 'asin', 'atan', 'ceil', 'cos', 'exp', 'fact', ...]
        """
        function_manager = next(
            m for m in self._managers if isinstance(m, FunctionManager)
        )
        return function_manager.get_available_functions()

    def get_available_variables(self) -> List[str]:
        """
        Get a list of all available variables and constants.

        Returns:
            List of variable names sorted alphabetically, including both
            user-defined variables and built-in constants.

        Example:
            >>> numo = Numo()
            >>> numo.get_available_variables()
            ['deg30', 'deg45', 'deg90', 'e', 'phi', 'pi', 'sqrt2', ...]
        """
        variable_manager = next(
            m for m in self._managers if isinstance(m, VariableManager)
        )
        return variable_manager.get_available_variables()

    def get_available_modules(self) -> List[str]:
        """
        Get a list of all active modules.

        Returns:
            List of module names sorted alphabetically.

        Example:
            >>> numo = Numo()
            >>> numo.get_available_modules()
            ['CurrencyModule', 'MathModule', 'TranslateModule', 'UnitModule', 'VariableModule']
        """
        return sorted([type(module).__name__ for module in self._modules])

    def add_module(self, module: NumoModule) -> None:
        """
        Add a custom module to the Numo engine.

        Args:
            module: Instance of a NumoModule implementation

        Example:
            >>> class CustomModule(NumoModule):
            ...     async def run(self, source: str) -> Optional[str]:
            ...         return source.upper()
            >>> numo.add_module(CustomModule())
        """
        if isinstance(module, NumoModule):
            self._modules.append(module)

    async def _execute_modules(self, sources: List[str]) -> List[Optional[str]]:
        """Execute each source through available modules until a result is found."""
        results = []

        for source in sources:
            if not source:
                results.append(None)
                continue

            result = None
            for module in self._modules:
                module_result = await module.run(source)
                if module_result:
                    result = module_result
                    break
            if isinstance(result, float):
                result = float(f"{result:.2f}")
            results.append(result)

        return results

    def _preprocess_input_lines(self, sources: List[str]) -> List[str]:
        """
        Preprocess input lines through all managers.

        Args:
            sources: List of raw input strings

        Returns:
            List of preprocessed strings
        """
        result = []

        for source in sources:
            processed_line = source.strip()
            for manager in self._managers:
                processed_line = manager.build(processed_line)
            result.append(processed_line)

        return result

    def add_function(self, name: str, func: Callable[[List[str]], Any]) -> None:
        """
        Add a new custom function to the Numo engine.

        Args:
            name: Function name to register
            func: Function implementation that takes a list of string parameters and returns any value

        Example:
            >>> numo = Numo()
            >>> numo.add_function("sum", lambda params: sum(float(p) for p in params))
            >>> await numo.calculate(["sum(1, 2, 3)"])  # ["6.0"]
        """
        function_manager = next(
            m for m in self._managers if isinstance(m, FunctionManager)
        )
        function_manager.add_function(name, func)

    def add_variable(self, name: str, value: Any) -> None:
        """
        Add a new variable to the Numo engine.

        Args:
            name: Variable name to register
            value: Value to associate with the variable

        Example:
            >>> numo = Numo()
            >>> numo.add_variable("pi", 3.14159)
            >>> await numo.calculate(["2 * pi"])  # ["6.28318"]
        """
        variable_manager = next(
            m for m in self._managers if isinstance(m, VariableManager)
        )
        variable_manager.add_variable(name, value)
