"""
Issue #4 - Job PySpark: Landing -> Bronze (Delta Lake)

Le o CSV bruto da camada Landing (MinIO) e grava em formato Delta na camada
Bronze, adicionando colunas de auditoria (data de ingestao e arquivo de origem).

Uso:
    spark-submit landing_to_bronze.py <tabela> <ano> <mes> <dia>

Exemplo:
    spark-submit landing_to_bronze.py customers 2026 06 21
"""

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit


def build_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("landing_to_bronze")
        .config("spark.jars.packages",
                "io.delta:delta-spark_2.12:3.1.0,org.apache.hadoop:hadoop-aws:3.3.4")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        # Credenciais e endpoint do MinIO (definidas no .env do projeto)
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )


def main():
    if len(sys.argv) != 5:
        print("Uso: spark-submit landing_to_bronze.py <tabela> <ano> <mes> <dia>")
        sys.exit(1)

    tabela, ano, mes, dia = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    spark = build_spark_session()

    caminho_landing = f"s3a://landing/sql/{tabela}/{ano}/{mes}/{dia}/"
    caminho_bronze = f"s3a://bronze/{tabela}/"

    print(f"Lendo dados de: {caminho_landing}")

    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(caminho_landing)
    )

    qtd_linhas = df.count()
    print(f"Linhas lidas: {qtd_linhas}")

    df_bronze = (
        df.withColumn("dt_ingestao", current_timestamp())
          .withColumn("arquivo_origem", lit(f"{tabela}.csv"))
          .withColumn("particao_data", lit(f"{ano}-{mes}-{dia}"))
    )

    print(f"Gravando em: {caminho_bronze}")

    df_bronze.write.format("delta").mode("append").save(caminho_bronze)

    print(f"Concluido: {tabela} -> Bronze ({qtd_linhas} linhas)")

    spark.stop()


if __name__ == "__main__":
    main()
