"""CSV validation and data integrity checks."""

import pandas as pd
from pathlib import Path
from typing import Union, Tuple

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


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
        return False, "Dataset is empty."
    
    if df.shape[0] == 0:
        return False, "Dataset contains no rows."
    
    if df.shape[1] == 0:
        return False, "Dataset contains no columns."
    
    return True, "DataFrame is valid."
