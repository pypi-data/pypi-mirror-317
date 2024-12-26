import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Union, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CSVToJSONConverter:
    def __init__(self):
        """Initialize the converter"""
        pass

    def convert_file(self, input_file: Union[str, Path], output_file: Union[str, Path]) -> bool:
        """
        Convert CSV file to JSON file.
        
        Args:
            input_file: Path to the input CSV file
            output_file: Path to the output JSON file
            
        Returns:
            bool: True if conversion was successful, False otherwise
        """
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        return self._convert_to_file()

    def convert_string(self, csv_string: str) -> Optional[str]:
        """
        Convert CSV string to JSON string.
        
        Args:
            csv_string: Input CSV string
            
        Returns:
            str: JSON string if successful, None otherwise
        """
        try:
            # Convert CSV string to list of dictionaries
            data = []
            for row in csv.DictReader(csv_string.splitlines()):
                data.append(self._clean_row(row))
            
            # Convert to JSON string
            return json.dumps(data, indent=2, ensure_ascii=False)
        
        except Exception as e:
            logger.error(f"Error converting CSV string to JSON: {str(e)}")
            return None

    def _convert_to_file(self) -> bool:
        """Internal method to handle file-based conversion"""
        try:
            if not self.input_file.exists():
                raise FileNotFoundError(f"Input file {self.input_file} does not exist")

            logger.info(f"Starting conversion of {self.input_file} to JSON")
            
            # Read CSV and convert to list of dictionaries
            data: List[Dict[str, Any]] = []
            with open(self.input_file, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                data = [self._clean_row(row) for row in csv_reader]

            # Write to JSON file
            with open(self.output_file, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=2, ensure_ascii=False)

            logger.info(f"Successfully converted CSV to JSON: {self.output_file}")
            return True

        except Exception as e:
            logger.error(f"Error converting CSV to JSON: {str(e)}")
            return False

    def _clean_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Clean and type-convert row data"""
        cleaned_row: Dict[str, Any] = {}
        for key, value in row.items():
            cleaned_key = key.strip()
            cleaned_value = value.strip()
            # Attempt type conversion
            if cleaned_value.isdigit():
                cleaned_row[cleaned_key] = int(cleaned_value)
            elif cleaned_value.lower() == 'true':
                cleaned_row[cleaned_key] = True
            elif cleaned_value.lower() == 'false':
                cleaned_row[cleaned_key] = False
            else:
                try:
                    cleaned_row[cleaned_key] = float(cleaned_value)
                except ValueError:
                    cleaned_row[cleaned_key] = cleaned_value
        return cleaned_row

def convert_csv_file(input_file: Union[str, Path], output_file: Union[str, Path]) -> bool:
    """
    Convenience function to convert CSV file to JSON file.
    
    Args:
        input_file: Path to the input CSV file
        output_file: Path to the output JSON file
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    converter = CSVToJSONConverter()
    return converter.convert_file(input_file, output_file)

def convert_csv_string(csv_string: str) -> Optional[str]:
    """
    Convenience function to convert CSV string to JSON string.
    
    Args:
        csv_string: Input CSV string
        
    Returns:
        str: JSON string if successful, None otherwise
    """
    converter = CSVToJSONConverter()
    return converter.convert_string(csv_string)
