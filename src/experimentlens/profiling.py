"""Dataset profiling and overview analysis."""

import pandas as pd
from typing import Dict, Any, List


def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate a dataset overview profile.
    
    Args:
        df: pandas DataFrame to profile.
    
    Returns:
        Dict containing dataset overview information.
    """
    profile = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "column_names": list(df.columns),
        "data_types": {col: str(df[col].dtype) for col in df.columns},
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 ** 2),
        "head": df.head(5).to_dict(orient="records"),
    }
    return profile
