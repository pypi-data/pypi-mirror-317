from typing import List, Optional, Callable, Any
from numo.domain.interfaces.numo_manager import NumoManager
from numo.domain.interfaces.numo_runner import NumoRunner
from numo.infrastructure.managers import VariableManager, FunctionManager
from numo.infrastructure.runners import (
    TranslateRunner,
    UnitRunner,
    CurrencyRunner,
    MathRunner,
    VariableRunner
)

class Numo:
    def __init__(self):
        self._managers: List[NumoManager] = [
            VariableManager(),
            FunctionManager()
        ]
        
        self._runners: List[NumoRunner] = [
            TranslateRunner(),
            UnitRunner(),
            CurrencyRunner(),
            MathRunner(),
            VariableRunner()
        ]
    
    async def calculate(self, lines: List[str]) -> List[Optional[str]]:
        """
        Process multiple lines of input through the Numo engine.
        
        Args:
            lines: List of input strings to process
            
        Returns:
            List of results, None if processing failed
        """
        processed_sources = self._preprocess_input_lines(lines)
        return await self._execute_runners(processed_sources)
        
    async def _execute_runners(self, sources: List[str]) -> List[Optional[str]]:
        results = []
        
        for source in sources:
            if not source:
                results.append(None)
                continue
            
            result = None
            for runner in self._runners:
                runner_result = await runner.run(source)
                if runner_result:
                    result = runner_result
                    break
                    
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
        function_manager = next(m for m in self._managers if isinstance(m, FunctionManager))
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
        variable_manager = next(m for m in self._managers if isinstance(m, VariableManager))
        variable_manager.add_variable(name, value) 