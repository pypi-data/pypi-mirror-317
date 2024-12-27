"""File operations service for the Numo engine."""

import json
import os


class FileService:
    """Service for handling file operations in the Numo engine."""

    @staticmethod
    def load_json_file(module_path: str, filename: str) -> dict:
        """
        Load and parse a JSON file from a specified module path.

        Args:
            module_path: The absolute path to the module directory
            filename: Name of the JSON file to load

        Returns:
            Dict containing the parsed JSON data

        Example:
            >>> current_dir = os.path.dirname(os.path.abspath(__file__))
            >>> data = FileService.load_json_file(current_dir, "config.json")
        """
        file_path = os.path.join(module_path, "data", filename)
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
