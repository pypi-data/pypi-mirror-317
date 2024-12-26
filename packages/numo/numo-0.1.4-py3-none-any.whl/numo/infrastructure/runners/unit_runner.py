import re
from typing import Dict, Optional
from numo.domain.interfaces.numo_runner import NumoRunner
from numo.infrastructure.runners.units import (
    angular_units,
    area_units,
    length_units,
    speed_units,
    storage_units,
    time_units,
    volume_units,
    weight_units
)

class UnitRunner(NumoRunner):
    def __init__(self):
        self._pattern = r"(\d+)\s*([a-zA-Z]+)\s*to\s*([a-zA-Z]+)"
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
            weight_units
        ]
        
        for collection in unit_collections:
            for unit_data in collection.values():
                for phrase in unit_data['phrases']:
                    self._conversion_factors[phrase.lower()] = float(unit_data['unit'])
    
    async def run(self, source: str) -> Optional[str]:
        """
        Convert between different units of measurement.
        
        Args:
            source: Input string in format "value unit_from to unit_to"
            
        Returns:
            Converted value string if successful, None if failed
        """
        match = re.match(self._pattern, source)
        if not match:
            return None

        try:
            amount = float(match.group(1))
            from_unit = match.group(2)
            to_unit = match.group(3)
            
            converted = self._convert_units(amount, from_unit, to_unit)
            if converted is not None:
                return str(converted)
        except Exception:
            pass
        
        return None
    
    def _convert_units(self, value: float, from_unit: str, to_unit: str) -> Optional[float]:
        """
        Convert value between units using conversion factors.
        
        Args:
            value: Numeric value to convert
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            Converted value if conversion is possible, None otherwise
        """
        from_factor = self._get_conversion_factor(from_unit)
        to_factor = self._get_conversion_factor(to_unit)
        
        if from_factor is not None and to_factor is not None:
            return value * from_factor / to_factor
        return None
    
    def _get_conversion_factor(self, unit: str) -> Optional[float]:
        """
        Get conversion factor for a unit.
        
        Args:
            unit: Unit name to look up
            
        Returns:
            Conversion factor if unit exists, None otherwise
        """
        return self._conversion_factors.get(unit.lower()) 