"""
DAG: dag_northwind_to_landing
Issue #3 — Ingestão PostgreSQL -> Landing (MinIO)

Esqueleto: estrutura, agendamento diário, retry e uma task por tabela.
A lógica de extração (Postgres -> CSV -> MinIO) entra na próxima etapa.
"""
from __future__ import annotations

import logging
from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

logger = logging.getLogger(__name__)

# As 10 tabelas geradas no PR #13.
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


def extract_table_to_landing(table: str, **context) -> None:
    """Placeholder — a lógica de extração entra na Parte 3."""
    logger.info("TODO: extrair a tabela '%s' e gravar na Landing.", table)


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