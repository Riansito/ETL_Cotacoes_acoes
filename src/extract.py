import pandas as pd
import yfinance as yf


def extract_data(file_path, list_tickers, date):
    list_df_tickers = list()
    for ticker_name in list_tickers:
        ticker = yf.Ticker(ticker_name)
        df = ticker.history(start=date)
        df["ticker"] = ticker_name
        list_df_tickers.append(df)
    df = pd.concat(list_df_tickers)
    df.to_csv(file_path)
    print("Salvo com sucesso no caminho: ", file_path)