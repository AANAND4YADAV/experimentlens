"""Report generation and aggregation."""

import pandas as pd
from typing import Dict, Any, List

from .profiling import profile_dataset
from .missing_values import analyze_missing_values
from .duplicates import analyze_duplicates
from .statistics import analyze_statistics
from .outliers import detect_outliers_iqr
from .skewness import analyze_skewness
from .feature_analysis import analyze_unnecessary_features, profile_categorical_columns


def generate_report(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate a comprehensive dataset analysis report.
    
    This is the main entry point for analysis.
    
    Args:
        df: pandas DataFrame to analyze. Must be validated before calling.
    
    Returns:
        Dict containing the complete analysis report.
    """
    # Run all analyses
    dataset_profile = profile_dataset(df)
    missing_analysis = analyze_missing_values(df)
    duplicate_analysis = analyze_duplicates(df)
    statistics = analyze_statistics(df)
    outliers = detect_outliers_iqr(df)
    skewness = analyze_skewness(df)
    unnecessary_features = analyze_unnecessary_features(df)
    categorical_profiles = profile_categorical_columns(df)
    
    # Generate warnings
    warnings = _generate_warnings(
        df,
        missing_analysis,
        duplicate_analysis,
        outliers,
        skewness,
        unnecessary_features,
    )
    
    report = {
        "dataset": dataset_profile,
        "missing_values": missing_analysis,
        "duplicates": duplicate_analysis,
        "statistics": statistics,
        "outliers": outliers,
        "skewness": skewness,
        "potentially_unnecessary_features": unnecessary_features,
        "categorical_profile": categorical_profiles,
        "warnings": warnings,
    }
    
    return report


def _generate_warnings(df: pd.DataFrame, missing_analysis: Dict, duplicate_analysis: Dict,
                      outliers: Dict, skewness: Dict, unnecessary_features: List) -> List[str]:
    """Generate actionable warnings based on analysis results.
    
    Args:
        df: Original DataFrame.
        missing_analysis: Result from analyze_missing_values.
        duplicate_analysis: Result from analyze_duplicates.
        outliers: Result from detect_outliers_iqr.
        skewness: Result from analyze_skewness.
        unnecessary_features: Result from analyze_unnecessary_features.
    
    Returns:
        List of warning strings.
    """
    warnings = []
    
    # Missing value warnings
    for col, stats in missing_analysis["columns"].items():
        if stats["missing_count"] > 0:
            warnings.append(
                f"Column '{col}' contains {stats['missing_count']} "
                f"({stats['missing_percentage']:.1f}%) missing values."
            )
    
    # Duplicate warnings
    if duplicate_analysis["has_duplicates"]:
        warnings.append(
            f"Dataset contains {duplicate_analysis['duplicate_rows']} "
            f"({duplicate_analysis['duplicate_percentage']:.1f}%) duplicate rows."
        )
    
    # Outlier warnings
    for col, stats in outliers.items():
        if "error" not in stats and stats.get("outlier_count", 0) > 0:
            warnings.append(
                f"Column '{col}' contains {stats['outlier_count']} "
                f"({stats['outlier_percentage']:.1f}%) potential outliers (IQR method)."
            )
    
    # Skewness warnings
    for col, stats in skewness.items():
        if "error" not in stats:
            if abs(stats["skewness"]) >= 1.5:
                warnings.append(
                    f"Column '{col}' is {stats['interpretation']} "
                    f"(skewness: {stats['skewness']:.3f})."
                )
    
    # Feature quality warnings
    for feature_flag in unnecessary_features:
        warnings.append(
            f"Column '{feature_flag['column']}' — {feature_flag['reason']} "
            f"({feature_flag['metric']})."
        )
    
    return warnings
