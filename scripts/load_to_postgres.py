"""
Carga dos dados de origem (CSV gerados via Faker) para o PostgreSQL.

Cria as tabelas (caso nao existam) e carrega cada CSV de Data/generated/
na tabela correspondente. Serve como etapa de "origem" do pipeline:
PostgreSQL -> (Airflow) -> Landing -> Bronze -> Silver -> Gold.

Pode ser executado manualmente:
    python scripts/load_to_postgres.py

Ou futuramente chamado por uma DAG do Airflow (issue #3).

Variaveis de conexao sao lidas do ambiente (.env), com defaults locais.
"""

import os
import sys

import pandas as pd
from sqlalchemy import create_engine, text

# --------------------------------------------------------------------------
# Configuracao de conexao
# --------------------------------------------------------------------------
# Quando rodado na sua MAQUINA (fora do Docker), o host e "localhost".
# Quando rodado DENTRO de um container na mesma rede, seria "postgres".
PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
PG_PORT = os.getenv("POSTGRES_PORT", "5432")
PG_USER = os.getenv("POSTGRES_USER", "admin")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin123")
PG_DB = os.getenv("POSTGRES_DB", "food_delivery")

DATA_DIR = os.getenv("DATA_DIR", "Data/generated")

# --------------------------------------------------------------------------
# Mapa: nome da tabela -> arquivo CSV
# A ordem importa: tabelas "pai" antes das que tem chave estrangeira.
# --------------------------------------------------------------------------
TABELAS = [
    ("categories", "categories.csv"),
    ("regions", "regions.csv"),
    ("shippers", "shippers.csv"),
    ("suppliers", "suppliers.csv"),
    ("employees", "employees.csv"),
    ("customers", "customers.csv"),
    ("products", "products.csv"),
    ("territories", "territories.csv"),
    ("orders", "orders.csv"),
    ("order_details", "order_details.csv"),
]


def build_engine():
    url = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    return create_engine(url)


def carregar_tabela(engine, tabela: str, arquivo: str) -> int:
    caminho = os.path.join(DATA_DIR, arquivo)
    if not os.path.exists(caminho):
        print(f"  [AVISO] arquivo nao encontrado: {caminho} -- pulando")
        return 0

    df = pd.read_csv(caminho)

    # to_sql cria a tabela automaticamente a partir do DataFrame (if_exists="replace").
    # chunksize evita estourar memoria em tabelas grandes (order_details ~200k).
    df.to_sql(
        tabela,
        engine,
        if_exists="replace",
        index=False,
        chunksize=10000,
        method="multi",
    )
    return len(df)


def main():
    print(f"Conectando em postgresql://{PG_USER}@{PG_HOST}:{PG_PORT}/{PG_DB}")
    engine = build_engine()

    # Teste de conexao rapido e claro (erro amigavel se o banco nao estiver de pe)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001
        print("\n[ERRO] Nao consegui conectar no PostgreSQL.")
        print("Verifique se o container esta rodando: docker compose ps")
        print(f"Detalhe: {exc}")
        sys.exit(1)

    total_geral = 0
    for tabela, arquivo in TABELAS:
        print(f"Carregando {tabela:15s} <- {arquivo}")
        qtd = carregar_tabela(engine, tabela, arquivo)
        print(f"  -> {qtd} linhas")
        total_geral += qtd

    print(f"\nConcluido. {len(TABELAS)} tabelas, {total_geral} linhas no total.")


if __name__ == "__main__":
    main()
