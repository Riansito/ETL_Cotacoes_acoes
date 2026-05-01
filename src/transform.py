import pandas as pd

def transform_drop_columns(df, columns_to_drop) -> pd.DataFrame:
    df = df.drop(columns=columns_to_drop)
    return df

def transform_date(df) -> pd.DataFrame:
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df

def transform_name_tickers(df) -> pd.DataFrame:
    df["ticker"] = df["ticker"].str.replace(".SA", "", regex=False)
    df["ticker"] = df["ticker"].str.replace("^", "", regex=False)
    return df
    

def transform_data(file_path, file_path_to_save, columns_to_drop):
    df = pd.read_csv(file_path)
    df = transform_drop_columns(df, columns_to_drop)
    df = transform_date(df)
    df = transform_name_tickers(df)
    df.to_csv(file_path_to_save)
    print("Transformação feita com sucesso, arquivo salvo no caminho: ", file_path_to_save)