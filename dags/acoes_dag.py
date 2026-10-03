from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys
import os
import json

# Adiciona a pasta /src ao PATH do Python
# Isso permite importar os módulos personalizados
# como extract.py, transform.py e load.py
sys.path.insert(0, '/opt/airflow/src')

# Importação das funções ETL
from extract import extract_data
from load import load_data
from transform import transform_data

# Biblioteca para carregar variáveis de ambiente
from dotenv import load_dotenv


# Caminho do arquivo .env
# O .env normalmente contém credenciais sensíveis,
# como usuário e senha do banco de dados
env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'

# Carrega as variáveis de ambiente
load_dotenv(env_path)


# ==========================================
# CAMINHOS DOS ARQUIVOS
# ==========================================

# Caminho onde os dados extraídos serão salvos em CSV
extracted_data_file_path = '/opt/airflow/data/extracted_data_tickers.csv'

# Caminho onde os dados transformados serão salvos em Parquet
transformed_data_file_path = '/opt/airflow/data/transformed_data_tickers.parquet'


# ==========================================
# CONFIGURAÇÕES DA EXTRAÇÃO
# ==========================================

# Carrega as configurações dos tickers a partir do arquivo config.json
config_file_path = Path(__file__).resolve().parent.parent / 'config' / 'config.json'

with open(config_file_path, 'r', encoding='utf-8') as f:
    config_data = json.load(f)

list_tickers = config_data["list_tickers"]
ticker_id_map = config_data["ticker_id_map"]


# ==========================================
# CONFIGURAÇÕES DA TRANSFORMAÇÃO
# ==========================================

# Colunas removidas durante o processo de transformação
# Essas colunas geralmente vêm vazias ou não serão utilizadas
columns_to_drop = [
    "Dividends",
    "Stock Splits",
    "ticker"
]

# Nome da tabela que receberá os dados no banco
table_name = "fato_acoes"


# ==========================================
# DEFINIÇÃO DA DAG
# ==========================================

@dag(
    
    # Nome único da DAG no Airflow
    dag_id='acoes_financas_etl',

    # Configurações padrão das tasks
    default_args={
        
        # Responsável pela DAG
        'owner': 'airflow',
        
        # Não depende da execução anterior
        'depends_on_past': False,
        
        # Número de tentativas em caso de erro
        'retries': 2,
        
        # Tempo de espera entre tentativas
        'retry_delay': timedelta(minutes=5)
    },

    # Descrição da DAG
    description='Pipeline ETL - Acoes Financas',

    # Executa às 05:00 da manhã de segunda a sexta
    schedule='0 5 * * 1-5',

    # Data inicial da DAG
    start_date=datetime(2026, 5, 4),

    # Evita executar execuções passadas automaticamente
    catchup=False,

    # Tags para organização no Airflow
    tags=['acoes', 'etl', 'se inscreve no canal!']
)

# Função principal da DAG
def acoes_pipeline():
    
    
    # ==========================================
    # TASK DE EXTRAÇÃO
    # ==========================================
    
    @task
    def extract(**kwargs):
        
        # Acessa a data lógica da execução através do contexto do Airflow (kwargs)
        # 'ds' é a string de data no formato YYYY-MM-DD
        date = kwargs.get('ds')

        # Realiza a coleta dos dados das ações
        # e salva em CSV
        extract_data(
            extracted_data_file_path,
            list_tickers,
            date
        )
        

    # ==========================================
    # TASK DE TRANSFORMAÇÃO
    # ==========================================
    
    @task
    def transform():
        
        # Executa as transformações dos dados
        df = transform_data(
            extracted_data_file_path,
            transformed_data_file_path,
            columns_to_drop, 
            ticker_id_map
        )

        # Salva os dados transformados em Parquet
        # O Parquet possui compressão e leitura otimizada
        df.to_parquet(transformed_data_file_path, index=False)
        

    # ==========================================
    # TASK DE CARGA
    # ==========================================
    
    @task 
    def load():
        
        import pandas as pd

        # Lê os dados transformados
        df = pd.read_parquet(transformed_data_file_path)

        # Envia os dados para o banco de dados
        load_data(table_name, df)
        

    # Define a ordem de execução das tasks
    # extract -> transform -> load
    extract() >> transform() >> load()


# Inicializa a DAG
acoes_pipeline()