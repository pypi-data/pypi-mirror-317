import pytest
import json
from pathlib import Path
from json_converter.csv_to_json import CSVToJSONConverter, convert_csv_file, convert_csv_string

# Sample data for testing
CSV_DATA = "Name,Age,City\nAlice,30,New York\nBob,25,London"
CSV_DATA_WITH_TYPES = "Name,Age,IsActive\nAlice,30,true\nBob,25,false"
CSV_DATA_WITH_NUMBERS = "Item,Price,Quantity\nItem1,10.5,5\nItem2,20,10"
EMPTY_CSV_DATA = "Name,Age,City\n"

@pytest.fixture
def converter():
    return CSVToJSONConverter()

def test_convert_string(converter):
    expected_json = json.dumps([{"Name": "Alice", "Age": 30, "City": "New York"}, {"Name": "Bob", "Age": 25, "City": "London"}], indent=2)
    assert json.loads(converter.convert_string(CSV_DATA)) == json.loads(expected_json)

def test_convert_string_with_types(converter):
    expected_json = json.dumps([{"Name": "Alice", "Age": 30, "IsActive": True}, {"Name": "Bob", "Age": 25, "IsActive": False}], indent=2)
    assert json.loads(converter.convert_string(CSV_DATA_WITH_TYPES)) == json.loads(expected_json)

def test_convert_string_with_numbers(converter):
    expected_json = json.dumps([{"Item": "Item1", "Price": 10.5, "Quantity": 5}, {"Item": "Item2", "Price": 20.0, "Quantity": 10}], indent=2)
    assert json.loads(converter.convert_string(CSV_DATA_WITH_NUMBERS)) == json.loads(expected_json)

def test_convert_string_empty():
    expected_json = '[]'
    assert convert_csv_string("Name,Age,City\n") == expected_json

def test_convert_file(converter, tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.json"
    input_file.write_text(CSV_DATA)
    assert converter.convert_file(input_file, output_file)
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert data == [{"Name": "Alice", "Age": 30, "City": "New York"}, {"Name": "Bob", "Age": 25, "City": "London"}]

def test_convert_file_with_types(converter, tmp_path):
    input_file = tmp_path / "input_types.csv"
    output_file = tmp_path / "output_types.json"
    input_file.write_text(CSV_DATA_WITH_TYPES)
    assert converter.convert_file(input_file, output_file)
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert data == [{"Name": "Alice", "Age": 30, "IsActive": True}, {"Name": "Bob", "Age": 25, "IsActive": False}]

def test_convert_file_with_numbers(converter, tmp_path):
    input_file = tmp_path / "input_numbers.csv"
    output_file = tmp_path / "output_numbers.json"
    input_file.write_text(CSV_DATA_WITH_NUMBERS)
    assert converter.convert_file(input_file, output_file)
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert data == [{"Item": "Item1", "Price": 10.5, "Quantity": 5}, {"Item": "Item2", "Price": 20.0, "Quantity": 10}]

def test_convert_file_empty(tmp_path):
    input_file = tmp_path / "empty.csv"
    output_file = tmp_path / "empty.json"
    input_file.write_text("Name,Age,City\n")
    assert convert_csv_file(input_file, output_file)
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert data == []

def test_convert_file_not_found(converter, tmp_path):
    input_file = tmp_path / "nonexistent.csv"
    output_file = tmp_path / "output.json"
    assert not converter.convert_file(input_file, output_file)

def test_convert_file_invalid(converter, tmp_path):
    input_file = tmp_path / "invalid.csv"
    output_file = tmp_path / "output.json"
    input_file.write_text("Name,Age,City\nAlice,30\nBob,25,London,Extra")
    assert not converter.convert_file(input_file, output_file)

def test_convert_string_invalid(converter):
    invalid_csv_data = "Name,Age,City\nAlice,30\nBob,25,London,Extra"
    assert not converter.convert_string(invalid_csv_data)
