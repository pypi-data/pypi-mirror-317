import re
import math
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
            # Basic Statistical Functions
            "nsum": lambda params: sum(float(p) for p in params),
            "navg": lambda params: sum(float(p) for p in params) / len(params),
            "nmax": lambda params: max(float(p) for p in params),
            "nmin": lambda params: min(float(p) for p in params),
            "nlen": lambda params: len(params),
            "nmedian": lambda params: sorted([float(p) for p in params])[len(params)//2],
            
            # Mathematical Functions
            "sqrt": lambda params: math.sqrt(float(params[0])),
            "abs": lambda params: abs(float(params[0])),
            "round": lambda params: round(float(params[0])),
            "floor": lambda params: math.floor(float(params[0])),
            "ceil": lambda params: math.ceil(float(params[0])),
            "pow": lambda params: math.pow(float(params[0]), float(params[1])),
            
            # Trigonometric Functions
            "sin": lambda params: math.sin(float(params[0])),
            "cos": lambda params: math.cos(float(params[0])),
            "tan": lambda params: math.tan(float(params[0])),
            "asin": lambda params: math.asin(float(params[0])),
            "acos": lambda params: math.acos(float(params[0])),
            "atan": lambda params: math.atan(float(params[0])),
            
            # Logarithmic Functions
            "log": lambda params: math.log(float(params[0])),
            "log10": lambda params: math.log10(float(params[0])),
            "log2": lambda params: math.log2(float(params[0])),
            
            # Additional Statistical Functions
            "nrange": lambda params: max(float(p) for p in params) - min(float(p) for p in params),
            "nproduct": lambda params: math.prod(float(p) for p in params),
            "nstd": lambda params: (
                sum((float(x) - (sum(float(p) for p in params) / len(params)))**2 
                for x in params) / len(params)
            )**0.5,
            
            # String Functions
            "concat": lambda params: "".join(params),
            "upper": lambda params: params[0].upper(),
            "lower": lambda params: params[0].lower(),
            "reverse": lambda params: params[0][::-1],
            "len": lambda params: len(params[0])
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