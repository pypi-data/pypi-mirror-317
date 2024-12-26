# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2024-12-26

### Added
- Comprehensive error handling system with custom exception classes:
  - `JsonFormatError` as base exception
  - `FileAccessError` for file-related issues
  - `JsonParseError` for JSON parsing problems
- Type hints for better code clarity and IDE support
- Detailed docstrings for all functions following standard Python format
- Path validation using `pathlib`
- UTF-8 encoding support for file operations
- Proper error messages directed to stderr
- System exit codes (0 for success, 1 for error)
- New utility functions for better code organization:
  - `read_file()` for safe file reading
  - `validate_file_path()` for path validation
  - `process_json_file()` for high-level processing
- Explicit `--no-sort` flag to disable JSON key sorting

### Changed
- Migrated from Click to argparse for command-line argument parsing
- Restructured command-line interface while maintaining the same functionality
- Updated help messages and argument descriptions for better clarity
- Improved error message formatting
- Enhanced file handling with better exception management
- Refactored code structure for better separation of concerns

### Technical Details
- Command-line arguments now use argparse's native boolean flag handling
- Maintained backward compatibility with existing JSON formatting functionality
- Default behavior of sorting remains enabled
- Added type annotations throughout the codebase
- Implemented proper resource handling for file operations

## [0.0.1] - Initial Release

### Added
- Initial release of JSON formatting tool
- Basic JSON formatting functionality with indentation
- Command-line interface using Click
- Support for enabling/disabling JSON key sorting
- File input handling with path validation
