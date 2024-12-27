"""Language data and utilities for the Numo engine."""

import os
from numo.services.file_service import FileService

# Get current module path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load language data
languages = FileService.load_json_file(current_dir, "language.json")

__all__ = ["languages"]
