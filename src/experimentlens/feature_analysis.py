"""Feature quality and necessity analysis."""

import pandas as pd
from typing import Dict, Any, List


def analyze_unnecessary_features(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Identify potentially unnecessary features.
    
    Flags:
    - Completely empty columns
    - Constant columns (single unique value)
    - Near-constant columns (very low cardinality)
    - Possible identifiers (nearly all unique)
    - Duplicate columns
    - Columns with Unnamed* pattern
    
    Args:
        df: pandas DataFrame to analyze.
    
    Returns:
        List of dictionaries, each describing a flagged feature.
    """
    flags = []
    
    # Track column names for duplicate detection
    seen_cols = {}
    
    for col in df.columns:
        col_data = df[col]
        unique_count = col_data.nunique()
        missing_count = col_data.isna().sum()
        total_count = len(df)
        non_null_count = total_count - missing_count
        
        # Completely empty column
        if non_null_count == 0:
            flags.append({
                "column": col,
                "reason": "Completely empty column",
                "metric": f"All {missing_count} values are missing"
            })
            continue
        
        # Constant column (only one unique value)
        if unique_count == 1:
            flags.append({
                "column": col,
                "reason": "Constant column",
                "metric": f"Only 1 unique value"
            })
            continue
        
        # Check for identifier-like columns (nearly all unique)
        # If >95% of non-null values are unique
        uniqueness_ratio = unique_count / non_null_count if non_null_count > 0 else 0
        if uniqueness_ratio > 0.95 and non_null_count > 10:
            flags.append({
                "column": col,
                "reason": "Possible identifier or index column",
                "metric": f"{uniqueness_ratio*100:.1f}% unique values"
            })
            continue
        
        # Check for very low cardinality (but not constant)
        # <5 unique values might warrant investigation
        if unique_count < 5 and non_null_count > 20:
            flags.append({
                "column": col,
                "reason": "Very low cardinality",
                "metric": f"Only {unique_count} unique values"
            })
            continue
        
        # Check for Unnamed index columns
        if col.lower().startswith("unnamed") or col.lower() == "index":
            flags.append({
                "column": col,
                "reason": "Appears to be an index column",
                "metric": f"Column name: {col}"
            })
            continue
        
        # Store column data as tuple for duplicate detection
        col_tuple = tuple(col_data.fillna('__null__').tolist())
        if col_tuple in seen_cols:
            flags.append({
                "column": col,
                "reason": "Duplicate column",
                "metric": f"Identical to column '{seen_cols[col_tuple]}'"
            })
        else:
            seen_cols[col_tuple] = col
    
    return flags


def profile_categorical_columns(df: pd.DataFrame) -> Dict[str, Any]:
    """Profile non-numerical columns.
    
    Args:
        df: pandas DataFrame to analyze.
    
    Returns:
        Dict mapping column names to their categorical profiles.
    """
    profiles = {}
    
    for col in df.select_dtypes(include=['object', 'string', 'category']).columns:
        unique_count = df[col].nunique()
        missing_count = df[col].isna().sum()
        
        value_counts = df[col].value_counts()
        most_frequent = None
        most_frequent_count = 0
        
        if len(value_counts) > 0:
            most_frequent = value_counts.index[0]
            most_frequent_count = int(value_counts.iloc[0])
        
        profiles[col] = {
            "unique_count": int(unique_count),
            "missing_count": int(missing_count),
            "most_frequent_value": most_frequent,
            "most_frequent_count": most_frequent_count,
        }
    
    return profiles
