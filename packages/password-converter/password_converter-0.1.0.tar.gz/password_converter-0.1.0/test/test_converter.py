import pytest
from pathlib import Path
from typing import Dict
from password_converter.converter import PasswordConverter, convert_file, convert_text

def test_read_file(temp_input_file: Path):
    converter = PasswordConverter(temp_input_file)
    sections = converter.read_file()
    assert len(sections) == 2
    assert "Website name: example.com" in sections[0]
    assert "Application: TestApp" in sections[1]

def test_parse_blocks(sample_text: str):
    converter = PasswordConverter()
    sections = [section.strip() for section in sample_text.split("---")]
    blocks = converter.parse_blocks(sections)
    
    assert len(blocks) == 2
    assert blocks[0]["Website name"] == "example.com"
    assert blocks[1]["Application"] == "TestApp"

def test_convert_to_apple_format(sample_website_entry: Dict[str, str], 
                               sample_app_entry: Dict[str, str]):
    converter = PasswordConverter()
    data = [sample_website_entry, sample_app_entry]
    apple_format = converter.convert_to_apple_format(data)
    
    assert len(apple_format) == 2
    
    # Check website entry
    website_entry = apple_format[0]
    assert website_entry["Title"] == "example.com (user@example.com)"
    assert website_entry["URL"] == "https://example.com"
    assert website_entry["Username"] == "user@example.com"
    assert website_entry["Password"] == "secretpass"
    assert website_entry["Notes"] == "Test account"
    assert website_entry["OTPAuth"] == ""
    
    # Check app entry
    app_entry = apple_format[1]
    assert app_entry["Title"] == "TestApp (testuser)"
    assert app_entry["URL"] == ""
    assert app_entry["Username"] == "testuser"
    assert app_entry["Password"] == "apppass123"
    assert app_entry["Notes"] == "App account"
    assert app_entry["OTPAuth"] == ""

def test_save_csv(tmp_path: Path, sample_website_entry: Dict[str, str]):
    converter = PasswordConverter()
    output_path = tmp_path / "test_output.csv"
    
    apple_format = converter.convert_to_apple_format([sample_website_entry])
    converter.save_csv(apple_format, output_path)
    
    assert output_path.exists()
    content = output_path.read_text()
    assert "Title,URL,Username,Password,Notes,OTPAuth" in content
    assert "example.com (user@example.com)" in content

def test_convert_file_integration(temp_input_file: Path, tmp_path: Path):
    output_path = tmp_path / "output.csv"
    convert_file(temp_input_file, output_path)
    
    assert output_path.exists()
    content = output_path.read_text()
    assert "example.com (user@example.com)" in content
    assert "TestApp (testuser)" in content

def test_convert_text_integration(sample_text: str):
    result = convert_text(sample_text)
    
    assert len(result) == 2
    assert result[0]["Title"] == "example.com (user@example.com)"
    assert result[1]["Title"] == "TestApp (testuser)"