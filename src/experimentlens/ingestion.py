"""CSV file ingestion and loading."""

import pandas as pd
from pathlib import Path
from typing import Union


def load_csv(filepath: Union[str, Path]) -> pd.DataFrame:
    """Load a CSV file into a DataFrame.
    
    Args:
        filepath: Path to the CSV file.
    
    Returns:
        pandas.DataFrame: Loaded data.
    
    Raises:
        FileNotFoundError: If file does not exist.
        pd.errors.ParserError: If CSV is malformed.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    return pd.read_csv(filepath)
