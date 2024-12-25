import tempfile
import pandas as pd


def csv_bytes_to_dataframe(byte_content: bytes) -> pd.DataFrame:
    """A helper method to convert byte object returned by S3 to pandas dataframe
    """
    tempfile_ = tempfile.NamedTemporaryFile()
    with open(tempfile_.name, 'wb') as f:
        f.write(byte_content)
    df = pd.read_csv(tempfile_.name)
    return df
