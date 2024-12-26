import pytest
import pandas as pd
from src.datalib.data_processing import load_csv, normalize_data, handle_missing_values



def test_load_csv():
    df = load_csv('Catalog.csv')
    assert isinstance(df, pd.DataFrame)

def test_normalize_data():
    df = pd.DataFrame({'A': [1, 2, 3, 4]})
    normalized_df = normalize_data(df)
    assert normalized_df['A'].min() == 0
    assert normalized_df['A'].max() == 1

def test_handle_missing_values():
    df = pd.DataFrame({'A': [1, 2, None, 4]})
    filled_df = handle_missing_values(df, method="mean")
    assert filled_df['A'].isna().sum() == 0
