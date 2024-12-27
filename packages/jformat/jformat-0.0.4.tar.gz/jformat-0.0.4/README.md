# JFormat

A command-line tool for formatting and prettifying JSON files with customizable sorting options.

## Quick Start

```bash
# Install the package
pip install jformat

# Format a JSON file
echo '{"b":1,"a":2}' > input.json
jformat input.json
```

## Features

- Pretty print JSON with proper indentation
- Optional sorting of JSON keys
- Simple command-line interface
- Support for large JSON files
- Preserves JSON data types

## Installation

You can install JFormat using pip:

```bash
pip install jformat
```

For development installation:

```bash
git clone https://github.com/hwang2006/jformat.git
cd jformat
pip install -e .
```

## Usage

Basic usage:

```bash
# Format with default settings (sorted keys)
jformat input.json

# Format without sorting keys
jformat --no-sort input.json
```

### Options

- `--sort` / `--no-sort`: Enable or disable sorting of JSON keys (default: --sort)
- `FILE_PATH`: Path to the JSON file to format

### Examples

1. Format a JSON file with sorted keys:
```bash
jformat examples/input.json
```

Input:
```json
{"b": 1,"a": 2,"c": {"z": 3,"y": 4}}
```

Output:
```json
{
    "a": 2,
    "b": 1,
    "c": {
        "y": 4,
        "z": 3
    }
}
```

2. Format without sorting keys (preserves original order):
```bash
jformat --no-sort examples/input.json
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/hwang2006/jformat.git
cd jformat

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install only the core/basic requirements, when you just want to work with the package functionality
pip install -e .

# Install development dependencies, when you plan to develop, test, or contribute to the package
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Project Structure

```
jformat/
├── setup.py           # Package configuration and metadata
├── README.md         # Project documentation
├── LICENSE           # MIT License details
├── MANIFEST.in       # Package inclusion rules
├── CHANGELOG.md      # Version history and changes
├── requirements.txt  # Core package dependencies
├── requirements-dev.txt  # Development dependencies
├── examples/         # Example JSON files for testing
│   ├── input.json    # Basic JSON example
│   └── example.json  # Complex JSON example
├── tests/            # Test suite directory
│   ├── __init__.py   # Makes tests a package
│   └── test_formatter.py  # Unit tests for formatter
└── jformat/          # Main package source
    ├── __init__.py   # Package initialization
    └── cli.py        # Command line interface implementation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Soonwook Hwang - [hwang@kisti.re.kr](mailto:hwang@kisti.re.kr)

## Acknowledgments

- Inspired by Python's built-in `json.tool`
- Built with [Click](https://click.palletsprojects.com/)
