import argparse
import json

def format_json(content, sort_keys):
    """Format JSON content with specified sorting."""
    loaded_json = json.loads(content)
    return json.dumps(loaded_json, sort_keys=sort_keys, indent=4)

def main():
    parser = argparse.ArgumentParser(
        description="JSON formatting tool that reads a file and outputs formatted JSON."
    )
    parser.add_argument(
        "file_path", type=str, help="Path to the JSON file to format"
    )
    parser.add_argument(
        "--sort", dest="sort", action="store_true", default=True, 
        help="Enable sorting of JSON keys (default: enabled)"
    )
    parser.add_argument(
        "--no-sort", dest="sort", action="store_false", 
        help="Disable sorting of JSON keys"
    )

    args = parser.parse_args()

    with open(args.file_path, 'r') as file:
        formatted_json = format_json(file.read(), args.sort)
        print(formatted_json)

if __name__ == "__main__":
    main()