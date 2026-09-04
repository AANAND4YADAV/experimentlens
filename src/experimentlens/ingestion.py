"""CSV file ingestion and loading with robust error handling."""

import pandas as pd
import os
from pathlib import Path
from typing import Union


MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


class IngestionError(Exception):
    """Base exception for ingestion errors."""
    pass


class FileSizeError(IngestionError):
    """Raised when file exceeds size limit."""
    pass


class EncodingError(IngestionError):
    """Raised when file encoding cannot be handled."""
    pass


class MalformedCSVError(IngestionError):
    """Raised when CSV structure is invalid."""
    pass


def _validate_file_size(filepath: Union[str, Path]) -> None:
    """Validate that file size does not exceed 10 MB.
    
    Args:
        filepath: Path to the file.
    
    Raises:
        FileSizeError: If file exceeds 10 MB.
    """
    path = Path(filepath)
    file_size = path.stat().st_size
    
    if file_size > MAX_FILE_SIZE_BYTES:
        size_mb = file_size / (1024 * 1024)
        raise FileSizeError(
            f"File size ({size_mb:.2f} MB) exceeds maximum allowed 10 MB."
        )


def _validate_file_exists(filepath: Union[str, Path]) -> None:
    """Validate that file exists.
    
    Args:
        filepath: Path to the file.
    
    Raises:
        FileNotFoundError: If file does not exist.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")


def _is_csv_file(filepath: Union[str, Path]) -> bool:
    """Check if file has .csv extension.
    
    Args:
        filepath: Path to the file.
    
    Returns:
        bool: True if file has .csv extension (case-insensitive).
    """
    path = Path(filepath)
    return path.suffix.lower() == ".csv"


def load_csv(filepath: Union[str, Path]) -> pd.DataFrame:
    """Load a CSV file into a DataFrame with comprehensive error handling.
    
    This function:
    - Validates file exists and is a CSV
    - Checks file size (max 10 MB)
    - Handles encoding errors gracefully
    - Detects malformed CSV structure
    - Preserves original data (does not modify)
    - Does not silently skip malformed rows
    
    Args:
        filepath: Path to the CSV file.
    
    Returns:
        pandas.DataFrame: Loaded data (copy of original, not modified).
    
    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file is not a CSV.
        FileSizeError: If file exceeds 10 MB.
        EncodingError: If file encoding cannot be handled.
        MalformedCSVError: If CSV structure is invalid.
    """
    # Validate file exists
    _validate_file_exists(filepath)
    
    # Validate file is CSV
    if not _is_csv_file(filepath):
        raise ValueError(
            f"Invalid file format. Expected CSV file, got: {Path(filepath).suffix}"
        )
    
    # Validate file size
    _validate_file_size(filepath)
    
    filepath = str(filepath)
    
    # Try to load CSV with UTF-8 encoding first
    try:
        df = pd.read_csv(filepath, dtype=None)
    except UnicodeDecodeError as e:
        raise EncodingError(
            f"Unable to decode file. Expected UTF-8 encoding. Error: {str(e)}"
        )
    except pd.errors.ParserError as e:
        raise MalformedCSVError(
            f"CSV file is malformed and cannot be parsed. Error: {str(e)}"
        )
    except Exception as e:
        raise MalformedCSVError(
            f"Unexpected error while parsing CSV: {str(e)}"
        )
    
    # Return a copy to prevent external modifications
    return df.copy()
