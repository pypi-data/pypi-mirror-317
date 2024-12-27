"""Unit conversion data and utilities for the Numo engine."""

import os
from numo.services.file_service import FileService

# Get current module path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load all unit data
angular_units = FileService.load_json_file(current_dir, "angular.json")
area_units = FileService.load_json_file(current_dir, "area.json")
length_units = FileService.load_json_file(current_dir, "length.json")
speed_units = FileService.load_json_file(current_dir, "speed.json")
storage_units = FileService.load_json_file(current_dir, "storage.json")
time_units = FileService.load_json_file(current_dir, "time.json")
volume_units = FileService.load_json_file(current_dir, "volume.json")
weight_units = FileService.load_json_file(current_dir, "weight.json")
pressure_units = FileService.load_json_file(current_dir, "pressure.json")
datarate_units = FileService.load_json_file(current_dir, "datarate.json")
electrical_units = FileService.load_json_file(current_dir, "electrical.json")
power_units = FileService.load_json_file(current_dir, "power.json")
screen_units = FileService.load_json_file(current_dir, "screen.json")

__all__ = [
    "angular_units",
    "area_units",
    "length_units",
    "speed_units",
    "storage_units",
    "time_units",
    "volume_units",
    "weight_units",
    "pressure_units",
    "datarate_units",
    "electrical_units",
    "power_units",
    "screen_units",
]
