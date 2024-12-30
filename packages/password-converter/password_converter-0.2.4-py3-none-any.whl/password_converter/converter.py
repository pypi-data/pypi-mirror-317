import csv
from pathlib import Path
from typing import List, Dict, Union, Optional
import logging
from .exceptions import ConverterError, ValidationError
from .utils import validate_entry
# from exceptions import ConverterError, ValidationError
# from utils import validate_entry

logger = logging.getLogger(__name__)

class PasswordConverter:
    """Main class for handling password conversion operations."""
    
    def __init__(self, input_path: Optional[Path] = None, output_path: Optional[Path] = None):
        self.input_path = input_path
        self.output_path = output_path
        self.logger = logging.getLogger(__name__)

    def read_file(self) -> List[str]:
        """Read and split input file into sections."""
        try:
            with open(self.input_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            return [section.strip() for section in content.split("---") if section.strip()]
        except Exception as e:
            raise ConverterError(f"Error reading file: {e}")

    def parse_blocks(self, sections: List[str]) -> List[Dict[str, str]]:
        """Parse sections into structured blocks."""
        blocks = []
        
        for section in sections:
            current_block = {}
            lines = [line.strip() for line in section.split('\n') if line.strip()]
            
            # Skip headers
            if len(lines) == 1 and ':' not in lines[0]:
                continue
                
            for line in lines:
                if ':' in line:
                    key, value = map(str.strip, line.split(':', 1))
                    if key in ["Website name", "Website URL", "Application", 
                             "Login", "Password", "Comment"]:
                        current_block[key] = value
            
            if current_block:
                try:
                    validate_entry(current_block)
                    blocks.append(current_block)
                except ValidationError as e:
                    self.logger.warning(f"Skipping invalid entry: {e}")
                    
        return blocks

    def convert_to_apple_format(self, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Convert parsed data to Apple Password format."""
        apple_format = []
        
        for entry in data:
            try:
                if "Website name" in entry:
                    title = entry["Website name"]
                    url = entry["Website URL"]
                elif "Application" in entry:
                    title = entry["Application"]
                    url = ""
                else:
                    continue

                if entry.get("Login"):
                    title = f"{title} ({entry['Login']})"

                apple_format.append({
                    "Title": title,
                    "URL": url,
                    "Username": entry["Login"],
                    "Password": entry["Password"],
                    "Notes": entry.get("Comment", ""),
                    "OTPAuth": ""
                })
            except Exception as e:
                self.logger.error(f"Error converting entry {entry}: {e}")

        return apple_format

    def save_csv(self, data: List[Dict[str, str]], output_path: Path) -> None:
        """Save converted data to CSV file."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open('w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "Title", "URL", "Username", "Password", "Notes", "OTPAuth"
                ])
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            raise ConverterError(f"Error saving CSV: {e}")

def convert_file(input_path: Union[str, Path], 
                output_path: Union[str, Path], 
                log_level: str = "INFO",
                log_file: Optional[Union[str, Path]] = None) -> None:
    """
    Convert a password file to Apple Password format.
    
    Args:
        input_path: Path to input file
        output_path: Path to output CSV file
        log_level: Logging level (default: INFO)
        log_file: Optional path to log file
    """
    # from .utils import setup_logging
    from .utils import setup_logging
    
    # Convert paths to Path objects
    input_path = Path(input_path)
    output_path = Path(output_path)
    log_file = Path(log_file) if log_file else None
    
    # Setup logging
    setup_logging(log_level, log_file)
    
    try:
        converter = PasswordConverter(input_path, output_path)
        sections = converter.read_file()
        blocks = converter.parse_blocks(sections)
        apple_format = converter.convert_to_apple_format(blocks)
        converter.save_csv(apple_format, output_path)
        logger.info(f"Successfully converted {len(apple_format)} entries")
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise

def convert_text(text: str) -> List[Dict[str, str]]:
    """
    Convert password text directly to Apple Password format.
    
    Args:
        text: Input text in the expected format
        
    Returns:
        List of dictionaries in Apple Password format
    """
    converter = PasswordConverter()
    sections = [section.strip() for section in text.split("---") if section.strip()]
    blocks = converter.parse_blocks(sections)
    return converter.convert_to_apple_format(blocks)

# Add a main function to choose between file and text conversion

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert password file to Apple Password format")
    parser.add_argument("input", help="Path to input file or text")
    parser.add_argument("output", help="Path to output CSV file")
    parser.add_argument("--log-level", default="INFO", help="Logging level (default: INFO)")
    parser.add_argument("--log-file", help="Path to log file")
    args = parser.parse_args()
    
    if Path(args.input).is_file():
        convert_file(args.input, args.output, args.log_level, args.log_file)
    else:
        data = convert_text(args.input)
        converter = PasswordConverter()
        converter.save_csv(data, Path(args.output))

if __name__ == "__main__":
    main()