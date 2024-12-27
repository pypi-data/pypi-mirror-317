import re


class MathService:
    """
    Service class for handling mathematical operations.
    """

    pattern = r"^[\d\s\+\-\*\/\(\)\^\%\.\,]+$"

    @staticmethod
    def safe_eval(expression: str) -> float:
        """
        Safely evaluate a mathematical expression.
        """
        try:
            if not re.match(MathService.pattern, expression):
                return None
            expression = expression.replace("^", "**")
            return float(eval(expression, {"__builtins__": {}}, {}))
        except:
            return None
