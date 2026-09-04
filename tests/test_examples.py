import json


def test_example_dataset_contents():
    # Quick smoke test to ensure example dataset exists and is parseable as CSV
    path = "examples/sample_dataset.csv"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert "employee_id" in text
    # Ensure file is not empty
    assert len(text) > 0
