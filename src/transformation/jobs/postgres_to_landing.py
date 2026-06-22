"""
Issue #3 (parte) - Job PySpark: PostgreSQL -> Landing

Extrai cada tabela do PostgreSQL (origem) e grava o conteudo BRUTO em CSV
na camada Landing do data lake (MinIO), particionado por data:

    s3a://landing/sql/<tabela>/<ano>/<mes>/<dia>/

Esse e o formato que o job landing_to_bronze.py espera ler.

Uso:
    spark-submit --jars <postgres-jdbc.jar> postgres_to_landing.py <tabela> <ano> <mes> <dia>

Exemplo:
    spark-submit postgres_to_landing.py customers 2026 06 21

Observacao: precisa do driver JDBC do PostgreSQL disponivel para o Spark
(via --jars ou spark.jars.packages org.postgresql:postgresql:42.7.3).
"""

import sys

from pyspark.sql import SparkSession


def build_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("postgres_to_landing")
        .config(
            "spark.jars.packages",
            "io.delta:delta-spark_2.12:3.1.0,"
            "org.apache.hadoop:hadoop-aws:3.3.4,"
            "org.postgresql:postgresql:42.7.3",
        )
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        # MinIO (mesmas credenciais usadas pelos demais jobs)
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )


# Conexao com o PostgreSQL. Host "postgres" porque o Spark roda na MESMA
# rede docker (pipeline_net) que o container do banco.
JDBC_URL = "jdbc:postgresql://postgres:5432/food_delivery"
JDBC_PROPS = {
    "user": "admin",
    "password": "admin123",
    "driver": "org.postgresql.Driver",
}


def main():
    if len(sys.argv) != 5:
        print("Uso: spark-submit postgres_to_landing.py <tabela> <ano> <mes> <dia>")
        sys.exit(1)

    tabela, ano, mes, dia = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    spark = build_spark_session()

    print(f"Lendo tabela '{tabela}' do PostgreSQL...")
    df = spark.read.jdbc(url=JDBC_URL, table=tabela, properties=JDBC_PROPS)

    qtd = df.count()
    print(f"Linhas lidas do Postgres: {qtd}")

    caminho_landing = f"s3a://landing/sql/{tabela}/{ano}/{mes}/{dia}/"
    print(f"Gravando CSV bruto em: {caminho_landing}")

    # coalesce(1) -> um unico arquivo CSV por tabela/data (mais facil de inspecionar).
    (
        df.coalesce(1)
        .write
        .option("header", "true")
        .mode("overwrite")
        .csv(caminho_landing)
    )

    print(f"Concluido: {tabela} -> Landing ({qtd} linhas)")
    spark.stop()


if __name__ == "__main__":
    main()
