from src.extract import extract_data
from src.transform import transform_data
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent

extracted_data_file_path = BASE_PATH / "data" / "extracted_data_tickers.csv"
transformed_data_file_path = BASE_PATH / "data" / "transformed_data_tickers.csv"

list_tickers = [
    "PETR4.SA",
    "VALE3.SA",
    "ITUB4.SA",
    "BBDC4.SA",
    "WEGE3.SA",
    "^BVSP",
]

columns_to_drop = [
    "Dividends",
    "Stock Splits"
]

date = "2026-04-30"

if __name__ == "__main__":
    extract_data(extracted_data_file_path, list_tickers, date)
    transform_data(extracted_data_file_path, transformed_data_file_path, columns_to_drop)
