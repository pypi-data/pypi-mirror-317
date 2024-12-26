import pytest
import json
from pathlib import Path
import tempfile
import os
from jformat.cli import (
    format_json,
    read_file,
    validate_file_path,
    process_json_file,
    JsonFormatError,
    FileAccessError,
    JsonParseError
)

@pytest.fixture
def temp_json_file():
    """Fixture to create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json_content = {
            "b": 2,
            "a": 1,
            "c": {"y": 2, "x": 1}
        }
        json.dump(json_content, f)
        path = f.name
    
    yield path
    
    # Cleanup after test
    os.unlink(path)

@pytest.fixture
def invalid_json_file():
    """Fixture to create a temporary file with invalid JSON content."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write('{"invalid": "json"')  # Missing closing brace
        path = f.name
    
    yield path
    
    # Cleanup after test
    os.unlink(path)

def test_format_json_with_sorting():
    """Test JSON formatting with key sorting enabled."""
    input_json = '{"b": 2, "a": 1}'
    expected = json.dumps({"a": 1, "b": 2}, indent=4)
    assert format_json(input_json, sort_keys=True) == expected

def test_format_json_without_sorting():
    """Test JSON formatting with key sorting disabled."""
    input_json = '{"b": 2, "a": 1}'
    expected = json.dumps(json.loads(input_json), indent=4)
    assert format_json(input_json, sort_keys=False) == expected

def test_format_json_nested_structure():
    """Test JSON formatting with nested structures."""
    input_json = '{"b": {"y": 2, "x": 1}, "a": 1}'
    formatted = format_json(input_json, sort_keys=True)
    assert json.loads(formatted) == {"a": 1, "b": {"x": 1, "y": 2}}

def test_format_json_invalid_json():
    """Test handling of invalid JSON input."""
    with pytest.raises(JsonParseError):
        format_json('{"invalid": json}', sort_keys=True)

def test_read_file_success(temp_json_file):
    """Test successful file reading."""
    content = read_file(temp_json_file)
    assert content
    assert json.loads(content) is not None

def test_read_file_not_found():
    """Test handling of non-existent file."""
    with pytest.raises(FileAccessError):
        read_file("nonexistent_file.json")

def test_validate_file_path_success(temp_json_file):
    """Test successful file path validation."""
    path = validate_file_path(temp_json_file)
    assert isinstance(path, Path)
    assert path.exists()

def test_validate_file_path_directory():
    """Test handling when path points to a directory."""
    with pytest.raises(FileAccessError):
        validate_file_path(os.path.dirname(os.path.abspath(__file__)))

def test_process_json_file_success(temp_json_file):
    """Test successful JSON file processing."""
    formatted = process_json_file(temp_json_file, sort_keys=True)
    parsed = json.loads(formatted)
    assert isinstance(parsed, dict)
    assert list(parsed.keys()) == sorted(list(parsed.keys()))

def test_process_json_file_invalid_json(invalid_json_file):
    """Test handling of file with invalid JSON content."""
    with pytest.raises(JsonParseError):
        process_json_file(invalid_json_file, sort_keys=True)

def test_process_json_file_not_found():
    """Test handling of non-existent file during processing."""
    with pytest.raises(FileAccessError):
        process_json_file("nonexistent_file.json", sort_keys=True)

def test_format_json_empty_object():
    """Test formatting of empty JSON object."""
    input_json = '{}'
    expected = json.dumps({}, indent=4)
    assert format_json(input_json, sort_keys=True) == expected

def test_format_json_array():
    """Test formatting of JSON array."""
    input_json = '[1, 2, 3]'
    expected = json.dumps([1, 2, 3], indent=4)
    assert format_json(input_json, sort_keys=True) == expected

def test_format_json_complex_nested():
    """Test formatting of complex nested structures."""
    input_json = '''
    {
        "b": {
            "nested": {
                "y": 2,
                "x": 1
            }
        },
        "a": [1, 2, 3]
    }
    '''
    formatted = format_json(input_json, sort_keys=True)
    parsed = json.loads(formatted)
    assert parsed["a"] == [1, 2, 3]
    assert parsed["b"]["nested"]["x"] == 1
    assert parsed["b"]["nested"]["y"] == 2