import pytest
from json_converter.excel_to_json import convert_excel_file, convert_excel_string
import json
from pathlib import Path
import pandas as pd

def test_convert_excel_file_basic(tmp_path):
    # Create a sample Excel file
    data = {'name': ['John', 'Jane'], 'age': [30, 25]}
    df = pd.DataFrame(data)
    input_file = tmp_path / "input.xlsx"
    df.to_excel(input_file, index=False)

    # Define the output file path
    output_file = tmp_path / "output.json"

    # Call the convert_excel_file function
    result = convert_excel_file(input_file, output_file)
    assert result is True
    assert output_file.exists()

    # Check the content of the output JSON file
    with open(output_file, 'r') as f:
        json_data = json.load(f)
    assert json_data == [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]

def test_convert_excel_file_empty(tmp_path):
    # Create an empty Excel file
    input_file = tmp_path / "empty.xlsx"
    df = pd.DataFrame()
    df.to_excel(input_file, index=False)

    # Define the output file path
    output_file = tmp_path / "output.json"

    # Call the convert_excel_file function
    result = convert_excel_file(input_file, output_file)
    assert result is True
    assert output_file.exists()

    # Check the content of the output JSON file
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert data == []

import io

def test_convert_excel_string_basic():
    # Create a sample Excel content
    data = {'name': ['John', 'Jane'], 'age': [30, 25]}
    df = pd.DataFrame(data)
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    excel_content_bytes = buffer.getvalue()

    # Call the convert_excel_string function
    result = convert_excel_string(excel_content_bytes)
    assert result is not None
    json_data = json.loads(result)
    assert json_data == [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]

import io

def test_convert_excel_string_empty():
    # Create an empty Excel content
    df = pd.DataFrame()
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    excel_content_bytes = buffer.getvalue()

    # Call the convert_excel_string function
    result = convert_excel_string(excel_content_bytes)
    assert result is not None
    json_data = json.loads(result)
    assert json_data == []
