import logging
from typing import Dict, Optional
from pathlib import Path
from .exceptions import ValidationError
# from exceptions import ValidationError

def setup_logging(log_level: str = "INFO", log_file: Optional[Path] = None) -> None:
    """Configure logging with both console and file handlers."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers = []

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    handlers.append(console_handler)

    # File handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)

    # Set up basic configuration with appropriate logging level
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),  # Default to INFO if invalid level is provided
        handlers=handlers
    )

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))  # Explicitly set the level

def validate_entry(entry: Dict[str, str]) -> None:
    """Validate a single entry dictionary."""
    required_fields = {
        "Website": ["Website name", "Website URL", "Login", "Password"],
        "Application": ["Application", "Login", "Password"]
    }

    # Determine the entry type based on the fields present
    if "Website name" in entry:
        entry_type = "Website"
    elif "Application" in entry:
        entry_type = "Application"
    else:
        # If neither, raise an Unknown entry type error
        raise ValidationError(f"Unknown entry type: {entry}")

    # Check if required fields are present for the entry type
    missing_fields = [field for field in required_fields[entry_type]
                     if field not in entry or not entry[field]]
    
    if missing_fields:
        raise ValidationError(f"Missing required fields: {missing_fields}")
