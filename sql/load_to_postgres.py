"""
Carrega os CSVs de Data/generated/ para o PostgreSQL (banco food_delivery).

Uso (com o ambiente Docker no ar):
    python sql/load_to_postgres.py

Obs.: por padrão conecta em localhost:5432. Se rodar de dentro da rede Docker,
defina PGHOST=postgres.
"""
import os

import pandas as pd
from sqlalchemy import create_engine

PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = os.getenv("PGPORT", "5432")
PGUSER = os.getenv("POSTGRES_USER", "admin")
PGPASS = os.getenv("POSTGRES_PASSWORD", "admin123")
PGDB = os.getenv("POSTGRES_DB", "food_delivery")

# Ordem respeitando dependencias (tabelas "pai" antes das "filhas")
TABLES = [
    "categories",
    "suppliers",
    "shippers",
    "regions",
    "products",
    "employees",
    "customers",
    "territories",
    "orders",
    "order_details",
]

DATA_DIR = "Data/generated"


def main():
    # connect_args explicito + client_encoding evita UnicodeDecodeError no Windows
    engine = create_engine(
        "postgresql+psycopg2://",
        connect_args={
            "host": PGHOST,
            "port": int(PGPORT),
            "user": PGUSER,
            "password": PGPASS,
            "dbname": PGDB,
            "client_encoding": "utf8",
        },
    )
    for table in TABLES:
        path = os.path.join(DATA_DIR, f"{table}.csv")
        df = pd.read_csv(path)
        df.to_sql(table, engine, if_exists="append", index=False)
        print(f"{table}: {len(df)} linhas carregadas")
    print("Concluido.")


if __name__ == "__main__":
    main()