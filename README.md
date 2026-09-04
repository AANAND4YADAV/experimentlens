# ExperimentLens V1

**ExperimentLens** — Minimal ML Dataset Intelligence and Profiling Engine.

A lightweight dataset profiling and analysis tool that transforms raw CSV data into structured, evidence-based quality reports. Designed for data scientists and ML practitioners who need quick, reliable dataset insights.

---

## What is ExperimentLens?

### The Problem

Data scientists spend significant time understanding new datasets before modeling. Questions like "What's missing in this data?", "Are there outliers?", and "Which features look suspicious?" require manual inspection or scattered tools.

### The Solution

ExperimentLens V1 provides **automated, deterministic dataset profiling** in a single call. It analyzes your CSV, computes structured metrics, and generates actionable warnings—no data modification, no assumptions, just facts.

---

## Current V1 Capabilities

ExperimentLens V1 analyzes CSV datasets and produces a comprehensive structured report containing:

### Input & Validation
- **CSV Format Only**: Accepts well-formed UTF-8 CSV files
- **10 MB Size Limit**: Gracefully rejects files exceeding 10 MB with clear error messages
- **Robust Error Handling**: Detects malformed CSV, encoding issues, empty datasets, and provides descriptive feedback

### Dataset Overview
- Row and column counts
- Column names and data types
- Memory usage
- First 5 rows (preview snapshot)

### Data Quality Analysis

**Missing Values**
- Per-column missing value count and percentage
- Clear distinction between "no missing" and "missing detected"

**Duplicate Rows**
- Total duplicate count and percentage
- Flags duplicates without removing them (data integrity preserved)

**Numerical Statistics** (for numeric columns)
- Count, mean, median, standard deviation
- Min, Q1 (25th percentile), Q2 (50th percentile), Q3 (75th percentile), max
- Safe handling for columns with no variation

**Outlier Detection (IQR Method)**
- Per-column outlier identification using Interquartile Range
- Q1, Q3, IQR values
- Lower/upper bounds: `Q1 - 1.5 × IQR` and `Q3 + 1.5 × IQR`
- Outlier count and percentage
- **Important**: Outliers are *detected and reported*, never removed

**Skewness Analysis**
- Skewness coefficient for each numerical column
- Heuristic interpretation (approximately symmetric, moderately/highly skewed)
- Raw skewness value always provided

### Feature Quality Analysis

Identifies potentially unnecessary or suspicious features:
- **Completely empty columns**: All values missing
- **Constant columns**: Single unique value across all rows
- **Identifier-like columns**: >95% unique values (likely IDs)
- **Index-like columns**: Column names matching `Unnamed`, `index`, etc.
- **Duplicate columns**: Identical content as another column
- **Very low cardinality**: Fewer than 5 unique values (flagged for review)

**Important**: These are *recommendations only*. No automatic deletion.

### Categorical Column Profiling
- Per text/categorical column unique value count
- Missing value count
- Most frequent value and its frequency

### Actionable Warnings

Automatically generated warnings based on computed evidence:
- "Column 'age' contains 45 (4.5%) missing values."
- "Dataset contains 12 (1.2%) duplicate rows."
- "Column 'salary' contains 8 (0.8%) potential outliers (IQR method)."
- "Column 'salary' is highly skewed (skewness: 1.796)."
- "Column 'customer_id' appears to be identifier-like (99.9% unique)."

---

## Installation

