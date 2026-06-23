"""
Issue #5 - Job PySpark: Bronze -> Silver (Delta Lake)

Le os dados da camada Bronze, aplica regras de qualidade (remocao de
duplicatas, tratamento de nulos, padronizacao de tipos e nomes de colunas)
e grava em Delta Lake na camada Silver.

Para a tabela "orders", calcula campos derivados de data:
order_year, order_month, order_quarter.

Uso:
    spark-submit bronze_to_silver.py <tabela>

Exemplo:
    spark-submit bronze_to_silver.py orders
"""

import re
import sys
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    col, trim, to_date, year, month, quarter, current_timestamp
)


def build_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("bronze_to_silver")
        .config("spark.jars.packages",
                "io.delta:delta-spark_2.12:3.1.0,org.apache.hadoop:hadoop-aws:3.3.4")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )


def to_snake_case(nome_coluna: str) -> str:
    """Converte um nome de coluna para snake_case, removendo espacos extras."""
    nome = nome_coluna.strip()
    nome = re.sub(r"[\s\-]+", "_", nome)
    nome = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", nome)
    return nome.lower()


def padronizar_colunas(df: DataFrame) -> DataFrame:
    for coluna in df.columns:
        nova_coluna = to_snake_case(coluna)
        if nova_coluna != coluna:
            df = df.withColumnRenamed(coluna, nova_coluna)
    return df


def limpar_dados(df: DataFrame) -> DataFrame:
    # Remove linhas totalmente duplicadas
    df = df.dropDuplicates()

    # Remove linhas completamente vazias
    df = df.dropna(how="all")

    # Padroniza colunas de texto: remove espacos extras nas pontas
    for nome_coluna, tipo in df.dtypes:
        if tipo == "string":
            df = df.withColumn(nome_coluna, trim(col(nome_coluna)))

    return df


def aplicar_regras_orders(df: DataFrame) -> DataFrame:
    """Regras especificas da tabela orders: campos derivados de data."""
    if "order_date" not in df.columns:
        return df

    df = df.withColumn("order_date", to_date(col("order_date")))
    df = (
        df.withColumn("order_year", year(col("order_date")))
          .withColumn("order_month", month(col("order_date")))
          .withColumn("order_quarter", quarter(col("order_date")))
    )
    return df


def main():
    if len(sys.argv) != 2:
        print("Uso: spark-submit bronze_to_silver.py <tabela>")
        sys.exit(1)

    tabela = sys.argv[1]

    spark = build_spark_session()

    caminho_bronze = f"s3a://bronze/{tabela}/"
    caminho_silver = f"s3a://silver/{tabela}/"

    print(f"Lendo dados de: {caminho_bronze}")
    df = spark.read.format("delta").load(caminho_bronze)

    qtd_linhas_bronze = df.count()
    print(f"Linhas lidas da Bronze: {qtd_linhas_bronze}")

    df = padronizar_colunas(df)
    df = limpar_dados(df)

    # Regras especificas por tabela
    if tabela == "orders":
        df = aplicar_regras_orders(df)

    df = df.withColumn("dt_atualizacao_silver", current_timestamp())

    qtd_linhas_silver = df.count()
    print(f"Linhas apos limpeza: {qtd_linhas_silver}")

    print(f"Gravando em: {caminho_silver}")
    df.write.format("delta").mode("overwrite").save(caminho_silver)

    print(f"Concluido: {tabela} -> Silver ({qtd_linhas_silver} linhas)")

    spark.stop()


if __name__ == "__main__":
    main()