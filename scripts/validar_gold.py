"""
Validacao da camada Gold - confere integridade do modelo dimensional
e calcula os KPIs/metricas que vao para o dashboard.

Uso:
    spark-submit validar_gold.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    sum as _sum, count, countDistinct, round as _round, col
)


def build_spark_session():
    return (
        SparkSession.builder
        .appName("validar_gold")
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


def ler(spark, tabela):
    return spark.read.format("delta").load(f"s3a://gold/{tabela}/")


def main():
    spark = build_spark_session()

    fato = ler(spark, "fato_vendas")
    dim_cliente = ler(spark, "dim_cliente")
    dim_produto = ler(spark, "dim_produto")
    dim_tempo = ler(spark, "dim_tempo")

    print("\n" + "=" * 55)
    print("VALIDACAO DA CAMADA GOLD")
    print("=" * 55)

    # --- Integridade referencial: toda chave da fato existe na dimensao? ---
    print("\n[1] Integridade referencial (chaves orfas = problema)")

    orfas_cliente = (
        fato.join(dim_cliente, "sk_cliente", "left_anti").count()
    )
    orfas_produto = (
        fato.join(dim_produto, "sk_produto", "left_anti").count()
    )
    orfas_tempo = (
        fato.join(dim_tempo, "sk_tempo", "left_anti").count()
    )
    print(f"  Linhas da fato sem cliente correspondente:    {orfas_cliente}")
    print(f"  Linhas da fato sem produto correspondente:    {orfas_produto}")
    print(f"  Linhas da fato sem tempo correspondente:      {orfas_tempo}")
    print("  (todos devem ser 0)")

    # --- KPIs / metricas ---
    print("\n[2] KPIs e metricas (o que vai pro dashboard)")

    total_linhas = fato.count()
    faturamento = fato.agg(_round(_sum("valor_total"), 2)).first()[0]
    frete_total = fato.agg(_round(_sum("frete"), 2)).first()[0]
    qtd_pedidos = fato.agg(countDistinct("order_id")).first()[0]
    itens_vendidos = fato.agg(_sum("quantidade")).first()[0]
    ticket_medio = round(faturamento / qtd_pedidos, 2) if qtd_pedidos else 0

    print(f"  Itens de venda (linhas da fato): {total_linhas}")
    print(f"  Faturamento total:               R$ {faturamento:,.2f}")
    print(f"  Frete total:                     R$ {frete_total:,.2f}")
    print(f"  Numero de pedidos:               {qtd_pedidos}")
    print(f"  Itens vendidos (qtd):            {itens_vendidos}")
    print(f"  Ticket medio por pedido:         R$ {ticket_medio:,.2f}")

    # --- Top 5 produtos por faturamento ---
    print("\n[3] Top 5 produtos por faturamento")
    top = (
        fato.groupBy("sk_produto")
        .agg(_round(_sum("valor_total"), 2).alias("faturamento"))
        .join(dim_produto, "sk_produto")
        .select("product_name", "faturamento")
        .orderBy(col("faturamento").desc())
        .limit(5)
    )
    top.show(truncate=False)

    print("=" * 55)
    print("Validacao concluida.")
    print("=" * 55 + "\n")

    spark.stop()


if __name__ == "__main__":
    main()