### Requirements
- Python 3.7+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/AANAND4YADAV/experimentlens.git
cd experimentlens

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "from src.experimentlens.reporting import generate_report; print('ExperimentLens loaded successfully')"
```

---

## How to Test

Run the complete test suite:

```bash
python -m pytest tests/ -v
```

### What Tests Verify

The test suite validates:
- CSV file loading and format handling
- File size validation (10 MB limit)
- Malformed CSV detection
- Empty dataset handling
- Missing value detection and calculation
- Duplicate row detection
- Numerical statistics computation
- IQR-based outlier detection
- Skewness calculation
- Feature quality flag accuracy
- Categorical column profiling
- End-to-end report generation

### Example Test Output

```
tests/conftest.py ...                                           [X%]
tests/test_ingestion.py::test_load_valid_csv PASSED              [X%]
tests/test_validation.py::test_file_size_validation PASSED       [X%]
tests/test_missing_values.py::test_missing_detection PASSED      [X%]
tests/test_duplicates.py::test_duplicate_detection PASSED        [X%]
tests/test_statistics.py::test_numerical_stats PASSED            [X%]
tests/test_outliers.py::test_iqr_detection PASSED                [X%]
tests/test_skewness.py::test_skewness_calculation PASSED         [X%]
tests/test_feature_analysis.py::test_feature_quality PASSED      [X%]
tests/test_reporting.py::test_report_generation PASSED           [X%]

============================== N passed in X.XXs ==============================
```

---

## How to Run the Example Dataset

### Example CSV Location

A sample employee dataset is included at:
```
examples/sample_dataset.csv
```

The dataset contains 151 employee records with fields:
- `employee_id` (identifier)
- `age` (numeric, with some missing values)
- `salary` (numeric)
- `region` (categorical)
- `department` (categorical)
- `years_experience` (numeric)
- `is_manager` (boolean)
- `bonus_pct` (numeric)
- `hire_date` (text/date)

### Running the Analysis

Create a test script (e.g., `run_example.py`):

```python
from src.experimentlens.ingestion import load_csv
from src.experimentlens.validation import validate_file_size, validate_dataframe
from src.experimentlens.reporting import generate_report
import json

# Load and validate
csv_path = "examples/sample_dataset.csv"
is_valid, msg = validate_file_size(csv_path)
if not is_valid:
    print(f"File validation failed: {msg}")
    exit(1)

df = load_csv(csv_path)
is_valid, msg = validate_dataframe(df)
if not is_valid:
    print(f"DataFrame validation failed: {msg}")
    exit(1)

# Generate report
report = generate_report(df)

# Display key sections
print("\n=== DATASET OVERVIEW ===")
print(f"Rows: {report['dataset']['num_rows']}")
print(f"Columns: {report['dataset']['num_columns']}")
print(f"Column names: {report['dataset']['column_names']}")

print("\n=== MISSING VALUES ===")
for col, stats in report['missing_values']['columns'].items():
    if stats['missing_count'] > 0:
        print(f"  {col}: {stats['missing_count']} ({stats['missing_percentage']:.1f}%)")

print("\n=== DUPLICATES ===")
print(f"Duplicate rows: {report['duplicates']['duplicate_rows']} ({report['duplicates']['duplicate_percentage']:.1f}%)")

print("\n=== NUMERICAL STATISTICS (sample) ===")
if 'salary' in report['statistics']:
    stats = report['statistics']['salary']
    print(f"  salary: mean={stats['mean']:.2f}, median={stats['median']:.2f}, std={stats['std']:.2f}")

print("\n=== OUTLIERS (sample) ===")
if 'salary' in report['outliers']:
    outlier_info = report['outliers']['salary']
    print(f"  salary: {outlier_info['outlier_count']} outliers ({outlier_info['outlier_percentage']:.1f}%)")

print("\n=== SKEWNESS (sample) ===")
if 'salary' in report['skewness']:
    skew_info = report['skewness']['salary']
    print(f"  salary: {skew_info['skewness']:.3f} ({skew_info['interpretation']})")

print("\n=== FLAGGED FEATURES ===")
for feature in report['potentially_unnecessary_features']:
    print(f"  {feature['column']}: {feature['reason']}")

print("\n=== WARNINGS ===")
for warning in report['warnings']:
    print(f"  • {warning}")

print("\n=== FULL REPORT ===")
print(json.dumps(report, indent=2, default=str))
```

Run it:
```bash
python run_example.py
```

### Expected Output Summary

```
=== DATASET OVERVIEW ===
Rows: 151
Columns: 9
Column names: ['employee_id', 'age', 'salary', 'region', 'department', 'years_experience', 'is_manager', 'bonus_pct', 'hire_date']

