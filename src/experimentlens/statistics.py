"""Statistical analysis of numerical columns."""

import pandas as pd
from typing import Dict, Any


def analyze_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate numerical statistics for all columns.
    
    Args:
        df: pandas DataFrame to analyze.
    
    Returns:
        Dict mapping column names to their statistics.
    """
    statistics = {}
    
    for col in df.select_dtypes(include=['number']).columns:
        try:
            stats = {
                "count": int(df[col].count()),
                "mean": float(df[col].mean()),
                "median": float(df[col].median()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "q1": float(df[col].quantile(0.25)),
                "q2": float(df[col].quantile(0.50)),
                "q3": float(df[col].quantile(0.75)),
                "max": float(df[col].max()),
            }
            statistics[col] = stats
        except Exception as e:
            statistics[col] = {"error": str(e)}
    
    return statistics
