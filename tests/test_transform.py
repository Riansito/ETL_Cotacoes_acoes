import pytest
import pandas as pd
from unittest.mock import patch
from src.transform import (
    transform_drop_columns,
    transform_date,
    transform_name_tickers,
    transform_map_tickers,
    transform_data
)

def test_transform_drop_columns():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
    df_result = transform_drop_columns(df, ["B", "C"])
    assert list(df_result.columns) == ["A"]

def test_transform_date():
    df = pd.DataFrame({"Date": ["2023-01-01 10:00:00", "2023-01-02 12:00:00"]})
    df_result = transform_date(df)
    assert df_result["Date"].iloc[0] == pd.to_datetime("2023-01-01").date()
    assert df_result["Date"].iloc[1] == pd.to_datetime("2023-01-02").date()

def test_transform_name_tickers():
    df = pd.DataFrame({"ticker": ["PETR4.SA", "VALE3.SA"]})
    df_result = transform_name_tickers(df)
    assert df_result["ticker"].tolist() == ["PETR4", "VALE3"]

def test_transform_map_tickers():
    df = pd.DataFrame({"ticker": ["PETR4", "VALE3"]})
    ticker_map = {"PETR4": 1, "VALE3": 2}
    df_result = transform_map_tickers(df, ticker_map)
    assert df_result["Id_Ticker"].tolist() == [1, 2]

@patch("src.transform.pd.read_csv")
def test_transform_data(mock_read_csv):
    mock_df = pd.DataFrame({
        "Date": ["2023-01-01 10:00:00"],
        "ticker": ["PETR4.SA"],
        "Open": [10.0],
        "drop_me": [1]
    })
    mock_read_csv.return_value = mock_df
    
    ticker_map = {"PETR4": 1}
    columns_to_drop = ["drop_me"]
    
    df_result = transform_data("input.csv", "output.parquet", columns_to_drop, ticker_map)
    
    # Verifica transformações
    assert df_result["Date"].iloc[0] == pd.to_datetime("2023-01-01").date()
    assert df_result["ticker"].iloc[0] == "PETR4"
    assert df_result["Id_Ticker"].iloc[0] == 1
    assert "drop_me" not in df_result.columns
    assert "Open" in df_result.columns
