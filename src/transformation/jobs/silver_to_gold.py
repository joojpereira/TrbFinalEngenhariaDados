"""
Issue #6 - Job PySpark: Silver -> Gold (Modelo Dimensional / Star Schema)

Le as tabelas refinadas da camada Silver e constroi um modelo dimensional
(esquema estrela) na camada Gold, em Delta Lake:

    fato_vendas      (grao = item de pedido)
    dim_cliente
    dim_produto
    dim_funcionario
    dim_tempo

A camada Gold alimenta o dashboard (Superset) com os KPIs e metricas.

Uso:
    spark-submit silver_to_gold.py

(roda todas as tabelas de uma vez - nao recebe parametro)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, year, month, quarter, dayofmonth, date_format,
    monotonically_increasing_id, current_timestamp, to_date
)


def build_spark_session() -> SparkSession:
    """Mesma configuracao Spark + Delta + MinIO usada nos demais jobs."""
    return (
        SparkSession.builder
        .appName("silver_to_gold")
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


def ler_silver(spark, tabela):
    """Le uma tabela Delta da camada Silver."""
    caminho = f"s3a://silver/{tabela}/"
    return spark.read.format("delta").load(caminho)


def gravar_gold(df, tabela):
    """Grava uma tabela Delta na camada Gold (overwrite)."""
    caminho = f"s3a://gold/{tabela}/"
    df.write.format("delta").mode("overwrite").save(caminho)
    print(f"Gravado: gold/{tabela} ({df.count()} linhas)")


# ----------------------------------------------------------------------
# DIMENSOES
# ----------------------------------------------------------------------

def construir_dim_cliente(spark):
    customers = ler_silver(spark, "customers")
    dim = customers.select(
        col("customer_id").alias("sk_cliente"),
        col("customer_id"),
        col("customer_name"),
        col("email"),
        col("city").alias("cidade"),
        col("state").alias("estado"),
    ).dropDuplicates(["customer_id"])
    return dim


def construir_dim_produto(spark):
    products = ler_silver(spark, "products")
    dim = products.select(
        col("product_id").alias("sk_produto"),
        col("product_id"),
        col("product_name"),
        col("unit_price").alias("preco_unitario"),
    ).dropDuplicates(["product_id"])
    return dim


def construir_dim_funcionario(spark):
    employees = ler_silver(spark, "employees")
    dim = employees.select(
        col("employee_id").alias("sk_funcionario"),
        col("employee_id"),
        col("employee_name"),
        col("hire_date").alias("data_contratacao"),
    ).dropDuplicates(["employee_id"])
    return dim


def construir_dim_tempo(spark):
    """
    Dimensao de tempo derivada das datas distintas de orders.
    A Silver ja calculou order_year/month/quarter, mas aqui montamos
    uma dimensao limpa, com uma linha por data.
    """
    orders = ler_silver(spark, "orders")
    datas = orders.select(to_date(col("order_date")).alias("data")).dropDuplicates(["data"])
    dim = (
        datas
        .withColumn("sk_tempo", date_format(col("data"), "yyyyMMdd").cast("int"))
        .withColumn("ano", year(col("data")))
        .withColumn("mes", month(col("data")))
        .withColumn("trimestre", quarter(col("data")))
        .withColumn("dia", dayofmonth(col("data")))
        .select("sk_tempo", "data", "ano", "mes", "trimestre", "dia")
    )
    return dim


# ----------------------------------------------------------------------
# FATO
# ----------------------------------------------------------------------

def construir_fato_vendas(spark):
    """
    Tabela fato no grao de ITEM DE PEDIDO.
    Junta order_details (o item) com orders (cabecalho do pedido,
    de onde vem cliente, funcionario e data).
    """
    order_details = ler_silver(spark, "order_details")
    orders = ler_silver(spark, "orders")

    # Junta o item de pedido com o cabecalho do pedido
    fato = order_details.join(orders, on="order_id", how="inner")

    fato = fato.select(
        col("order_id"),
        # chaves estrangeiras para as dimensoes
        col("customer_id").alias("sk_cliente"),
        col("product_id").alias("sk_produto"),
        col("employee_id").alias("sk_funcionario"),
        date_format(to_date(col("order_date")), "yyyyMMdd").cast("int").alias("sk_tempo"),
        # metricas (os numeros que o dashboard vai somar/medir)
        col("quantity").alias("quantidade"),
        col("unit_price").alias("preco_unitario"),
        col("total").alias("valor_total"),
        col("freight").alias("frete"),
    )
    return fato


def main():
    spark = build_spark_session()
    print("Construindo camada Gold (modelo dimensional)...\n")

    print("-> dim_cliente")
    gravar_gold(construir_dim_cliente(spark), "dim_cliente")

    print("-> dim_produto")
    gravar_gold(construir_dim_produto(spark), "dim_produto")

    print("-> dim_funcionario")
    gravar_gold(construir_dim_funcionario(spark), "dim_funcionario")

    print("-> dim_tempo")
    gravar_gold(construir_dim_tempo(spark), "dim_tempo")

    print("-> fato_vendas")
    gravar_gold(construir_fato_vendas(spark), "fato_vendas")

    print("\nCamada Gold concluida com sucesso.")
    spark.stop()


if __name__ == "__main__":
    main()
