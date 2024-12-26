import argparse
import json
import sys
from pathlib import Path
from typing import Union, Any

class JsonFormatError(Exception):
    """Base exception class for JSON formatting errors."""
    pass

class FileAccessError(JsonFormatError):
    """Exception raised for file access related errors."""
    pass

class JsonParseError(JsonFormatError):
    """Exception raised for JSON parsing related errors."""
    pass

def read_file(file_path: Union[str, Path]) -> str:
    """
    Read content from a file with error handling.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        str: Content of the file
        
    Raises:
        FileAccessError: If there are any issues accessing or reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileAccessError(f"File not found: {file_path}")
    except PermissionError:
        raise FileAccessError(f"Permission denied when accessing file: {file_path}")
    except IOError as e:
        raise FileAccessError(f"Error reading file {file_path}: {str(e)}")

def format_json(content: str, sort_keys: bool) -> str:
    """
    Format JSON content with specified sorting.
    
    Args:
        content: JSON string to format
        sort_keys: Whether to sort dictionary keys
        
    Returns:
        str: Formatted JSON string
        
    Raises:
        JsonParseError: If the content is not valid JSON
    """
    try:
        loaded_json = json.loads(content)
        return json.dumps(loaded_json, sort_keys=sort_keys, indent=4)
    except json.JSONDecodeError as e:
        raise JsonParseError(f"Invalid JSON format: {str(e)}")

def validate_file_path(file_path: str) -> Path:
    """
    Validate the input file path.
    
    Args:
        file_path: Path to validate
        
    Returns:
        Path: Validated Path object
        
    Raises:
        FileAccessError: If the path is invalid or points to a directory
    """
    path = Path(file_path)
    if path.is_dir():
        raise FileAccessError(f"Path points to a directory, not a file: {file_path}")
    return path

def process_json_file(file_path: str, sort_keys: bool) -> str:
    """
    Process a JSON file with all error handling.
    
    Args:
        file_path: Path to the JSON file
        sort_keys: Whether to sort dictionary keys
        
    Returns:
        str: Formatted JSON string
        
    Raises:
        JsonFormatError: If any error occurs during processing
    """
    path = validate_file_path(file_path)
    content = read_file(path)
    return format_json(content, sort_keys)

def main() -> int:
    """
    Main function with command line interface.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="JSON formatting tool that reads a file and outputs formatted JSON.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "file_path",
        type=str,
        help="Path to the JSON file to format"
    )
    parser.add_argument(
        "--sort",
        dest="sort",
        action="store_true",
        default=True,
        help="Enable sorting of JSON keys"
    )
    parser.add_argument(
        "--no-sort",
        dest="sort",
        action="store_false",
        help="Disable sorting of JSON keys"
    )

    args = parser.parse_args()

    try:
        formatted_json = process_json_file(args.file_path, args.sort)
        print(formatted_json)
        return 0
    except JsonFormatError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())