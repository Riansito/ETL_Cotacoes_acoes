import logging
from datetime import datetime
from pathlib import Path

from src.extract import extract_data
from src.load import load_data
from src.transform import transform_data


# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Caminho base do projeto
BASE_PATH = Path(__file__).resolve().parent


# Caminhos dos arquivos
extracted_data_file_path = (
    BASE_PATH / "data" / "extracted_data_tickers.csv"
)

transformed_data_file_path = (
    BASE_PATH / "data" / "transformed_data_tickers.parquet"
)


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


# Nome da tabela de destino no PostgreSQL
table_name = "acoes_financas"


if __name__ == "__main__":

    logger.info("Iniciando pipeline ETL financeiro.")

    try:

        # Etapa de extração
        extract_data(
            extracted_data_file_path,
            list_tickers,
            date
        )

        logger.info("Etapa de extração finalizada.")

        # Etapa de transformação
        transform_data(
            extracted_data_file_path,
            transformed_data_file_path,
            columns_to_drop
        )

        logger.info("Etapa de transformação finalizada.")

        # Etapa de carga
        load_data(
            table_name,
            transformed_data_file_path
        )

        logger.info("Pipeline ETL finalizado com sucesso.")

    except Exception as e:

        logger.exception(f"Erro durante execução do pipeline: {e}")

        # Relança erro para Airflow/orquestrador
        raise