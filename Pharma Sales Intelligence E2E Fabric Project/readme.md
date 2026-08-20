# End-to-End Pharmaceutical Commercial & Sales Analytics (Microsoft Fabric)

A scalable, production-grade Medallion Architecture implementation built on **Microsoft Fabric** to ingest, transform, validate, and report on enterprise-scale pharmaceutical sales, dispensing transactions, and commercial revenue.

---

## 🏗️ Architecture Overview

The platform uses a medallion data movement strategy within Microsoft Fabric:

1. **Landing Zone (OneLake / Lakehouse)**: Ingestion point for raw monthly prescription Parquet batches and dimensional CSV lookup files.
2. **Staging Layer (Warehouse - `stg`)**: Initial ingestion layer where raw data lands before undergoing stored-procedure-driven outlier detection, data hygiene checks, and audit logging.
3. **Presentation Layer (Warehouse - `dbo`)**: Star/Snowflake-aligned fact table enriched with product classifications, therapeutic areas, distributor profiles, and normalized payer channels.
4. **Semantic Model & Reporting (Direct Lake)**: Direct Lake mode Power BI semantic model featuring dynamic DAX KPIs for executive and commercial portfolio tracking.

---

## 📂 Repository Structure

```text
├── data/
│   ├── generate_pharma_data.py       # Generates synthetic monthly sales & lookups
│   ├── data_dictionary_pharma.py     # Generates PDF data dictionary
│   └── pharma_product_lookup.csv     # Master drug, therapeutic & segment lookup
├── sql/
│   ├── 01_staging_tables.sql         # DDL for staging schema & tables
│   ├── 02_metadata_logging.sql       # Audit logging tables & stored procedures
│   ├── 03_data_cleaning_sp.sql       # Date outlier elimination procedure
│   └── 04_presentation_layer.sql     # Target table & load stored procedure
├── pipelines/
│   ├── pl_stg_lookup.json            # Ingests master CSV lookups
│   ├── pl_stg_processing_pharma.json # Incremental monthly sales ingestion
│   ├── pl_pres_processing.json       # Presentation transformation pipeline
│   └── pl_orchestrate_pharma.json    # Master end-to-end orchestrator
├── reports/
│   └── Pharma_Sales_Report.pbip      # Power BI report definition
├── requirements.txt                  # Python dependencies
└── README.md
