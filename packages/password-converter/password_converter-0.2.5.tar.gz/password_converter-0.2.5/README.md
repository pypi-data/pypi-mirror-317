# Password Converter

**Password Converter** is a Python tool designed to convert exported password files from Kaspersky Password Manager into a format compatible with Apple Passwords. This utility simplifies the migration process for users switching between password management systems.

---

## Features

- Converts Kaspersky Password Manager exports into Apple Password format.
- Validates password entries to ensure data integrity.
- Logs invalid entries with helpful error messages for troubleshooting.
- Outputs the converted data as a CSV file for easy import into Apple Passwords.
- Command-line interface (CLI) for simple usage.

---

## Installation

### Requirements
- Python 3.10 or higher.

### Install via pip
```bash
pip install password-converter
```

## Usage

### Command Line

The input.txt file is the file that is generated automatically with the Kaspersky password manager, and the output.csv is the file that is going to be generated with your passwords. You can import this .csv file directly into the Passwords app.

```bash
password-converter input.txt output.csv
password-converter input.txt output.csv --log-level DEBUG --log-file convert.log
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
Website name: Example Website
Website URL: https://example.com
Login: user@example.com
Password: secretpassword123
Comment: My favorite website
```

For applications:
```
Application: Example App
Login: user@example.com
Password: anotherpassword456
Comment:
```

## Output Format

Title,URL,Username,Password,Notes,OTPAuth
Example Website (user@example.com),https://example.com,user@example.com,secretpassword123,My favorite website,
Example App (user@example.com),,user@example.com,anotherpassword456,,

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
