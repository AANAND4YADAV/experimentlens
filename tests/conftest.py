"""Pytest configuration and shared fixtures."""

import pytest
import pandas as pd
import tempfile
from pathlib import Path


@pytest.fixture
def sample_valid_csv(tmp_path):
    """Create a valid sample CSV for testing."""
    data = {
        "age": [25, 30, 35, 40, 45, 50, None, 28, 32, 38],
        "salary": [50000, 60000, 75000, 80000, 95000, 120000, 55000, 58000, 70000, 85000],
        "region": ["North", "South", "North", "East", "West", "South", "North", "East", "West", "South"],
        "experience": [2, 5, 8, 10, 12, 20, 3, 6, 9, 11],
    }
    df = pd.DataFrame(data)
    filepath = tmp_path / "sample.csv"
    df.to_csv(filepath, index=False)
    return str(filepath)


@pytest.fixture
def sample_empty_csv(tmp_path):
    """Create an empty CSV for testing."""
    filepath = tmp_path / "empty.csv"
    filepath.write_text("col1,col2,col3\n")
    return str(filepath)


@pytest.fixture
def sample_malformed_csv(tmp_path):
    """Create a malformed CSV for testing."""
    filepath = tmp_path / "malformed.csv"
    filepath.write_text("col1,col2,col3\n1,2\n3,4,5,6")
    return str(filepath)


@pytest.fixture
def sample_outlier_csv(tmp_path):
    """Create a CSV with obvious outliers for testing IQR detection."""
    data = {
        "value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1000],  # 1000 is an obvious outlier
    }
    df = pd.DataFrame(data)
    filepath = tmp_path / "outliers.csv"
    df.to_csv(filepath, index=False)
    return str(filepath)


@pytest.fixture
def sample_constant_column_csv(tmp_path):
    """Create a CSV with constant columns."""
    data = {
        "constant_col": [5, 5, 5, 5, 5],
        "normal_col": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)
    filepath = tmp_path / "constant.csv"
    df.to_csv(filepath, index=False)
    return str(filepath)


@pytest.fixture
def sample_duplicates_csv(tmp_path):
    """Create a CSV with duplicate rows."""
    data = {
        "id": [1, 2, 3, 2, 1],
        "name": ["Alice", "Bob", "Charlie", "Bob", "Alice"],
    }
    df = pd.DataFrame(data)
    filepath = tmp_path / "duplicates.csv"
    df.to_csv(filepath, index=False)
    return str(filepath)


@pytest.fixture
def sample_skewed_csv(tmp_path):
    """Create a CSV with skewed numerical distribution."""
    # Right-skewed data (long tail to the right)
    data = {
        "income": [20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 1000000],
    }
    df = pd.DataFrame(data)
    filepath = tmp_path / "skewed.csv"
    df.to_csv(filepath, index=False)
    return str(filepath)
