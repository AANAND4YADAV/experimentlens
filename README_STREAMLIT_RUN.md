## Run Streamlit app (simple)

To run the minimal Streamlit interface included with ExperimentLens V1:

pip install -r requirements.txt
streamlit run app.py

The Streamlit app lets you upload a CSV (max 10 MB) or load the included example dataset at examples/sample_dataset.csv. The app passes the uploaded file through the existing ingestion and analysis pipeline and displays the report sections: dataset overview, preview, dtypes, missing values, duplicates, numerical statistics, IQR outliers, skewness, potentially unnecessary features, categorical profiling, and actionable warnings.
