from pyspark import pipelines as dp
from pyspark.sql import functions as F

SILVER_QUALITY_RULES = {
    "valid_transaction_id": "transaction_id IS NOT NULL",
    "valid_transaction_date": "transaction_date IS NOT NULL",
    "valid_transaction_timestamp": "transaction_timestamp IS NOT NULL",
    "positive_transaction_qty": "transaction_qty > 0",
    "valid_store_id": "store_id IS NOT NULL",
    "valid_product_id": "product_id IS NOT NULL",
    "positive_unit_price": "unit_price > 0"
}

@dp.table(
    name="caffaine.silver.coffee_sales_clean",
    comment="Cleaned and validated coffee sales transactions.",
    table_properties={"quality": "silver"},
)
@dp.expect_all_or_drop(SILVER_QUALITY_RULES)

def coffee_sales_clean():
    return (
        spark.readStream.table("caffaine.bronze.coffee_sales_raw")
        .select(
            F.col("transaction_id").cast("long").alias("transaction_id"),
            F.to_date("transaction_date", "yyyy-MM-dd").alias("transaction_date"),
            F.trim("transaction_time").alias("transaction_time"),
            F.col("transaction_qty").cast("int").alias("transaction_qty"),
            F.col("store_id").cast("int").alias("store_id"),
            F.trim("store_location").alias("store_location"),
            F.col("product_id").cast("int").alias("product_id"),
            F.col("unit_price").cast("decimal(10,2)").alias("unit_price"),
            F.trim("product_category").alias("product_category"),
            F.trim("product_type").alias("product_type"),
            F.trim("product_detail").alias("product_detail"),
            F.col("_source_file"),
            F.col("_source_file_path"),
            F.col("_source_file_modified_at"),
            F.col("_ingested_at"),
        )
        .withColumn(
            "transaction_timestamp",
            F.to_timestamp(
                F.concat_ws(
                    " ",
                    F.col("transaction_date").cast("string"),
                    F.col("transaction_time"),
                ),
                "yyyy-MM-dd H:mm:ss",
            ),
        )
        .withColumn(
            "sales_amount",
            (
                F.col("transaction_qty") * F.col("unit_price")
            ).cast("decimal(12,2)"),
        )
        .withColumn(
            "_silver_processed_at",
            F.current_timestamp()
        )
    )