"""Duplicate row analysis."""

import pandas as pd
from typing import Dict, Any


def analyze_duplicates(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze duplicate rows in the dataset.
    
    Args:
        df: pandas DataFrame to analyze.
    
    Returns:
        Dict containing duplicate statistics.
    """
    duplicate_count = df.duplicated().sum()
    duplicate_percentage = (duplicate_count / len(df)) * 100 if len(df) > 0 else 0
    
    return {
        "total_rows": len(df),
        "duplicate_rows": int(duplicate_count),
        "duplicate_percentage": float(duplicate_percentage),
        "has_duplicates": duplicate_count > 0,
    }
