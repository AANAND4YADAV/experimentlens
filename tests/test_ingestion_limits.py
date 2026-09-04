from src.experimentlens.ingestion import MAX_FILE_SIZE_BYTES
from src.experimentlens.ingestion import FileSizeError
import tempfile


def test_ingestion_file_size_limit():
    # create a temporary file larger than MAX_FILE_SIZE_BYTES
    with tempfile.NamedTemporaryFile(suffix=".csv") as tmp:
        tmp.write(b"0" * (MAX_FILE_SIZE_BYTES + 1))
        tmp.flush()
        try:
            # Attempt to validate by using the private _validate_file_size through load_csv indirectly
            # load_csv will raise FileSizeError when file is too large
            from src.experimentlens.ingestion import load_csv
            try:
                load_csv(tmp.name)
                raised = False
            except Exception as e:
                raised = isinstance(e, FileSizeError)
            assert raised, "Expected FileSizeError for oversized file"
        except AssertionError:
            raise
