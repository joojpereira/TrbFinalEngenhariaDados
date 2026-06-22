import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


DATA_DIR = Path("Data/generated")

DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin123")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "northwind")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

TABLES = [
    "regions",
    "territories",
    "categories",
    "suppliers",
    "products",
    "customers",
    "employees",
    "shippers",
    "orders",
    "order_details",
]


def load_csv_to_postgres(table_name: str, engine) -> None:
    csv_path = DATA_DIR / f"{table_name}.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

    print(f"Carregando {csv_path} para tabela {table_name}...")

    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=5000,
    )

    print(f"Tabela {table_name} carregada com {len(df)} registros.")


def main() -> None:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    for table in TABLES:
        load_csv_to_postgres(table, engine)

    print("Carga no PostgreSQL finalizada com sucesso!")


if __name__ == "__main__":
    main()import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


DATA_DIR = Path("Data/generated")

DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin123")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "northwind")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

TABLES = [
    "regions",
    "territories",
    "categories",
    "suppliers",
    "products",
    "customers",
    "employees",
    "shippers",
    "orders",
    "order_details",
]


def load_csv_to_postgres(table_name: str, engine) -> None:
    csv_path = DATA_DIR / f"{table_name}.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

    print(f"Carregando {csv_path} para tabela {table_name}...")

    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=5000,
    )

    print(f"Tabela {table_name} carregada com {len(df)} registros.")


def main() -> None:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    for table in TABLES:
        load_csv_to_postgres(table, engine)

    print("Carga no PostgreSQL finalizada com sucesso!")


if __name__ == "__main__":
    main()