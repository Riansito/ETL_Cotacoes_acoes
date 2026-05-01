import pandas as pd
import yfinance as yf



list_tickers = [
    "PETR4.SA",
    "VALE3.SA",
    "ITUB4.SA",
    "BBDC4.SA",
    "WEGE3.SA",
    "^BVSP",
]

def extract_data(file_path, list_tickers, date) -> :
    list_df_tickers = list()
    for ticker_name in list_tickers:
        ticker = yf.Ticker(ticker_name)
        df = ticker.history(start=date).reset_index()
        df["ticker"] = ticker_name
        list_df_tickers.append(df)
    df = pd.concat(list_df_tickers)
    df.reset_index(inplace=True)
    df.to_csv(file_path)
    print("Salvo com sucesso no caminho: ", file_path)