import pytest
from src.application.numo import Numo

@pytest.fixture
def numo():
    """Create a Numo instance for testing."""
    return Numo()

@pytest.mark.asyncio
class TestNumo:
    async def test_math_operations(self, numo):
        """Test basic mathematical operations."""
        results = await numo.calculate([
            "2 + 2",
            "3 * 4",
            "10 / 2",
            "2 ^ 3",
            "10 % 3"
        ])
        assert len(results) == 5
        assert results[0] == "4"
        assert results[1] == "12"
        assert results[2] == "5.0"
        assert results[3] == "8"
        assert results[4] == "1"

    async def test_unit_conversions(self, numo):
        """Test unit conversion functionality."""
        results = await numo.calculate([
            "1 km to m",
            "100 cm to m",
            "1 kg to g",
            "1 hour to minutes",
            "1 gb to mb",
            "100 mph to kmph"
        ])
        assert len(results) == 6
        assert results[0] == "1000 m"
        assert results[1] == "1 m"
        assert results[2] == "1000 g"
        assert results[3] == "60 minutes"
        assert results[4] == "1000 mb"
        assert "kmph" in results[5]

    async def test_currency_conversion(self, numo):
        """Test currency conversion functionality."""
        results = await numo.calculate([
            "100 USD to EUR",
            "50 EUR to JPY"
        ])
        assert len(results) == 2
        assert all(result is not None for result in results)
        assert "EUR" in results[0]
        assert "JPY" in results[1]

    async def test_translation(self, numo):
        """Test translation functionality."""
        results = await numo.calculate([
            "hello in spanish",
            "goodbye in french"
        ])
        assert len(results) == 2
        assert results[0] == "hola"
        assert results[1] == "au revoir"

    async def test_variable_management(self, numo):
        """Test variable management functionality."""
        results = await numo.calculate([
            "x = 5",
            "y = 3",
            "x + y",
            "z = x * y",
            "z / 2"
        ])
        assert len(results) == 5
        assert results[2] == "8"
        assert results[4] == "7.5"

    async def test_function_calls(self, numo):
        """Test built-in function calls."""
        results = await numo.calculate([
            "nsum(1,2,3,4)",
            "navg(2,4,6,8)",
            "nmax(1,5,3,7)",
            "nmin(4,2,6,1)"
        ])
        assert len(results) == 4
        assert results[0] == "10"
        assert results[1] == "5"
        assert results[2] == "7"
        assert results[3] == "1"

    async def test_operator_aliases(self, numo):
        """Test operator alias functionality."""
        results = await numo.calculate([
            "5 plus 3",
            "10 minus 4",
            "3 times 4",
            "15 divide 3",
            "7 mod 2"
        ])
        assert len(results) == 5
        assert results[0] == "8"
        assert results[1] == "6"
        assert results[2] == "12"
        assert results[3] == "5"
        assert results[4] == "1"

    async def test_empty_and_invalid_input(self, numo):
        """Test handling of empty and invalid input."""
        results = await numo.calculate([
            "",
            "invalid expression",
            "xyz + 123",
            "1 km to invalidunit"
        ])
        assert len(results) == 4
        assert all(result is None for result in results)

    async def test_error_handling(self, numo):
        """Test error handling in various scenarios."""
        results = await numo.calculate([
            "1 / 0",  # Division by zero
            "sqrt(-1)",  # Invalid math operation
            "invalid in spanish",  # Invalid translation
            "abc to xyz"  # Invalid unit conversion
        ])
        assert len(results) == 4
        assert all(result is None for result in results) 