import streamlit as st
import tempfile
import os
from pathlib import Path

from src.experimentlens.ingestion import load_csv, IngestionError
from src.experimentlens.validation import validate_dataframe
from src.experimentlens.reporting import generate_report

st.set_page_config(page_title="ExperimentLens V1", layout="wide")

st.title("ExperimentLens V1 — Dataset Profiling")

st.write("Upload a CSV file (max 10 MB) or use the example dataset included with the package.")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"]) 
use_example = st.button("Load example dataset")

csv_path = None

if use_example:
    csv_path = Path("examples/sample_dataset.csv")
    if not csv_path.exists():
        st.error("Example dataset not found in examples/sample_dataset.csv")

if uploaded_file is not None:
    # Enforce 10 MB limit (bytes)
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("File is too large. Maximum allowed size is 10 MB.")
    else:
        # Save to temporary file and pass path to ingestion.load_csv (which expects a file path)
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            csv_path = Path(tmp_path)
        except Exception as e:
            st.error(f"Failed to save uploaded file: {e}")


if csv_path is not None:
    try:
        # Use the existing ingestion pipeline (which validates size, encoding, etc.)
        df = load_csv(csv_path)

        # Validate DataFrame
        is_valid, msg = validate_dataframe(df)
        if not is_valid:
            st.error(f"Data validation failed: {msg}")
        else:
            report = generate_report(df)

            st.subheader("Dataset overview")
            ds = report.get("dataset", {})
            st.write(f"Rows: {ds.get('num_rows')}")
            st.write(f"Columns: {ds.get('num_columns')}")
            st.write("Column names:")
            st.write(ds.get("column_names"))

            st.subheader("Preview (first 5 rows)")
            try:
                st.dataframe(df.head(5))
            except Exception:
                st.write(ds.get("head"))

            st.subheader("Data types")
            dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
            st.json(dtypes)

            st.subheader("Missing values")
            st.json(report.get("missing_values"))

            st.subheader("Duplicate rows")
            st.json(report.get("duplicates"))

            st.subheader("Numerical statistics (sample)")
            st.json(report.get("statistics"))

            st.subheader("IQR Outlier analysis")
            st.json(report.get("outliers"))

            st.subheader("Skewness")
            st.json(report.get("skewness"))

            st.subheader("Potentially unnecessary features")
            st.json(report.get("potentially_unnecessary_features"))

            st.subheader("Categorical profiling")
            st.json(report.get("categorical_profile"))

            st.subheader("Actionable warnings")
            warnings = report.get("warnings", [])
            if warnings:
                for w in warnings:
                    st.warning(w)
            else:
                st.success("No warnings generated.")

    except IngestionError as ie:
        st.error(f"Ingestion error: {ie}")
    except ValueError as ve:
        st.error(f"Value error: {ve}")
    except Exception as e:
        st.error(f"Unexpected error during analysis: {e}")
    finally:
        # Clean up temporary uploaded file
        try:
            if uploaded_file is not None and 'tmp_path' in locals():
                os.remove(tmp_path)
        except Exception:
            pass
