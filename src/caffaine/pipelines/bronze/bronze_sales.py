from pyspark import pipelines as dp
from pyspark.sql import functions as F

SOURCE_PATH = "/Volumes/caffaine/bronze/source_files"

@dp.table(
    name="coffee_sales_raw",
    comment="Raw coffee sales records incrementally ingested from monthly csv files.",
    table_properties={"quality": "bronze"},
)
def coffee_sales_raw():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "false")
        .option("cloudFiles.schemaEvolutionMode", "rescue")
        .option("rescuedDataColumn", "_rescued_data")
        .load(SOURCE_PATH)
        .select(
            "*",
            F.col("_metadata.file_name").alias("_source_file"),
            F.col("_metadata.file_path").alias("_source_file_path"),
            F.col("_metadata.file_modification_time").alias("_source_file_modified_at"),
            F.current_timestamp().alias("_ingested_at"),
        )
    )