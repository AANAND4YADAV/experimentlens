# Pytest configuration and fixtures
import pytest
import pandas as pd
from src.experimentlens.ingestion import load_csv


@pytest.fixture(scope="session")
def sample_df():
    return load_csv("examples/sample_dataset.csv")
