from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys
import os

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

# Lista de ações (tickers) que serão coletadas
# ".SA" indica ações da bolsa brasileira (B3)
list_tickers = [
    "PETR4.SA",
    "VALE3.SA",
    "ITUB4.SA",
    "BBDC4.SA",
    "WEGE3.SA",
]


# ==========================================
# CONFIGURAÇÕES DA TRANSFORMAÇÃO
# ==========================================

# Colunas removidas durante o processo de transformação
# Essas colunas geralmente vêm vazias ou não serão utilizadas
columns_to_drop = [
    "Dividends",
    "Stock Splits"
]

# Data da coleta
# datetime.now().date() pega apenas a data atual
date = str(datetime.now().date())

# Nome da tabela que receberá os dados no banco
table_name = "acoes_financas"


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
    def extract():
        
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
            columns_to_drop
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