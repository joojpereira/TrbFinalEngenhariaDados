"""
Exporta as tabelas da camada Gold em Delta Lake/MinIO
para o PostgreSQL, permitindo o consumo pelo Superset.

Uso:
    spark-submit gold_to_postgres.py
"""

from pyspark.sql import SparkSession


TABELAS_GOLD = [
    "dim_cliente",
    "dim_produto",
    "dim_funcionario",
    "dim_tempo",
    "fato_vendas",
]


def build_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("gold_to_postgres")
        .config("spark.sql.extensions",
                "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        )
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config(
            "spark.hadoop.fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )
        .getOrCreate()
    )


def main():
    spark = build_spark_session()

    jdbc_url = "jdbc:postgresql://postgres:5432/food_delivery"

    propriedades = {
        "user": "admin",
        "password": "admin123",
        "driver": "org.postgresql.Driver",
    }

    for tabela in TABELAS_GOLD:
        origem = f"s3a://gold/{tabela}/"
        destino = f"gold.{tabela}"

        print(f"\nLendo: {origem}")

        df = (
            spark.read
            .format("delta")
            .load(origem)
        )

        quantidade = df.count()
        print(f"Linhas encontradas: {quantidade}")
        print(f"Gravando no PostgreSQL: {destino}")

        (
            df.write
            .format("jdbc")
            .option("url", jdbc_url)
            .option("dbtable", destino)
            .option("user", propriedades["user"])
            .option("password", propriedades["password"])
            .option("driver", propriedades["driver"])
            .mode("overwrite")
            .save()
        )

        print(f"Concluído: {destino}")

    print("\nTodas as tabelas Gold foram enviadas ao PostgreSQL.")

    spark.stop()


if __name__ == "__main__":
    main()