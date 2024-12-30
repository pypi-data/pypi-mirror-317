import pytest
import logging
from pathlib import Path
from password_converter.utils import setup_logging, validate_entry
from password_converter.exceptions import ValidationError

def test_setup_logging(tmp_path: Path):
    log_file = tmp_path / "test.log"
    setup_logging(log_level="DEBUG", log_file=log_file)

    logger = logging.getLogger()
    assert logger.level == logging.DEBUG

def test_validate_entry_website_valid(sample_website_entry):
    # Should not raise an exception
    validate_entry(sample_website_entry)

def test_validate_entry_app_valid(sample_app_entry):
    # Should not raise an exception
    validate_entry(sample_app_entry)

def test_validate_entry_website_missing_field():
    invalid_entry = {
        "Website name": "example.com",
        "Website URL": "https://example.com",
        # Missing Login
        "Password": "secretpass"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        validate_entry(invalid_entry)
    assert "Missing required fields" in str(exc_info.value)

def test_validate_entry_app_missing_field():
    invalid_entry = {
        "Application": "TestApp",
        # Missing Login
        "Password": "apppass123"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        validate_entry(invalid_entry)
    assert "Missing required fields" in str(exc_info.value)

def test_validate_entry_unknown_type():
    invalid_entry = {
        "Unknown": "value",
        "Login": "user",
        "Password": "pass"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        validate_entry(invalid_entry)
    assert "Unknown entry type" in str(exc_info.value)