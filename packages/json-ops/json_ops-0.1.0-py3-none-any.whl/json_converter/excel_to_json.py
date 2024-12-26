import io
import pandas as pd
import json
from pathlib import Path
from typing import Union, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExcelToJSONConverter:
    def _add_to_nested_dict(self, keys, value, target):
        """Adds a value to a nested dictionary using a list of keys."""
        for key in keys[:-1]:
            target = target.setdefault(key, {})
        target[keys[-1]] = value

    def convert_file(self, input_file: Union[str, Path], output_file: Union[str, Path]) -> bool:
        """Convert an Excel file to a nested JSON file based on column names."""
        try:
            df = pd.read_excel(input_file)
            nested_data = []
            for _, row in df.iterrows():
                item = {}
                for col, value in row.items():
                    if pd.notna(value):
                        keys = col.split('.')
                        self._add_to_nested_dict(keys, value, item)
                if item:
                    nested_data.append(item)
            with open(output_file, 'w') as f:
                json.dump(nested_data, f, indent=2)
            logger.info(f"Successfully converted '{input_file}' to '{output_file}'")
            return True
        except FileNotFoundError:
            logger.error(f"Error: Input file '{input_file}' not found.")
            return False
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return False

    def convert_string(self, excel_content: bytes) -> Optional[str]:
        """Convert Excel file content (bytes) to a nested JSON string based on column names."""
        try:
            df = pd.read_excel(io.BytesIO(excel_content))
            nested_data = []
            for _, row in df.iterrows():
                item = {}
                for col, value in row.items():
                    if pd.notna(value):
                        keys = col.split('.')
                        self._add_to_nested_dict(keys, value, item)
                if item:
                    nested_data.append(item)
            return json.dumps(nested_data, indent=2)
        except Exception as e:
            logger.error(f"Error converting Excel content to JSON: {e}")
            return None

def convert_excel_file(input_file: Union[str, Path], output_file: Union[str, Path]) -> bool:
    """Convenience function to convert an Excel file to nested JSON based on column names."""
    converter = ExcelToJSONConverter()
    return converter.convert_file(input_file, output_file)

def convert_excel_string(excel_content: bytes) -> Optional[str]:
    """Convenience function to convert Excel file content (bytes) to nested JSON based on column names."""
    converter = ExcelToJSONConverter()
    return converter.convert_string(excel_content)
