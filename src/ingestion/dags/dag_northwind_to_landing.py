"""
DAG: dag_northwind_to_landing
Issue #3 — Ingestão PostgreSQL -> Landing (MinIO)

Extrai cada tabela do PostgreSQL (banco `food_delivery`) e grava como CSV no
MinIO, na camada Landing, particionado por data:

    landing/sql/{tabela}/{ano}/{mes}/{dia}/{tabela}.csv

- Uma task por tabela.
- Agendamento diário (@daily), retry em caso de falha.
"""
from __future__ import annotations

import io
import logging
import os
from datetime import timedelta

import boto3
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# --- Configuração ----------------------------------------------------------
POSTGRES_CONN_ID = "postgres_origem"

# Lidos do ambiente (vêm do .env via docker-compose); defaults batem com o .env
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
LANDING_BUCKET = os.getenv("LANDING_BUCKET", "landing")

TABLES = [
    "categories",
    "customers",
    "employees",
    "products",
    "regions",
    "shippers",
    "suppliers",
    "territories",
    "orders",
    "order_details",
]

DEFAULT_ARGS = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


# --- Helpers ---------------------------------------------------------------
def _minio_client():
    """Cliente boto3 apontando para o MinIO (path-style + s3v4)."""
    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        region_name="us-east-1",
    )


def _ensure_bucket(client, bucket: str) -> None:
    """Garante que o bucket existe (cria se necessário)."""
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError:
        try:
            client.create_bucket(Bucket=bucket)
            logger.info("Bucket '%s' criado.", bucket)
        except ClientError as exc:
            logger.warning("create_bucket('%s'): %s", bucket, exc)


# --- Task ------------------------------------------------------------------
def extract_table_to_landing(table: str, **context) -> None:
    """Lê a tabela do Postgres e grava o CSV particionado no MinIO."""
    logical_date = context["logical_date"]
    ano = logical_date.strftime("%Y")
    mes = logical_date.strftime("%m")
    dia = logical_date.strftime("%d")

    # 1) Extrai do Postgres
    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    df = hook.get_pandas_df(f'SELECT * FROM "{table}"')
    logger.info("Tabela '%s': %d linhas extraídas.", table, len(df))

    # 2) Serializa em CSV (em memória)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    body = buffer.getvalue().encode("utf-8")

    # 3) Grava no MinIO (camada Landing, particionado por data)
    key = f"sql/{table}/{ano}/{mes}/{dia}/{table}.csv"
    client = _minio_client()
    _ensure_bucket(client, LANDING_BUCKET)
    client.put_object(Bucket=LANDING_BUCKET, Key=key, Body=body)
    logger.info("Gravado em s3://%s/%s (%d bytes).", LANDING_BUCKET, key, len(body))


# --- DAG -------------------------------------------------------------------
with DAG(
    dag_id="dag_northwind_to_landing",
    description="Issue #3 — Extrai tabelas do PostgreSQL e grava CSV na Landing (MinIO)",
    default_args=DEFAULT_ARGS,
    start_date=pendulum.datetime(2024, 1, 1, tz="America/Sao_Paulo"),
    schedule="@daily",
    catchup=False,
    tags=["ingestion", "landing", "northwind"],
) as dag:
    for table in TABLES:
        PythonOperator(
            task_id=f"extract_{table}",
            python_callable=extract_table_to_landing,
            op_kwargs={"table": table},
        )