=== MISSING VALUES ===
  age: 8 (5.3%)

=== DUPLICATES ===
Duplicate rows: 0 (0.0%)

=== NUMERICAL STATISTICS (sample) ===
  salary: mean=62894.77, median=62000.00, std=16847.23

=== OUTLIERS (sample) ===
  salary: 1 outliers (0.7%)

=== SKEWNESS (sample) ===
  salary: 4.812 (highly skewed)

=== FLAGGED FEATURES ===
  employee_id: Possible identifier (100.0% unique)

=== WARNINGS ===
  • Column 'age' contains 8 (5.3%) missing values.
  • Column 'employee_id' appears to be identifier-like (100.0% unique).
  • Column 'salary' contains 1 (0.7%) potential outliers (IQR method).
  • Column 'salary' is highly skewed (skewness: 4.812).
```

---

## Project Structure

```
experimentlens/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
│
├── src/
│   └── experimentlens/
│       ├── __init__.py               # Package initialization
│       ├── ingestion.py              # CSV loading with error handling
│       ├── validation.py             # File and DataFrame validation
│       ├── profiling.py              # Dataset overview profiling
│       ├── missing_values.py         # Missing value analysis
│       ├── duplicates.py             # Duplicate row detection
│       ├── statistics.py             # Numerical statistics computation
│       ├── outliers.py               # IQR-based outlier detection
│       ├── skewness.py               # Skewness analysis
│       ├── feature_analysis.py       # Feature quality flagging & categorical profiling
│       └── reporting.py              # Report generation & warning aggregation
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Pytest fixtures and configuration
│   └── test_*.py                     # Test modules (created per-feature)
│
└── examples/
    ├── sample_dataset.csv            # Example employee dataset for testing
    └── .gitkeep
