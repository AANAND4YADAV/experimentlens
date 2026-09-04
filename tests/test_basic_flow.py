import pytest
import pandas as pd
from src.experimentlens.ingestion import load_csv
from src.experimentlens.validation import validate_file_size, validate_dataframe
from src.experimentlens.reporting import generate_report


def test_load_valid_csv(tmp_path):
    # Use the provided example dataset in the repository
    sample = "examples/sample_dataset.csv"
    df = load_csv(sample)
    assert isinstance(df, pd.DataFrame)
    assert "employee_id" in df.columns
    assert df.shape[0] > 0


def test_file_size_validation():
    sample = "examples/sample_dataset.csv"
    is_valid, msg = validate_file_size(sample)
    assert is_valid is True


def test_validate_dataframe_and_report():
    sample = "examples/sample_dataset.csv"
    df = load_csv(sample)
    is_valid, msg = validate_dataframe(df)
    assert is_valid is True

    report = generate_report(df)
    # Basic structure checks
    assert "dataset" in report
    assert "missing_values" in report
    assert "statistics" in report
    assert "outliers" in report
    assert "skewness" in report
    assert "warnings" in report

    # Ensure dataset metadata contains expected fields
    ds = report["dataset"]
    assert "column_names" in ds
    assert "employee_id" in ds["column_names"]
