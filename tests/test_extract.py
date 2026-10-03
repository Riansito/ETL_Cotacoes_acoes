import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.extract import extract_data

@patch("src.extract.yf.Ticker")
@patch("src.extract.pd.DataFrame.to_csv")
def test_extract_data_success(mock_to_csv, mock_ticker):
    # Setup mock dataframe returned by history
    mock_df = pd.DataFrame({"Close": [10.0, 11.0]})
    
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.history.return_value = mock_df
    mock_ticker.return_value = mock_ticker_instance
    
    # Executa a função
    extract_data("test_file.csv", ["AAPL"], "2023-01-01")
    
    # Verificações
    mock_ticker.assert_called_with("AAPL")
    mock_ticker_instance.history.assert_called_with(start="2023-01-01")
    mock_to_csv.assert_called_once_with("test_file.csv")

@patch("src.extract.yf.Ticker")
def test_extract_data_empty(mock_ticker):
    # Setup mock empty dataframe
    mock_df = pd.DataFrame()
    
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.history.return_value = mock_df
    mock_ticker.return_value = mock_ticker_instance
    
    # Verifica se levanta exceção
    with pytest.raises(ValueError, match="Sem dados para subir pro banco!"):
        extract_data("test_file.csv", ["AAPL"], "2023-01-01")
