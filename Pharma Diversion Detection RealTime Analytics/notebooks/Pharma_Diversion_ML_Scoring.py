from pyspark.sql.functions import col, when
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier

# Read historical streaming delta table
df_raw = spark.read.table("Pharma_Compliance_Ops.RawPrescriptions")

# Feature Transformation
indexer_loc = StringIndexer(inputCol="location", outputCol="loc_indexed").fit(df_raw)
indexer_drug = StringIndexer(inputCol="drug_name", outputCol="drug_indexed").fit(df_raw)
df_indexed = indexer_drug.transform(indexer_loc.transform(df_raw))

assembler = VectorAssembler(
    inputCols=["units_dispensed", "risk_score", "loc_indexed", "drug_indexed"],
    outputCol="features"
)
df_features = assembler.transform(df_indexed)

# Label construction (1 for confirmed diversion, 0 for clean)
df_data = df_features.withColumn("label", when(col("anomaly_type") != "None", 1.0).otherwise(0.0))

# Train 20-Tree Random Forest Model
rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=20, maxBins=64)
model = rf.fit(df_data)

# Score and filter high-confidence violations
predictions = model.transform(df_features)
df_alerts = predictions.filter(col("prediction") == 1.0).select(
    col("rx_id"),
    col("patient_id"),
    col("units_dispensed").alias("FlaggedUnits"),
    col("drug_name"),
    col("location"),
    col("timestamp"),
    col("anomaly_type").alias("DiversionType")
)

# Write to Gold Delta Table
df_alerts.write.mode("overwrite").format("delta").saveAsTable("Pharma_Compliance_Ops.diversion_alerts")
print("Diversion alerts successfully generated in Lakehouse Gold Table.")