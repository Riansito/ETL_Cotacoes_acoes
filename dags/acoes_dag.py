from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys
import os

sys.path.insert(0, '/opt/airflow/src')

from extract import extract_data
from load import load_data
from transform import transform_data
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)


# Caminhos dos arquivos
extracted_data_file_path = '/opt/airflow/data/extracted_data_tickers.csv'

transformed_data_file_path = '/opt/airflow/data/transformed_data_tickers.parquet'


# Lista de tickers que serão coletados
list_tickers = [
    "PETR4.SA",
    "VALE3.SA",
    "ITUB4.SA",
    "BBDC4.SA",
    "WEGE3.SA",
]


# Colunas que serão removidas durante a transformação
columns_to_drop = [
    "Dividends",
    "Stock Splits"
]

# Data inicial da coleta
date = str(datetime.now().date())

table_name = "acoes_financas"

@dag(
    dag_id='acoes_financas_etl',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Pipeline ETL - Acoes Financas',
    schedule='0 */1 * * * ',
    start_date=datetime(2026, 5, 4),
    catchup=False,
    tags=['acoes', 'etl', 'se inscreve no canal!']
)
def acoes_pipeline():
    
    @task
    def extract():
        extract_data(
            extracted_data_file_path,
            list_tickers,
            date
        )
        
    @task
    def transform():
        df = transform_data(
            extracted_data_file_path,
            transformed_data_file_path,
            columns_to_drop
        )
        df.to_parquet(transformed_data_file_path, index=False)
        
    @task 
    def load():
        import pandas as pd
        df = pd.read_parquet(transformed_data_file_path)
        load_data(table_name, df)
        
    extract() >> transform() >> load()

acoes_pipeline()