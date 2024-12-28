# src/pyeda/utils/helpers.py
import pandas as pd
import numpy as np

def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Validate input DataFrame"""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    if df.empty:
        raise ValueError("DataFrame is empty")
    return df