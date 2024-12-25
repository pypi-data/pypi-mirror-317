import re
from typing import Dict, Any
from src.domain.interfaces.numo_manager import NumoManager

class VariableManager(NumoManager):
    def __init__(self):
        self._pattern = r"(\w+)\s*[:=]\s*([^\s]+)"
        self._variables: Dict[str, str] = {}
        self._initialize_operator_aliases()
        
    def _initialize_operator_aliases(self) -> None:
        """Initialize standard operator aliases for better readability."""
        operator_mappings = {
            # Mathematical operators and their aliases
            "+": ["+", "plus", "add"],
            "-": ["-", "minus", "subtract"],
            "*": ["*", "multiply", "times"],
            "/": ["/", "division", "divide"],
            "%": ["%", "mod", "modulus"],
            "^": ["^", "power", "exponent"]
        }
        
        for operator, aliases in operator_mappings.items():
            for alias in aliases:
                self._variables[alias.lower()] = operator

    def build(self, source: str) -> str:
        """
        Process source string for variable definitions and replacements.
        
        Args:
            source: Input string to process
            
        Returns:
            Processed string with variables replaced
        """
        if not self._process_variable_definition(source):
            return self._replace_variable_references(source)
        return source

    def _replace_variable_references(self, source: str) -> str:
        """
        Replace variable references with their corresponding values.
        
        Args:
            source: Input string containing variable references
            
        Returns:
            String with variables replaced by their values
        """
        tokens = source.split()
        for i, token in enumerate(tokens):
            value = self._variables.get(token.lower())
            if value is not None:
                tokens[i] = value
        return " ".join(tokens)

    def _process_variable_definition(self, source: str) -> bool:
        """
        Process and store variable definitions.
        
        Args:
            source: Input string potentially containing variable definition
            
        Returns:
            True if string contains variable definition, False otherwise
        """
        match = re.match(self._pattern, source)
        if match:
            variable_name = match.group(1)
            variable_value = match.group(2)
            self._variables[variable_name.lower()] = variable_value
            return True
        return False 

    def add_variable(self, name: str, value: Any) -> None:
        """
        Add a new variable to the manager.
        
        Args:
            name: Variable name to register
            value: Value to associate with the variable
        """
        self._variables[name.lower()] = str(value) 