"""Unit conversion data and utilities for the Numo engine."""
from pathlib import Path
import json
from typing import Dict, Any

def load_unit_data(unit_type: str) -> Dict[str, Any]:
    """
    Load unit conversion data from JSON configuration files.
    
    Args:
        unit_type: Type of units to load (e.g., 'length', 'weight')
        
    Returns:
        Dictionary containing unit conversion data
        
    Raises:
        FileNotFoundError: If unit data file doesn't exist
        JSONDecodeError: If unit data file is invalid JSON
    """
    current_dir = Path(__file__).parent
    data_dir = current_dir / 'data'
    file_path = data_dir / f'{unit_type}.json'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load all unit conversion data
angular_units = load_unit_data('angular')
area_units = load_unit_data('area')
length_units = load_unit_data('length')
speed_units = load_unit_data('speed')
storage_units = load_unit_data('storage')
time_units = load_unit_data('time')
volume_units = load_unit_data('volume')
weight_units = load_unit_data('weight')
languages = load_unit_data('language')

__all__ = [
    'angular_units',
    'area_units',
    'length_units',
    'speed_units',
    'storage_units',
    'time_units',
    'volume_units',
    'weight_units',
    'languages'
] 