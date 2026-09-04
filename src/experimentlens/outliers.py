"""Outlier detection using IQR method."""

import pandas as pd
from typing import Dict, Any


def detect_outliers_iqr(df: pd.DataFrame) -> Dict[str, Any]:
    """Detect outliers using the Interquartile Range (IQR) method.
    
    For each numerical column:
    - IQR = Q3 - Q1
    - Lower Bound = Q1 - 1.5 * IQR
    - Upper Bound = Q3 + 1.5 * IQR
    - Outliers are values < Lower Bound or > Upper Bound
    
    Args:
        df: pandas DataFrame to analyze.
    
    Returns:
        Dict mapping column names to their outlier analysis.
    """
    outliers = {}
    
    for col in df.select_dtypes(include=['number']).columns:
        try:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            
            # Handle case where IQR is 0 (constant column)
            if iqr == 0:
                outliers[col] = {
                    "q1": float(q1),
                    "q3": float(q3),
                    "iqr": float(iqr),
                    "lower_bound": float(q1),
                    "upper_bound": float(q3),
                    "outlier_count": 0,
                    "outlier_percentage": 0.0,
                    "note": "No variation in column (IQR = 0)."
                }
                continue
            
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            outlier_percentage = (outlier_count / len(df)) * 100
            
            outliers[col] = {
                "q1": float(q1),
                "q3": float(q3),
                "iqr": float(iqr),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "outlier_count": int(outlier_count),
                "outlier_percentage": float(outlier_percentage),
            }
        except Exception as e:
            outliers[col] = {"error": str(e)}
    
    return outliers
