"""Missing value analysis."""

import pandas as pd
from typing import Dict, Any


def analyze_missing_values(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze missing values across all columns.
    
    Args:
        df: pandas DataFrame to analyze.
    
    Returns:
        Dict containing missing value statistics.
    """
    missing_stats = {}
    has_missing = False
    
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_percentage = (missing_count / len(df)) * 100 if len(df) > 0 else 0
        
        if missing_count > 0:
            has_missing = True
        
        missing_stats[col] = {
            "missing_count": int(missing_count),
            "missing_percentage": float(missing_percentage),
        }
    
    return {
        "has_missing_values": has_missing,
        "columns": missing_stats,
    }
