"""Skewness analysis for numerical columns."""

import pandas as pd
from typing import Dict, Any


def analyze_skewness(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate skewness for numerical columns.
    
    Interpretation guide (heuristic, not universal):
    - |skewness| < 0.5: approximately symmetric
    - 0.5 <= |skewness| < 1.5: moderately skewed
    - |skewness| >= 1.5: highly skewed
    
    Args:
        df: pandas DataFrame to analyze.
    
    Returns:
        Dict mapping column names to skewness statistics.
    """
    skewness_stats = {}
    
    for col in df.select_dtypes(include=['number']).columns:
        try:
            skewness_value = df[col].skew()
            
            # Qualitative interpretation
            if abs(skewness_value) < 0.5:
                interpretation = "approximately symmetric"
            elif abs(skewness_value) < 1.5:
                interpretation = "moderately skewed"
            else:
                interpretation = "highly skewed"
            
            skewness_stats[col] = {
                "skewness": float(skewness_value),
                "interpretation": interpretation,
            }
        except Exception as e:
            skewness_stats[col] = {"error": str(e)}
    
    return skewness_stats
