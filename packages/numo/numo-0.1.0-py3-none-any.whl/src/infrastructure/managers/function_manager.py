import re
from typing import Dict, Callable, List, Any
from src.domain.interfaces.numo_manager import NumoManager

class FunctionManager(NumoManager):
    def __init__(self):
        self._pattern = r"(\w+)\((.*?)\)"
        self._functions: Dict[str, Callable[[List[str]], Any]] = {}
        self._initialize_functions()

    def _initialize_functions(self) -> None:
        """Initialize standard mathematical functions."""
        self._functions.update({
            "nsum": lambda params: sum(float(p) for p in params),
            "navg": lambda params: sum(float(p) for p in params) / len(params),
            "nmax": lambda params: max(float(p) for p in params),
            "nmin": lambda params: min(float(p) for p in params)
        })

    def add_function(self, name: str, func: Callable[[List[str]], Any]) -> None:
        """
        Add a new function to the manager.
        
        Args:
            name: Function name
            func: Function implementation that takes list of string parameters
        """
        self._functions[name.lower()] = func

    def build(self, source: str) -> str:
        """
        Process source string for function calls.
        
        Args:
            source: Input string to process
            
        Returns:
            String with function calls evaluated
        """
        match = re.search(self._pattern, source)
        if not match:
            return source

        try:
            func_name = match.group(1).lower()
            params = [p.strip() for p in match.group(2).split(",")]
            
            func = self._functions.get(func_name)
            if func:
                result = func(params)
                return source.replace(match.group(0), str(result))
                
        except Exception:
            pass

        return source 