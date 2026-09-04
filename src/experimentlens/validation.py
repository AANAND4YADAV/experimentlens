"""CSV validation and data integrity checks."""

import pandas as pd
from pathlib import Path
from typing import Union, Tuple

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


class ValidationError(Exception):
    """Base exception for validation errors."""
    pass


class EmptyDatasetError(ValidationError):
    """Raised when dataset is empty."""
    pass


class InvalidHeaderError(ValidationError):
    """Raised when header is invalid."""
    pass


def validate_file_size(filepath: Union[str, Path]) -> Tuple[bool, str]:
    """Validate that file size does not exceed 10 MB.
    
    Args:
        filepath: Path to the file.
    
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    path = Path(filepath)
    file_size = path.stat().st_size
    
    if file_size > MAX_FILE_SIZE_BYTES:
        size_mb = file_size / (1024 * 1024)
        return False, f"File size ({size_mb:.2f} MB) exceeds 10 MB limit."
    
    return True, "File size is valid."


def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate that DataFrame is not empty and has valid structure.
    
    Args:
        df: pandas DataFrame to validate.
    
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if df.empty:
        return False, "Dataset is empty (no rows or columns)."
    
    if df.shape[0] == 0:
        return False, "Dataset contains no rows."
    
    if df.shape[1] == 0:
        return False, "Dataset contains no columns."
    
    return True, "DataFrame is valid."


def validate_header(df: pd.DataFrame, require_header: bool = True) -> Tuple[bool, str]:
    """Validate that DataFrame has a valid header (column names).
    
    Args:
        df: pandas DataFrame to validate.
        require_header: If True, require non-empty column names.
    
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if require_header:
        if len(df.columns) == 0:
            return False, "DataFrame has no columns/header."
        
        # Check if all columns are unnamed or default-named
        if all(str(col).startswith("Unnamed:") for col in df.columns):
            return False, "DataFrame has no valid header; all columns are unnamed."
    
    return True, "Header is valid."
