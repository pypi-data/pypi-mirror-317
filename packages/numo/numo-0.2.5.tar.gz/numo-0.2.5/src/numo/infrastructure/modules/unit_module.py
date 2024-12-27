import re
from typing import Dict, Optional, Any
from numo.domain.interfaces.numo_module import NumoModule
from numo.infrastructure.modules.units import (
    angular_units,
    area_units,
    length_units,
    speed_units,
    storage_units,
    time_units,
    volume_units,
    weight_units,
)


class UnitModule(NumoModule):
    """
    Unit conversion module.
    Handles conversions between different units of measurement.
    Supports length, weight, area, volume, speed, time, and digital storage units.
    """

    def __init__(self):
        """Initialize with conversion factors."""
        self._pattern = r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)\s*to\s*([a-zA-Z]+)"
        self._conversion_factors: Dict[str, float] = {}
        self._initialize_conversion_factors()

    def _initialize_conversion_factors(self) -> None:
        """Initialize conversion factors from all unit types."""
        unit_collections = [
            angular_units,
            area_units,
            length_units,
            speed_units,
            storage_units,
            time_units,
            volume_units,
            weight_units,
        ]

        for collection in unit_collections:
            for unit_data in collection.values():
                for phrase in unit_data["phrases"]:
                    try:
                        factor = float(unit_data["unit"])
                        self._conversion_factors[phrase.lower()] = factor
                    except:
                        continue

    async def run(self, source: str) -> Optional[str]:
        """
        Convert between different units of measurement.

        Args:
            source: Input string in format "value unit_from to unit_to"

        Returns:
            str: Converted value as string if successful
            None: For any error or invalid input

        Example:
            >>> module = UnitModule()
            >>> await module.run("5 km to miles")  # Returns "3.10686"
            >>> await module.run("1 kg to pounds")  # Returns "2.20462"
        """
        if not source or not isinstance(source, str):
            return None

        match = re.match(self._pattern, source)
        if not match:
            return None

        try:
            amount = float(match.group(1))
            from_unit = match.group(2).lower()
            to_unit = match.group(3).lower()
        except (ValueError, TypeError):
            return None

        result = self._convert_units(amount, from_unit, to_unit)
        if result is None:
            return None

        return self._format_result(result)

    def _convert_units(
        self, value: float, from_unit: str, to_unit: str
    ) -> Optional[float]:
        """
        Convert value between units using conversion factors.

        Args:
            value: Numeric value to convert
            from_unit: Source unit
            to_unit: Target unit

        Returns:
            float: Converted value if possible
            None: For any error or invalid input
        """
        from_factor = self._get_conversion_factor(from_unit)
        if from_factor is None:
            return None

        to_factor = self._get_conversion_factor(to_unit)
        if to_factor is None or to_factor == 0:
            return None

        try:
            return value * (from_factor / to_factor)
        except (ValueError, ZeroDivisionError):
            return None

    def _get_conversion_factor(self, unit: str) -> Optional[float]:
        """
        Get conversion factor for a unit.

        Args:
            unit: Unit name to look up

        Returns:
            float: Conversion factor if unit exists
            None: For any error or invalid unit
        """
        return self._conversion_factors.get(unit.lower())

    def _format_result(self, value: float) -> str:
        """Format the result as a string with two decimal places."""
        try:
            return f"{float(value):.2f}"
        except (ValueError, TypeError):
            return str(value)
