# Password Converter

A Python tool for converting Kaspersky password manager exports to Apple Password format.

## Features

- Convert password exports to Apple Password CSV format
- Support for both website and application passwords
- Robust error handling and validation
- Detailed logging
- Command-line interface
- Python API for programmatic usage

## Installation

```bash
pip install password-converter
```

## Usage

### Command Line

```bash
python -m password-converter input.txt output.csv
python -m password-converter input.txt output.csv --log-level DEBUG --log-file convert.log
```

### Python API

```python
from password_converter import convert_file, convert_text

# Convert a file
convert_file("input.txt", "output.csv")

# Convert text directly
text = """
Website name: example.com
Website URL: https://example.com
Login: user@example.com
Password: secretpass
Comment: My account
---
"""
entries = convert_text(text)
```

## Input Format

The input file should contain password entries separated by "---". Each entry should have the following format:

For websites:
```
Website name: example.com
Website URL: https://example.com
Login: username
Password: password123
Comment: Optional comment
```

For applications:
```
Application: AppName
Login: username
Password: password123
Comment: Optional comment
```

## Development

1. Clone the repository
2. Install development dependencies:
```bash
pip install -e ".[dev]"
```
3. Run tests:
```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.