"""
Password Converter
----------------
A tool for converting Kaspersky manager exports to Apple Password format.
"""

__version__ = "0.1.0"
from .converter import convert_file, convert_text
from .exceptions import ConverterError, ValidationError