```

---

## What V1 Does NOT Do

ExperimentLens V1 is intentionally **minimal and focused**. It does not:

- ❌ **Automatically clean or modify data** — Analysis only, no transformations
- ❌ **Delete or remove features** — Only flags suspicious columns for human review
- ❌ **Build ML models or make predictions** — Not a modeling tool
- ❌ **Provide interactive dashboards or UI** — Structured JSON output only
- ❌ **Accept non-CSV formats** — CSV only (no Excel, JSON, Parquet, etc.)
- ❌ **Support large files** — Hard limit at 10 MB
- ❌ **Require databases or authentication** — Single-file, standalone tool
- ❌ **Perform advanced NLP or text analysis** — Basic categorical profiling only
- ❌ **Compute correlations or relationships** — Single-column analysis only
- ❌ **Detect time-series patterns** — No temporal analysis
- ❌ **Integrate with experiment tracking** — Standalone reporting tool

These are intentional boundaries for V1. Future versions may expand scope.

---

## Design Principles

ExperimentLens V1 is built on these core principles:

1. **Data Integrity First**
   - Original data is never modified, deleted, or overwritten
   - Analysis is read-only; changes are never persisted back to the file
   - Warnings and flags are recommendations only

2. **Deterministic Analysis**
   - Same CSV input always produces identical output
   - No randomization, no probabilistic sampling
   - Reproducible results across runs and environments

3. **Structured Output**
   - Analysis results are returned as Python dictionaries/JSON, not formatted strings
   - Enables downstream integration and custom reporting
   - Machine-readable and parseable

4. **Evidence-Based Warnings**
   - Every warning is grounded in computed metrics with thresholds
   - No guessing or heuristics without justification
   - Warnings include the metric value for verification

5. **Graceful Error Handling**
   - Invalid input produces descriptive error messages, not crashes
   - Clear explanation of what went wrong and why
   - Partial analysis when possible (e.g., skip non-numeric columns for statistics)

6. **Minimal Dependencies**
   - Only `pandas` and `numpy` required
   - No heavy frameworks, APIs, or external services
   - Fast startup and lightweight footprint

7. **No Over-Engineering**
   - Focused scope: CSV profiling, not data pipelines
   - Simple, readable code over premature optimization
   - Explicit over implicit (clear logic, not magic)

---

## Example Output Structure

The `generate_report()` function returns a Python dictionary with this structure:

```python
{
    "dataset": {
        "num_rows": 151,
        "num_columns": 9,
        "column_names": ["employee_id", "age", "salary", ...],
        "data_types": {"employee_id": "object", "age": "float64", "salary": "int64", ...},
        "memory_usage_mb": 0.012,
        "head": [
            {"employee_id": "E001", "age": 28.0, "salary": 45000, ...},
            {"employee_id": "E002", "age": 35.0, "salary": 65000, ...},
            ...
        ]
    },
    "missing_values": {
        "has_missing_values": True,
        "columns": {
            "age": {"missing_count": 8, "missing_percentage": 5.3},
            "is_manager": {"missing_count": 0, "missing_percentage": 0.0},
            ...
        }
    },
    "duplicates": {
        "total_rows": 151,
        "duplicate_rows": 0,
        "duplicate_percentage": 0.0,
        "has_duplicates": False
    },
    "statistics": {
        "age": {
            "count": 143,
            "mean": 35.76,
            "median": 35.0,
            "std": 7.32,
            "min": 26.0,
            "q1": 29.75,
            "q2": 35.0,
            "q3": 41.25,
            "max": 50.0
        },
        "salary": { ... },
        ...
    },
    "outliers": {
        "salary": {
            "q1": 48000,
            "q3": 75000,
            "iqr": 27000,
            "lower_bound": -12000,
            "upper_bound": 135000,
            "outlier_count": 1,
            "outlier_percentage": 0.7
        },
        ...
    },
    "skewness": {
        "salary": {
            "skewness": 4.812,
            "interpretation": "highly skewed"
        },
        ...
    },
    "potentially_unnecessary_features": [
        {
            "column": "employee_id",
            "reason": "Possible identifier",
            "metric": "100.0% unique"
        },
        ...
    ],
    "categorical_profile": {
        "region": {
            "unique_count": 4,
            "missing_count": 0,
            "most_frequent_value": "North",
            "most_frequent_count": 40
        },
        ...
    },
    "warnings": [
        "Column 'age' contains 8 (5.3%) missing values.",
        "Column 'employee_id' appears to be identifier-like (100.0% unique).",
        "Column 'salary' contains 1 (0.7%) potential outliers (IQR method).",
        "Column 'salary' is highly skewed (skewness: 4.812)."
    ]
}
```

---

## Future Scope (Not V1)

These features are **not implemented in V1** but represent possible future directions:

- 🔮 **Web UI** — Visualize reports in a browser
- 🔮 **Data Visualization** — Charts, distributions, correlation heatmaps
- 🔮 **Additional File Formats** — Excel, Parquet, JSON, SQL databases
- 🔮 **Correlation Analysis** — Feature-to-feature relationships
- 🔮 **Time-Series Analysis** — Temporal patterns and trends
- 🔮 **Experiment Tracking Integration** — Link profiling to model experiments
- 🔮 **Richer Dataset Intelligence** — Domain-aware analysis, anomaly detection
- 🔮 **ML Workflow Integration** — Direct pipeline connectivity

---

## Dependencies

**Python 3.7+** with:
- `pandas >= 2.0.0` — DataFrame manipulation and CSV I/O
- `numpy >= 1.24.0` — Numerical computations (used by pandas)

See `requirements.txt` for exact versions.

---

## License

MIT License © 2026 AANAND YADAV

See [LICENSE](LICENSE) file for full text.

---

## Support & Contributing

For issues, questions, or contributions:
1. Check existing documentation in this README
2. Review test fixtures in `tests/conftest.py` for usage examples
3. Examine the example CSV in `examples/sample_dataset.csv`

---

## Changelog

### Version 0.1.0 (Initial Release)
- CSV input and validation
- Dataset overview profiling
- Missing value analysis
- Duplicate detection
- Numerical statistics
- IQR-based outlier detection
- Skewness analysis
- Feature quality analysis
- Categorical column profiling
- Actionable warning generation
