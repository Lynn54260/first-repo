# ============================
# Bronze Customer Load
# ============================

from pyspark.sql.functions import current_timestamp, lit

# 1. Read CSV
customer_df = (
    spark.read
         .option("header", True)
         .option("inferSchema", True)
         .csv("dbfs:/FileStore/tables/customer.csv")
)

# 2. Add Bronze Metadata
bronze_customer_df = (
    customer_df
    .withColumn("LoadTimestamp", current_timestamp())
    .withColumn("SourceSystem", lit("SAP"))
)

# 3. Check Data
display(bronze_customer_df)

# 4. Create Bronze Delta Table
(
    bronze_customer_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("bronze_customer")
)

print("Bronze Customer Table Created Successfully")