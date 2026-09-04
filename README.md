# ExperimentLens V1

**ExperimentLens** — ML Experiment Intelligence for Dataset Analysis.

A minimal dataset intelligence and profiling engine that transforms raw CSV data into structured, actionable quality reports.

## What is ExperimentLens?

ExperimentLens V1 is a **dataset profiling and intelligence engine** designed to help data scientists and ML practitioners understand their datasets quickly. It answers critical questions about data quality without requiring configuration, ML modeling, or complex setup.

### What V1 Does

Given a CSV file, ExperimentLens V1:

1. **Validates** the file (size, format, structure)
2. **Profiles** the dataset (rows, columns, types, memory)
3. **Analyzes** data quality (missing values, duplicates)
4. **Computes** statistics (mean, median, quartiles, std dev)
5. **Detects** potential outliers using the IQR method
6. **Measures** skewness in numerical features
7. **Flags** potentially unnecessary features (with explanations, no auto-deletion)
8. **Catalogs** categorical column profiles
9. **Generates** actionable warnings

### What V1 Does NOT Do

- ❌ Automatically clean or modify data
- ❌ Build ML models or make predictions
- ❌ Provide interactive dashboards
- ❌ Require authentication or databases
- ❌ Accept JSON or other input formats
- ❌ Perform complex NLP or text analysis

## Input Contract

**Format:** CSV only  
**Maximum file size:** 10 MB  
**Encoding:** UTF-8 supported

If a file exceeds 10 MB, ExperimentLens rejects it gracefully with a clear error message.

Common issues are handled safely:
- Malformed CSV → descriptive error
- Empty dataset → graceful notification
- Missing headers → works (columns named by position)
- Encoding issues → attempted recovery or clear error
- Inconsistent rows → analysis proceeds with available data

## Installation

```bash
git clone https://github.com/AANAND4YADAV/experimentlens.git
cd experimentlens
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from src.experimentlens.ingestion import load_csv
from src.experimentlens.validation import validate_file_size, validate_dataframe
from src.experimentlens.reporting import generate_report

# Load and validate
df = load_csv("data.csv")
is_valid, msg = validate_dataframe(df)

if is_valid:
    # Generate report
    report = generate_report(df)
    print(report)
else:
    print(f"Validation failed: {msg}")
```

## Analysis Pipeline

### 1. Dataset Overview
- Rows, columns, names, data types
- Memory usage
- First 5 rows (preview, not full dump)

### 2. Missing Value Analysis
Per column:
- Missing count and percentage
- Clear distinction between "no missing" and "missing detected"

### 3. Duplicate Row Analysis
- Total duplicates and percentage
- Reported but not deleted (data integrity preserved)

### 4. Numerical Statistics
For numerical columns:
- Count, mean, median, std dev
- Min, Q1, Q2, Q3, max
- Safe handling for columns with no variation

### 5. Outlier Detection (IQR Method)
Per numerical column:
- Q1, Q3, IQR
- Lower/upper bounds
- Outlier count and percentage

**IQR Formula:**
```
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

**Important:** Outliers are *detected* and *reported*, never removed.

### 6. Skewness Analysis
Per numerical column:
- Skewness coefficient
- Heuristic interpretation (approximate symmetry, moderate/high skew)
- Always provides raw value

### 7. Feature Quality Analysis
Flags potentially unnecessary features:
- Completely empty columns
- Constant columns (single unique value)
- Possible identifiers (>95% unique)
- Very low cardinality (<5 unique values)
- Duplicate columns
- Index-like column names (Unnamed, index)

**Important:** These are *recommendations only*. No automatic deletion.

### 8. Categorical Column Profiling
Per text/categorical column:
- Unique value count
- Missing count
- Most frequent value and its count

### 9. Dataset Warnings
Actionable findings based on computed evidence:
- "Column age contains 8.2% missing values."
- "income contains 37 potential outliers (IQR method)."
- "customer_id appears to be identifier-like."
- "salary is highly skewed (skewness: 2.15)."

## Example Output Structure

```python
{
    "dataset": {
        "num_rows": 1000,
        "num_columns": 5,
        "column_names": [...],
        "data_types": {...},
        "memory_usage_mb": 0.05,
        "head": [...]
    },
    "missing_values": {
        "has_missing_values": True,
        "columns": {"age": {"missing_count": 45, "missing_percentage": 4.5}, ...}
    },
    "duplicates": {
        "total_rows": 1000,
        "duplicate_rows": 12,
        "duplicate_percentage": 1.2,
        "has_duplicates": True
    },
    "statistics": {
        "age": {"count": 955, "mean": 42.3, "median": 40.0, ...},
        "salary": {...}
    },
    "outliers": {
        "salary": {
            "q1": 35000,
            "q3": 95000,
            "iqr": 60000,
            "lower_bound": -55000,
            "upper_bound": 185000,
            "outlier_count": 8,
            "outlier_percentage": 0.8
        }
    },
    "skewness": {
        "salary": {"skewness": 1.8, "interpretation": "highly skewed"}
    },
    "potentially_unnecessary_features": [
        {"column": "id", "reason": "Possible identifier", "metric": "99.9% unique"}
    ],
    "categorical_profile": {
        "region": {"unique_count": 4, "missing_count": 0, "most_frequent_value": "North", ...}
    },
    "warnings": [
        "Column 'age' contains 45 (4.5%) missing values.",
        "Dataset contains 12 (1.2%) duplicate rows.",
        "Column 'salary' contains 8 (0.8%) potential outliers (IQR method).",
        "Column 'salary' is highly skewed (skewness: 1.796)."
    ]
}
```

## Key Design Principles

1. **Data Integrity First:** Original data is never modified or deleted during analysis.
2. **No Over-Engineering:** Minimal dependencies, focused scope.
3. **Structured Output:** Analysis results are dictionaries, not formatted strings.
4. **Evidence-Based:** Every warning is grounded in computed metrics.
5. **Graceful Error Handling:** Bad input produces clear messages, not crashes.
6. **Deterministic:** Same input always produces same output.

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Tests cover:
- Valid CSV loading
- File size validation
- Malformed CSV handling
- Empty dataset handling
- Missing value detection
- Duplicate detection
- Numerical statistics
- IQR outlier detection
- Skewness calculation
- Feature quality flags
- Categorical profiling

## Limitations

- CSV only (no Excel, JSON, Parquet, etc.)
- 10 MB file size limit
- No interactive visualization
- No ML modeling or prediction
- No data cleaning or transformation
- No authentication or multi-user support
- No database persistence
- Single-threaded processing

## License

MIT License. See LICENSE file for details.

## Next Steps (Future Versions)

- Web UI for report visualization
- Support for additional input formats
- Advanced correlation analysis
- Time-series pattern detection
- Integration with experiment tracking systems
- Collaborative dataset sharing
