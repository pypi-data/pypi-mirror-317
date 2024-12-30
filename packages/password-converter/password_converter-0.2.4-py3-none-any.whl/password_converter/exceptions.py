class ConverterError(Exception):
    """Base exception for password converter errors."""
    pass

class ValidationError(ConverterError):
    """Raised when input data validation fails."""
    pass