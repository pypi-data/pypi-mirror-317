from typing import Dict, Optional, Tuple
from numo.domain.interfaces.numo_manager import NumoManager


class VariableManager(NumoManager):
    """
    Manager for handling variable operations and source code manipulation.
    Responsible for:
    1. Variable definitions (x = 5, y := 10)
    2. Variable substitutions in expressions
    3. Mathematical operator aliases
    """

    def __init__(self):
        """Initialize variable storage and operator aliases."""
        # Variable storage
        self._variables: Dict[str, str] = {}

        # Mathematical operator aliases
        self._operators = {
            "+": ["plus", "add"],
            "-": ["minus", "subtract"],
            "*": ["multiply", "times"],
            "/": ["divide", "division"],
            "%": ["mod", "modulus"],
            "^": ["power", "exponent"],
        }

        # Initialize operator aliases
        self._initialize_operators()

    def build(self, source: str) -> str:
        """
        Process source code for variable operations.

        Args:
            source: Source code that might contain:
                   - Variable definition (x = 5)
                   - Variable reference (x + 10)
                   - Operator aliases (plus, times)

        Returns:
            Processed source code with:
            - Variable references replaced with their values
            - Operator aliases replaced with actual operators
            - Variable definitions processed and stored

        Example:
            >>> manager = VariableManager()
            >>> manager.build("x = 5")        # Stores x=5, returns "x = 5"
            >>> manager.build("x plus 3")      # Returns "5 + 3"
            >>> manager.build("y times 2")     # Returns "y * 2" (y not defined)
        """
        if not source or not isinstance(source, str):
            return source

        try:
            # First check if it's a variable definition
            source = source.strip()
            is_definition, processed = self._process_definition(source)
            if is_definition:
                return processed

            # If not a definition, process variable references and operators
            return self._process_references(source)

        except:  # Catch absolutely everything
            return source

    def _process_definition(self, source: str) -> Tuple[bool, str]:
        """
        Process potential variable definition.

        Args:
            source: Source code to check for variable definition

        Returns:
            Tuple of (is_definition, processed_source)
        """
        try:
            # Check for assignment operators
            for op in ["=", ":="]:
                if op in source:
                    parts = source.split(op, 1)
                    if len(parts) == 2:
                        name = parts[0].strip()
                        value = parts[1].strip()

                        # Validate variable name
                        if not self._is_valid_name(name):
                            return False, source

                        # Process value for any existing variable references
                        processed_value = self._process_references(value)

                        # Store the variable
                        self._variables[name.lower()] = processed_value

                        return True, f"{name} {op} {processed_value}"

            return False, source

        except:  # Catch absolutely everything
            return False, source

    def _process_references(self, source: str) -> str:
        """
        Process variable references and operator aliases in source.

        Args:
            source: Source code containing references/aliases

        Returns:
            Processed source with references/aliases replaced
        """
        try:
            tokens = source.split()
            processed = []

            for token in tokens:
                # Try to replace variable or operator
                lower_token = token.lower()
                if lower_token in self._variables:
                    processed.append(self._variables[lower_token])
                else:
                    processed.append(token)

            return " ".join(processed)

        except:  # Catch absolutely everything
            return source

    def _is_valid_name(self, name: str) -> bool:
        """
        Validate variable name.

        Args:
            name: Variable name to validate

        Returns:
            True if name is valid, False otherwise
        """
        try:
            # Must be a string and not empty
            if not name or not isinstance(name, str):
                return False

            # Must start with letter or underscore
            if not name[0].isalpha() and name[0] != "_":
                return False

            # Rest must be alphanumeric or underscore
            return all(c.isalnum() or c == "_" for c in name[1:])

        except:  # Catch absolutely everything
            return False

    def _initialize_operators(self) -> None:
        """Initialize mathematical operator aliases."""
        try:
            for operator, aliases in self._operators.items():
                # Store operator itself
                self._variables[operator] = operator
                # Store all aliases
                for alias in aliases:
                    self._variables[alias.lower()] = operator
        except:  # Catch absolutely everything
            pass

    def get_variable(self, name: str) -> Optional[str]:
        """
        Get value of a variable.

        Args:
            name: Variable name to look up

        Returns:
            Variable value if exists, None otherwise
        """
        try:
            return self._variables.get(name.lower())
        except:  # Catch absolutely everything
            return None

    def clear_variables(self) -> None:
        """Clear all user variables but keep operator aliases."""
        try:
            # Keep only operator aliases
            operators = {
                name: value
                for name, value in self._variables.items()
                if any(value == op for op in self._operators.keys())
            }
            self._variables = operators
        except:  # Catch absolutely everything
            pass
